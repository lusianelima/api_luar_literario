from fastapi import APIRouter, HTTPException
from database import get_connection
from models import ConsignacaoModel

router = APIRouter()

@router.post("/api/consignacao")
def registrar_consignacao(dados: ConsignacaoModel):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        titulo = dados.titulo
        autor = dados.autor
        preco_venda = dados.preco_venda
        cpf_cliente = dados.cpf_cliente

        cursor.execute("START TRANSACTION;")

        # Verifica se o livro já existe
        cursor.execute("SELECT cod_livro FROM Livro WHERE titulo = %s FOR UPDATE;", (titulo,))
        livro = cursor.fetchone()

        if not livro:
            cursor.execute("""
                INSERT INTO Livro (titulo, autor, preco_venda)
                VALUES (%s, %s, %s);
            """, (titulo, autor, preco_venda))
            cod_livro = cursor.lastrowid
        else:
            cod_livro = livro['cod_livro']

        # Atualiza ou insere no estoque
        cursor.execute("SELECT cod_livro FROM Estoque WHERE cod_livro = %s;", (cod_livro,))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE Estoque
                SET quantidade = quantidade + 1
                WHERE cod_livro = %s;
            """, (cod_livro,))
        else:
            cursor.execute("""
                INSERT INTO Estoque (cod_livro, quantidade, quantidade_min)
                VALUES (%s, 1, 1);
            """, (cod_livro,))

        # Registra consignação
        cursor.execute("""
            INSERT INTO Consignacao (cpf_cliente, cod_livro, data_consignacao)
            VALUES (%s, %s, NOW());
        """, (cpf_cliente, cod_livro))

        conn.commit()
        return {"mensagem": "Consignação registrada com sucesso.", "cod_livro": cod_livro}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao registrar consignação: {e}")

    finally:
        cursor.close()
        conn.close()
