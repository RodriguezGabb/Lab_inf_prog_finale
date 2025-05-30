from typing import Dict, List, Tuple
from src.backend.mariadb_manager import execute_insert

def add_entry_to_movies(title:str, release_year:int, director:str, genre:str)->List[Tuple]:
    '''fill a line into movies table'''
    return execute_insert("INSERT INTO movies (titolo, anno, director, genre) VALUES (%s, %d, %s, %s) ON DUPLICATE KEY UPDATE anno=VALUES(anno), director = VALUES(director), genre = VALUES(genre);", (title, release_year, director, genre))

def add_entry_to_directors(director:str, age:int)->List[Tuple]:
    '''insert a line into directors table'''
    return execute_insert("INSERT INTO directors (director, age) VALUES (%s, %d) ON DUPLICATE KEY UPDATE age = VALUES(age);", (director, age))

def add_entry_to_platforms(title: str, platform1:str=None,platform2:str=None)->List[Tuple]:
    '''insert a line into relation_platform_film table'''
    if platform1:
        execute_insert("INSERT IGNORE INTO platform (platform_name) VALUES (%s)",(platform1,))
    if platform2:
        execute_insert("INSERT IGNORE INTO platform (platform_name) VALUES (%s)",(platform2,)) 
    
    return execute_insert("INSERT INTO relation_platform_film (titolo, platform1, platform2) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE platform1 = VALUES(platform1), platform2 = VALUES(platform2);", (title, platform1, platform2))

def add_from_row(row:Dict[str,str])->str:
    '''insert data into the database from dictionary made as such:
    row:Dict[str,str]={"Titolo":str,"Regista":str,"Età_Autore":str,"Anno":str, "Genere":str, "Piattaforma_1":str, "Piattaforma_2":str}
    those name depends from data.tsv
    '''
        
    title = row.get("Titolo")
    director = row.get("Regista")
    try:
        age = int(row.get("Età_Autore"))
    except ValueError:
        return "the age given is not a number" 
    try:
        release_year = int(row.get("Anno"))
    except ValueError:
        return "the release year is not a number"
    
    genre = row.get("Genere")
    platform1= row.get("Piattaforma_1")
    platform2 = row.get("Piattaforma_2")
    
    add_entry_to_directors(director,age)
    add_entry_to_movies(title,release_year,director,genre)
    #this if else section serve to insert every possible combination of platform in the database
    if platform1 and platform2:
        add_entry_to_platforms(title,platform1,platform2)
    elif platform1:
        add_entry_to_platforms(title,platform1=platform1)
    elif platform2:
        add_entry_to_platforms(title,platform2=platform2)
    else: 
        add_entry_to_platforms(title)
    return "ok"