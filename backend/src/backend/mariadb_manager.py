from typing import Any, List, Tuple
import mariadb

def connect() -> mariadb.Connection:
    '''starts the connection with mariadb with user "film_user"'''
    try:
        conn = mariadb.connect(
            host="mariadb_esame",
            port=3306,
            user="film_user",
            password="filmpassword",
            database="esame"
        )
    except mariadb.Error as e:
        raise Exception(f"error in the connection with mariadb: {e}")
    return conn

def execute_query(query: str) -> List[Tuple]:
    '''execute query, return the output'''
    connection: mariadb.Connection = connect()
    cursor : mariadb.Cursor=connection.cursor()
    try:
        cursor.execute(query)
    except mariadb.Error as e:
        raise Exception(f"Error in the execution of the following query:\n {query}\n the error message is:\n {e}")
    try:
        results: Any = cursor.fetchall()
    except mariadb.Error as e:
        raise Exception(f"Error in the return of the following query: {query}\n the error message is:\n:\n {e}")

    connection.commit()
    cursor.close()
    connection.close()
    return results

def execute_insert(query: str,attribute: Tuple) -> str:
    '''insert data into tables'''
    connection: mariadb.Connection = connect()
    cursor : mariadb.Cursor=connection.cursor()
    try:
        cursor.execute(query,attribute)
    except mariadb.Error as e:
        return f"error in the execution of the insert: {query}:\n {e}"
    connection.commit()
    cursor.close()
    connection.close()
    return 'ok'
