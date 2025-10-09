# 📚 API Luar Literário: Sistema de Vendas Transacional

Este projeto implementa uma API de backend para um sistema de livraria (Luar Literário), focado em resolver problemas de **integridade de dados** e **concorrência** que são comuns em sistemas de gestão de estoque e vendas online. O foco principal é a aplicação de **Transações Explícitas** e mecanismos de **Controle de Concorrência** em um banco de dados relacional.

## 🎯 Objetivo Principal

O objetivo central é garantir que operações complexas de leitura e escrita sejam **atômicas** e **isoladas**.

* [cite_start]**Atomicidade (ACID):** Garantir que uma sequência de operações (como a baixa de estoque e o registro da venda) seja tratada como uma única unidade lógica: ou todas são concluídas com sucesso (`COMMIT`), ou nenhuma delas é aplicada (`ROLLBACK`)[cite: 12].
* [cite_start]**Controle de Concorrência:** Evitar **condições de corrida** (race conditions) onde múltiplos usuários tentam comprar o mesmo item simultaneamente, o que poderia levar a um estoque negativo ou inconsistente[cite: 22].

## ⚙️ Arquitetura e Tecnologias

* **Backend:** Python 3.x, **FastAPI**
* **Banco de Dados:** MySQL/MariaDB (Conexão via `pymysql`)
* **Gerenciamento de Transações:** Desabilitando o `autocommit` padrão e usando comandos SQL explícitos (`START TRANSACTION`, `COMMIT`, `ROLLBACK`).
* **Controle de Concorrência:** Bloqueio de linha pessimista (`SELECT... FOR UPDATE`).

## 💡 Solução de Concorrência em Detalhes

O principal desafio está na rota de **Venda (`/venda`)**, onde o estoque deve ser verificado e atualizado.

1.  **Início da Transação:** A rota inicia com `START TRANSACTION;`.
2.  **Bloqueio de Linha:** O sistema imediatamente consulta o estoque usando o bloqueio de linha (`FOR UPDATE`):
    ```sql
    SELECT quantidade FROM Estoque WHERE cod_livro = %s FOR UPDATE;
    ```
    * **Efeito:** Se dois clientes tentarem comprar o mesmo livro ao mesmo tempo, o primeiro adquire um bloqueio exclusivo na linha do estoque. O segundo cliente é **bloqueado** (colocado em espera) nessa mesma linha.
3.  **Verificação e Atualização:** Somente após o primeiro cliente liberar o bloqueio (via `COMMIT` ou `ROLLBACK`), o segundo cliente prossegue. [cite_start]Neste momento, o segundo cliente lerá a quantidade de estoque já atualizada pelo primeiro, evitando que o estoque fique negativo[cite: 18].
4.  **Finalização:** Em caso de sucesso, `conn.commit()` é chamado. Em falha (ex: estoque insuficiente, erro no registro de venda), `conn.rollback()` garante que o estoque não seja alterado.

Essa lógica é replicada em rotas críticas como **Compra**, **Consignação**, e **Ajuste de Estoque**.

## 🚀 Endpoints da API

A API é documentada via Swagger/OpenAPI (visível em `/docs` ao rodar localmente).

| Método | Endpoint | Descrição | Transação / Concorrência |
| :--- | :--- | :--- | :--- |
| `POST` | `/venda` | Realiza a venda de um livro. | **Crítico:** Garante a baixa atômica do estoque e bloqueia a linha de `Estoque` (`FOR UPDATE`). |
| `POST` | `/api/compra` | Registra a compra de livros, aumentando o estoque. | Garante a atualização atômica do estoque e registro da compra. |
| `POST` | `/api/consignacao` | Registra um livro em consignação, podendo criar o livro ou atualizar o estoque existente. | Garante a atomicidade da criação/atualização de `Livro`, `Estoque` e `Consignacao`. |
| `PUT` | `/api/estoque/ajustar` | Realiza o ajuste manual de um item no estoque. | Bloqueia a linha de `Estoque` (`FOR UPDATE`) antes de atualizar para prevenir ajustes concorrentes. |

## 🛠️ Como Rodar o Projeto

### Pré-requisitos
* Python 3.x
* MySQL/MariaDB

### 1. Configurar o Banco de Dados

Crie um banco de dados e configure as seguintes variáveis no arquivo `.env` (ou utilize as variáveis de ambiente do seu sistema):

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=luar_literario_db
```

Nota: O esquema SQL para criação das tabelas (Livro, Estoque, Venda, Compra, Consignacao, Venda_Livro, Compra_Livro) deve ser executado no seu banco de dados MySQL antes de iniciar a API.

### 2. Instalar Dependências
Instale as dependências necessárias listadas em requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Iniciar o Servidor
```bash
uvicorn main:app --reload
```

A API estará disponível em http://127.0.0.1:8000/. Acesse http://127.0.0.1:8000/docs para a documentação interativa (Swagger UI).