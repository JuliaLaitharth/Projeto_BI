CREATE TABLE DIM_DATA (
    id_data DATE PRIMARY KEY,
    dia INT,
    mes INT,
    trimestre INT,
    ano INT,
    dia_semana VARCHAR(20)
);

CREATE TABLE DIM_TITULAR (
    id_titular SERIAL PRIMARY KEY,
    nome_titular VARCHAR(100),
    final_cartao VARCHAR(4)
);

CREATE TABLE DIM_CATEGORIA (
    id_categoria SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(100)
);

CREATE TABLE DIM_ESTABELECIMENTO (
    id_estabelec SERIAL PRIMARY KEY,
    nome_estabelec VARCHAR(150)
);

CREATE TABLE FATO_TRANSACAO (
    id_transacao SERIAL PRIMARY KEY,
    id_data DATE REFERENCES DIM_DATA(id_data),
    id_titular INT REFERENCES DIM_TITULAR(id_titular),
    id_categoria INT REFERENCES DIM_CATEGORIA(id_categoria),
    id_estabelec INT REFERENCES DIM_ESTABELECIMENTO(id_estabelec),
    valor_brl DECIMAL(10,2),
    valor_usd DECIMAL(10,2),
    cotacao DECIMAL(10,4),
    parcela_texto VARCHAR(20), 
    num_parcela INT,           
    total_parcelas INT         
);
