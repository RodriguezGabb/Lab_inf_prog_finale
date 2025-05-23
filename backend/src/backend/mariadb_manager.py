from typing import Any, List, Tuple
import mariadb

def connect() -> mariadb.Connection:
    '''inizializza conessione con la piattaforma di mariadb con il user "film_user" e ritorna la conessione'''
    try:
        conn = mariadb.connect(
            host="mariadb_esonero",
            port=3306,
            user="film_user",
            password="filmpassword",
            database="esonero"
        )
    except mariadb.Error as e:
        raise Exception(f"Errore nella connessione con la piattaforma di maria db: {e}")
    return conn

def execute_query(query: str) -> List[Tuple]:
    '''esegue la querie che gli arriva in input con gli attributi forniti, e restituisce un output'''
    connection: mariadb.Connection = connect()
    cursor : mariadb.Cursor=connection.cursor()
    try:
        cursor.execute(query)
    except mariadb.Error as e:
        raise Exception(f"Errore nel escuzuine della query {query}:\n {e}")
    try:
        results: Any = cursor.fetchall()
    except mariadb.Error as e:
        raise Exception(f"Errore nel recupero del output della query {query}:\n {e}")
    
    connection.commit()
    cursor.close()
    connection.close()
    return results

def execute_inserimento(query: str,attributi: Tuple) -> str:
    '''esegue l'inserimento che gli arriva in input con gli attributi forniti'''
    connection: mariadb.Connection = connect()
    cursor : mariadb.Cursor=connection.cursor()
    try:
        cursor.execute(query,attributi)
    except mariadb.Error as e:
        return f"Errore nel escuzuine del inseriment {query}:\n {e}"
    connection.commit()
    cursor.close()
    connection.close()
    return "ok"


