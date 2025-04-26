USE playmusica;

CREATE TABLE musica(
	id_musica INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome_musica VARCHAR(50) NOT NULL,
    cantor_banda VARCHAR(50) NOT NULL,
    genero_musica VARCHAR(20) NOT NULL
);
SELECT * FROM musica;

-- ordenando o id e o nome_musica 
SET @novo_id = 0;
UPDATE musica
SET id_musica = (@novo_id := @novo_id + 1)
ORDER BY nome_musica ASC;

ALTER TABLE musica AUTO_INCREMENT = 1;
SELECT * FROM musica;
SELECT * FROM musica ORDER BY nome_musica ASC;

CREATE TABLE musica_temp AS
SELECT * FROM musica ORDER BY nome_musica ASC;

ALTER TABLE musica_temp DROP COLUMN id_musica;
ALTER TABLE musica_temp ADD COLUMN id_musica INT PRIMARY KEY AUTO_INCREMENT FIRST;
DROP TABLE musica;
ALTER TABLE musica_temp RENAME TO musica;
-- fim da ordenação

SELECT * FROM musica;

CREATE TABLE usuario(
	id_usuario INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome_usuario VARCHAR(50) NOT NULL,
    login_usuario VARCHAR(50) UNIQUE NOT NULL,
    senha_usuario VARCHAR(255) NOT NULL
);

SELECT * FROM usuario;
SELECT * FROM musica;

ALTER TABLE usuario MODIFY COLUMN senha_usuario VARCHAR(255) NOT NULL;

