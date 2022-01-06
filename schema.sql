DROP TABLE IF EXISTS cliente;

CREATE TABLE cliente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    --name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

DROP TABLE IF EXISTS funcionario;

CREATE TABLE funcionario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    matricula TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

DROP TABLE IF EXISTS reclamacao;

CREATE TABLE reclamacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_email TEXT NOT NULL,
    cliente_login TEXT NOT NULL,
    reclamacao TEXT NOT NULL,
    data_reclamacao TEXT NOT NULL DEFAULT (datetime('now')),
    respondida BOOLEAN DEFAULT(FALSE)
);

DROP TABLE IF EXISTS obra;

CREATE TABLE obra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT UNIQUE NOT NULL,
    nome_autor TEXT UNIQUE NOT NULL,
    assunto TEXT NOT NULL,
    data_publicacao TEXT NOT NULL,
    posicao TEXT NOT NULL
);

DROP TABLE IF EXISTS emprestimo;

CREATE TABLE emprestimo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    obra_id INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL DEFAULT (datetime('now')),
    data_devolucao TEXT,
    devolvido BOOLEAN DEFAULT(FALSE),
    avaliacao INTEGER DEFAULT(0)
);