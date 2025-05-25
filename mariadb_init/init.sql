--creazione del user e del database 
CREATE USER IF NOT EXISTS 'film_user'@'localhost' IDENTIFIED BY 'filmpassword';
CREATE DATABASE IF NOT EXISTS esame;
GRANT ALL PRIVILEGES ON esame.* TO 'film_user'@'%' IDENTIFIED BY 'filmpassword';
USE esame;

--creo prima perché è foreign key
CREATE TABLE IF NOT EXISTS directors( 
    director VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY (director)
);

CREATE TABLE IF NOT EXISTS movies(
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    director VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    PRIMARY KEY (title),
    FOREIGN KEY (director) REFERENCES directors(director),
    CONSTRAINT UC_film UNIQUE (title, release_year, director),/*non può uscire lo stesso film nello stesso anno dallo stesso regista*/
    CONSTRAINT UC_film2 UNIQUE (title, release_year)/*non può uscire lo stesso film nello stesso anno*/
);



CREATE TABLE IF NOT EXISTS platform(
    platform_name VARCHAR(255) PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS relation_platform_film(
    id_relation INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    platform1 VARCHAR(255) ,
    platform2 VARCHAR(255) ,

    FOREIGN KEY (title) REFERENCES movies(title),
    FOREIGN KEY (platform1) REFERENCES platform(platform_name),
    FOREIGN KEY (platform2) REFERENCES platform(platform_name),
    PRIMARY KEY (id_relation),
    CONSTRAINT UC_platform UNIQUE (title)/*this is to have a single entry for each film*/
); 
