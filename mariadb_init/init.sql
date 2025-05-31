--creation of the database and the user 
CREATE USER IF NOT EXISTS 'film_user'@'localhost' IDENTIFIED BY 'filmpassword';
CREATE DATABASE IF NOT EXISTS esame;
GRANT ALL PRIVILEGES ON esame.* TO 'film_user'@'%' IDENTIFIED BY 'filmpassword';
USE esame;


CREATE TABLE IF NOT EXISTS directors( 
    director VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY (director)
);

CREATE TABLE IF NOT EXISTS movies(
    titolo VARCHAR(255) NOT NULL,
    anno INT NOT NULL,
    director VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    PRIMARY KEY (titolo),
    FOREIGN KEY (director) REFERENCES directors(director),
    CONSTRAINT UC_film UNIQUE (titolo, anno, director),
    CONSTRAINT UC_film2 UNIQUE (titolo, anno)
);



CREATE TABLE IF NOT EXISTS platform(
    platform_name VARCHAR(255) PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS relation_platform_film(
    id_relation INT AUTO_INCREMENT,
    titolo VARCHAR(255) NOT NULL,
    platform1 VARCHAR(255) ,
    platform2 VARCHAR(255) ,

    FOREIGN KEY (titolo) REFERENCES movies(titolo),
    FOREIGN KEY (platform1) REFERENCES platform(platform_name),
    FOREIGN KEY (platform2) REFERENCES platform(platform_name),
    PRIMARY KEY (id_relation),
    CONSTRAINT UC_platform UNIQUE (titolo)/*this is to have a single entry for each film*/
); 
