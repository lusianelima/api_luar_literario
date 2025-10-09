
-- Criação do banco de dados
-- CREATE DATABASE bd_luar_literario;
USE bd_luar_literario;

-- Tabela Livro
CREATE TABLE Livro (
    cod_livro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    estado VARCHAR(20),
    edicao VARCHAR(20),
    preco_venda DECIMAL(10,2)
);

-- Tabela Cliente
CREATE TABLE Cliente (
    cpf_cliente VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    tipo VARCHAR(20)
);

-- Tabela Fornecedor
CREATE TABLE Fornecedor (
    cnpj VARCHAR(18) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100)
);

-- Tabela Compra
CREATE TABLE Compra (
    idCompra INT AUTO_INCREMENT PRIMARY KEY,
    data_compra DATE,
    cnpj VARCHAR(18),
    FOREIGN KEY (cnpj) REFERENCES Fornecedor(cnpj)
);

-- Tabela Compra_livro
CREATE TABLE Compra_livro (
    idCompra INT,
    cod_livro INT,
    quantidade INT,
    valor_unitario DECIMAL(10,2),
    PRIMARY KEY (idCompra, cod_livro),
    FOREIGN KEY (idCompra) REFERENCES Compra(idCompra),
    FOREIGN KEY (cod_livro) REFERENCES Livro(cod_livro)
);

-- Tabela Estoque
CREATE TABLE Estoque (
    cod_livro INT PRIMARY KEY,
    quantidade INT,
    quantidade_min INT,
    FOREIGN KEY (cod_livro) REFERENCES Livro(cod_livro)
);

-- Tabela Venda
CREATE TABLE Venda (
    idVenda INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATE,
    valor_total DECIMAL(10,2),
    forma_pagam VARCHAR(20),
    cpf_cliente VARCHAR(14),
    FOREIGN KEY (cpf_cliente) REFERENCES Cliente(cpf_cliente)
);

-- Tabela Venda_livro
CREATE TABLE Venda_livro (
    idVenda INT,
    cod_livro INT,
    quantidade INT,
    preco_unitario DECIMAL(10,2),
    PRIMARY KEY (idVenda, cod_livro),
    FOREIGN KEY (idVenda) REFERENCES Venda(idVenda),
    FOREIGN KEY (cod_livro) REFERENCES Livro(cod_livro)
);

-- Tabela Consignacao
CREATE TABLE Consignacao (
    id_consignacao INT AUTO_INCREMENT PRIMARY KEY,
    status_exemplar VARCHAR(20),
    percentual_repass VARCHAR(10),
    data_entrada DATE,
    cpf_cliente VARCHAR(14),
    cod_livro INT,
    FOREIGN KEY (cpf_cliente) REFERENCES Cliente(cpf_cliente),
    FOREIGN KEY (cod_livro) REFERENCES Livro(cod_livro)
);

INSERT INTO Livro (titulo, autor, estado, edicao, preco_venda) VALUES
('Dom Casmurro', 'Machado de Assis', 'Usado', '3ª', 30.00),
('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 'Novo', '1ª', 50.00),
('Capitães da Areia', 'Jorge Amado', 'Seminovo', '2ª', 35.00),
('A Hora da Estrela', 'Clarice Lispector', 'Usado', '1ª', 25.00),
('Vidas Secas', 'Graciliano Ramos', 'Novo', '4ª', 45.00),
('A Cabeça do Santo', 'Socorro Acioli', 'Novo', '1ª', 45.99),
('O alquimista', 'Paulo Coelho', 'Seminovo', '1ª', 31.90),
('Memórias do subsolo', 'Fyodor Dostoevsky', 'Novo', '1ª', 39.50);

INSERT INTO Cliente (cpf_cliente, nome, telefone, email, tipo) VALUES
('111.111.111-11', 'Maria Silva', '99999-1111', 'maria@gmail.com', 'Consigador'),
('222.222.222-22', 'João Souza', '99999-2222', 'joao@gmail.com', 'Consignador'),
('333.333.333-33', 'Ana Lima', '99999-3333', 'ana@gmail.com', 'Consumidor'),
('444.444.444-44', 'Carlos Pereira', '99999-4444', 'carlos@gmail.com', 'Consignador'),
('555.555.555-55', 'Fernanda Dias', '99999-5555', 'fernanda@gmail.com', 'Consumidor'),
('365.041.585-32', 'Joana Dark', '95487-2164', 'darkjoana@gmail.com', 'Consignador'),
('725.254.348-35', 'Domenico', '94561-3672', 'domenico@gmail.com', 'Consumidor'),
('247.097.845-61', 'Francis Rios', '92359-8815', 'francis@gmail.com', 'Consumidor');


INSERT INTO Fornecedor (cnpj, nome, telefone, email) VALUES
('12.345.678/0001-01', 'Editora ABC', '3333-4444', 'abc@editora.com'),
('98.765.432/0001-02', 'Arqueiro', '5873-2156', 'xyz@arqui.com'),
('23.456.789/0001-03', 'Livros Brasil', '7777-8888', 'brasil@livros.com'),
('87.654.321/0001-04', 'Cultura Distribuidora', '4029-5390', 'cultura@distrib.com'),
('65.432.109/0001-05', 'Editora Nacional', '3487-5422', 'nacional@editora.com');

INSERT INTO Compra (data_compra, cnpj) VALUES
('2024-04-01', '12.345.678/0001-01'),
('2024-06-10', '98.765.432/0001-02'),
('2024-06-15', '23.456.789/0001-03'),
('2024-08-18', '87.654.321/0001-04'),
('2025-01-20', '65.432.109/0001-05'),
('2025-03-03', '23.456.789/0001-03'),
('2025-05-27', '87.654.321/0001-04');

INSERT INTO Compra_livro (idCompra, cod_livro, quantidade, valor_unitario) VALUES
(8, 1, 10, 20.00),
(9, 2, 5, 35.00),
(9, 3, 8, 25.00),
(10, 4, 7, 18.00),
(11, 5, 12, 30.00);

INSERT INTO Estoque (cod_livro, quantidade, quantidade_min) VALUES
(1, 10, 3),
(2, 5, 2),
(3, 1, 3),
(4, 7, 2),
(5, 3, 4),
(6, 2, 3),
(7, 5, 2),
(8, 12, 4);

INSERT INTO Venda (data_venda, valor_total, forma_pagam, cpf_cliente) VALUES
('2024-06-20', 100.00, 'PIX', '111.111.111-11'),
('2024-06-22', 70.00, 'Cartão', '333.333.333-33'),
('2024-06-23', 150.00, 'Dinheiro', '555.555.555-55'),
('2024-06-24', 90.00, 'PIX', '111.111.111-11'),
('2024-06-25', 60.00, 'Cartão', '333.333.333-33');

INSERT INTO Venda_livro (idVenda, cod_livro, quantidade, preco_unitario) VALUES
(1, 1, 2, 30.00),
(1, 2, 1, 50.00),
(2, 3, 2, 35.00),
(3, 4, 3, 25.00),
(4, 5, 2, 45.00),
(3, 6, 1, 45.99);

INSERT INTO Consignacao (status_exemplar, percentual_repass, data_entrada, cpf_cliente, cod_livro) VALUES
('Disponível', '60%', '2025-03-15', '111.111.111-11', 3),
('Vendido', '45%', '2024-02-08', '365.041.585-32', 4),
('Disponível', '55%', '2024-06-14', '222.222.222-22', 8),
('Vendido', '50%', '2024-06-16', '444.444.444-44', 2),
('Disponível', '65%', '2024-06-18', '222.222.222-22', 1);


