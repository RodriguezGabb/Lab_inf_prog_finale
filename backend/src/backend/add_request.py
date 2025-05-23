from typing import Dict, List, Tuple
from src.backend.mariadb_manager import execute_inserimento


def add_entry_to_movies(titolo:str, anno:int, regista:str, genere:str)->List[Tuple]:
    '''inserisce una nuova riga alla tabella film'''
    return execute_inserimento("INSERT INTO movies (titolo, anno, regista, genere) VALUES (%s, %d, %s, %s) ON DUPLICATE KEY UPDATE anno=VALUES(anno), regista = VALUES(regista), genere = VALUES(genere);", (titolo, anno, regista, genere))

def add_entry_to_registi(regista:str, eta:int)->List[Tuple]:
    '''inserisce una nuova riga alla tabella registi'''
    return execute_inserimento("INSERT INTO Registi (regista, eta) VALUES (%s, %d) ON DUPLICATE KEY UPDATE eta = VALUES(eta);", (regista, eta))

def add_entry_to_piattaforme(titolo: str, piattaforma_1:str,piattaforma_2:str=None)->List[Tuple]:
    '''inserisce una nuova riga alla tabella piattaforme'''
    if piattaforma_2: 
        return execute_inserimento("INSERT INTO Piattaforme (titolo, piattaforma_1, piattaforma_2) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE piattaforma_1 = VALUES(piattaforma_1), piattaforma_2 = VALUES(piattaforma_2);", (titolo, piattaforma_1, piattaforma_2))
    else:
        return execute_inserimento("INSERT INTO Piattaforme (titolo, piattaforma_1) VALUES (%s, %s) ON DUPLICATE KEY UPDATE piattaforma_1 = VALUES(piattaforma_1);", (titolo, piattaforma_1))

def add_from_row(row:Dict[str,str])->str:
    '''Aggiunge dati nel database a partire da un idizzionario sta composta nel seguente modo:
    row:Dict[str,str]={"Titolo":str,"Regista":str,"Età_Autore":str,"Anno":str, "Genere":str, "Piattaforma_1":str, "Piattaforma_2":str}
    '''
    for i in row:
        if not isinstance(row.get(i), str):
            return f"Il valore di {i} non è una stringa valida"
        
    titolo = row.get("Titolo")
    regista = row.get("Regista")
    try:
        eta = int(row.get("Età_Autore"))
    except ValueError:
        return "Il valore dato per l'età del regista non è numerio" 
    try:
        anno = int(row.get("Anno"))
    except ValueError:
        return "Il valore di Anno non è numerio"
    
    genere = row.get("Genere")
    piat_1= row.get("Piattaforma_1")
    piat_2 = row.get("Piattaforma_2")
    
    

    add_entry_to_registi(regista,eta)
    add_entry_to_movies(titolo,anno,regista,genere)
    if piat_2: 
        add_entry_to_piattaforme(titolo,piat_1,piat_2)
    else:
        add_entry_to_piattaforme(titolo,piat_1)
    return "ok"