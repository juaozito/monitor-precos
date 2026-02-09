CREATE DATABASE IF NOT EXISTS monitor_precos;
USE monitor_precos;

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco_atual DECIMAL(10, 2) NOT NULL,
    preco_antigo DECIMAL(10, 2),
    url_produto TEXT NOT NULL,
    url_imagem TEXT,
    loja VARCHAR(100),
    data_captura TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);