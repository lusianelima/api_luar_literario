from fastapi import APIRouter, HTTPException
from database import get_connection
from models import VendaModel

router = APIRouter()

@router.post("/venda")
def realizar_venda(venda: VendaModel):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("START TRANSACTION;")

        # Verifica estoque e bloqueia linha
        cursor.execute("SELECT quantidade FROM Estoque WHERE cod_livro = %s FOR UPDATE;", (venda.cod_livro,))
        result = cursor.fetchone()

        if not result:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Livro não encontrado.")

        if result['quantidade'] < venda.quantidade:
            conn.rollback()
            raise HTTPException(status_code=400, detail="Estoque insuficiente.")

        # Atualiza o estoque
        cursor.execute("""
            UPDATE Estoque
            SET quantidade = quantidade - %s
            WHERE cod_livro = %s;
        """, (venda.quantidade, venda.cod_livro))

        # Registra venda
        cursor.execute("""
            INSERT INTO Venda (data_venda, valor_total, forma_pagam, cpf_cliente)
            VALUES (NOW(), 0, %s, %s);
        """, (venda.forma_pagam, venda.cpf_cliente))
        id_venda = cursor.lastrowid

        # Insere na tabela venda_livro
        cursor.execute("""
            INSERT INTO Venda_livro (idVenda, cod_livro, quantidade, preco_unitario)
            VALUES (%s, %s, %s,
            (SELECT preco_venda FROM Livro WHERE cod_livro = %s));
        """, (id_venda, venda.cod_livro, venda.quantidade, venda.cod_livro))

        # Atualiza o valor total
        cursor.execute("""
            UPDATE Venda
            SET valor_total = (
                SELECT SUM(vl.quantidade * vl.preco_unitario)
                FROM Venda_livro vl
                WHERE vl.idVenda = %s
            )
            WHERE idVenda = %s;
        """, (id_venda, id_venda))

        conn.commit()
        return {"mensagem": "Venda concluída com sucesso.", "id_venda": id_venda}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro na transação: {str(e)}")

    finally:
        cursor.close()
        conn.close()
