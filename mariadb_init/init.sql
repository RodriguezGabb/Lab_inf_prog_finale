--creazione del user e del database 
CREATE USER IF NOT EXISTS 'film_user'@'localhost' IDENTIFIED BY 'filmpassword';
CREATE DATABASE IF NOT EXISTS esonero;
GRANT ALL PRIVILEGES ON esonero.* TO 'film_user'@'%' IDENTIFIED BY 'filmpassword';
USE esonero;

--creo prima perché è foreign key
CREATE TABLE IF NOT EXISTS Registi( 
    regista VARCHAR(255) NOT NULL,
    eta INT NOT NULL,
    PRIMARY KEY (regista)
);

CREATE TABLE IF NOT EXISTS movies(
    titolo VARCHAR(255) NOT NULL,
    anno INT NOT NULL,
    regista VARCHAR(255) NOT NULL,
    genere VARCHAR(255) NOT NULL,
    PRIMARY KEY (titolo),
    FOREIGN KEY (regista) REFERENCES Registi(regista),
    CONSTRAINT UC_film UNIQUE (titolo, anno, regista),/*non può uscire lo stesso film nello stesso anno dallo stesso regista*/
    CONSTRAINT UC_film2 UNIQUE (titolo, anno)/*non può uscire lo stesso film nello stesso anno*/
);



CREATE TABLE IF NOT EXISTS Piattaforme(
    id_piattaforma INT AUTO_INCREMENT,
    titolo VARCHAR(255) NOT NULL,
    piattaforma_1 VARCHAR(255),
    piattaforma_2 VARCHAR(255),
    PRIMARY KEY(id_piattaforma),
    FOREIGN KEY (titolo) REFERENCES movies(titolo),
    CONSTRAINT UC_piattafroma UNIQUE (titolo)
);  
