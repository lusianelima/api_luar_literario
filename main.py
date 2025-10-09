from fastapi import FastAPI
from routes_vendas import router as venda_router

app = FastAPI(
    title="API Luar Literário",
    description="Sistema de vendas com controle de transações e concorrência.",
    version="1.0"
)

app.include_router(venda_router, prefix="/api", tags=["Vendas"])

@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API Luar Literário!"}

from fastapi import FastAPI
from routes_vendas import router as vendas_router
from routes_compras import router as compras_router
from routes_consignacao import router as consignacoes_router
from routes_estoque import router as estoque_router

app = FastAPI(title="API Luar Literário")

app.include_router(vendas_router)
app.include_router(compras_router)
app.include_router(consignacoes_router)
app.include_router(estoque_router)
