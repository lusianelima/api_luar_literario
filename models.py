from pydantic import BaseModel
from typing import Optional

# ---------- VENDA ----------
class VendaModel(BaseModel):
    cod_livro: int
    quantidade: int
    cpf_cliente: str
    forma_pagam: str

# ---------- COMPRA ----------
class CompraModel(BaseModel):
    cod_livro: int
    quantidade: int
    preco_unit: float

# ---------- CONSIGNAÇÃO ----------
class ConsignacaoModel(BaseModel):
    titulo: str
    autor: str
    preco_venda: float
    cpf_cliente: str

# ---------- AJUSTE DE ESTOQUE ----------
class AjusteEstoqueModel(BaseModel):
    cod_livro: int
    nova_quantidade: int

