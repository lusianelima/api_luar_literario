from fastapi import APIRouter, HTTPException
from database import get_connection
from models import AjusteEstoqueModel

router = APIRouter()

@router.put("/api/estoque/ajustar")
def ajustar_estoque(dados: AjusteEstoqueModel):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cod_livro = dados.cod_livro
        nova_quantidade = dados.nova_quantidade

        cursor.execute("START TRANSACTION;")

        cursor.execute("SELECT quantidade FROM Estoque WHERE cod_livro = %s FOR UPDATE;", (cod_livro,))
        if not cursor.fetchone():
            conn.rollback()
            raise HTTPException(status_code=404, detail="Livro não encontrado no estoque.")

        cursor.execute("""
            UPDATE Estoque
            SET quantidade = %s
            WHERE cod_livro = %s;
        """, (nova_quantidade, cod_livro))

        conn.commit()
        return {"mensagem": "Estoque ajustado com sucesso."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao ajustar estoque: {e}")

    finally:
        cursor.close()
        conn.close()
