from fastapi import APIRouter, HTTPException
from database import get_connection
from models import CompraModel

router = APIRouter()

@router.post("/api/compra")
def registrar_compra(dados: CompraModel):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cod_livro = dados.cod_livro
        quantidade = dados.quantidade
        preco_unit = dados.preco_unit

        cursor.execute("START TRANSACTION;")

        # Confere se o livro existe
        cursor.execute("SELECT cod_livro FROM Estoque WHERE cod_livro = %s FOR UPDATE;", (cod_livro,))
        if not cursor.fetchone():
            conn.rollback()
            raise HTTPException(status_code=404, detail="Livro não encontrado.")

        # Atualiza o estoque (entrada)
        cursor.execute("""
            UPDATE Estoque
            SET quantidade = quantidade + %s
            WHERE cod_livro = %s;
        """, (quantidade, cod_livro))

        # Registra a compra
        cursor.execute("""
            INSERT INTO Compra (data_compra, valor_total)
            VALUES (NOW(), %s);
        """, (quantidade * preco_unit,))
        id_compra = cursor.lastrowid

        cursor.execute("""
            INSERT INTO Compra_Livro (idCompra, cod_livro, quantidade, valor_unitario)
            VALUES (%s, %s, %s, %s);
        """, (id_compra, cod_livro, quantidade, preco_unit))

        conn.commit()
        return {"mensagem": "Compra registrada com sucesso.", "id_compra": id_compra}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao registrar compra: {e}")

    finally:
        cursor.close()
        conn.close()
