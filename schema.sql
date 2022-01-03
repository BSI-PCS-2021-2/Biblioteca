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
    cliente_email TEXT UNIQUE NOT NULL,
    cliente_login TEXT UNIQUE NOT NULL,
    reclamacao TEXT NOT NULL,
    data_reclamacao TEXT NOT NULL DEFAULT (datetime('now')),
    respondida BOOLEAN DEFAULT(FALSE)
);