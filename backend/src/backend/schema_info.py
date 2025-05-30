from itsdangerous import BadData
import mariadb
from typing import Any, List, Tuple

# from src.backend.mariadb_manager import execute_query
# from mariadb_manager import execute_query

def connect() -> mariadb.Connection:
    '''starts the connection with mariadb with user "film_user"'''
    try:
        conn = mariadb.connect(
            host="localhost",
            port=3307,
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

def get_db_struct()->dict:
    '''retuns database structure for ai'''
    
    try:
        # retriving columns 
        table_columns=execute_query("""
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'esame'
            ORDER BY table_name, ordinal_position;
        """)
        print("## tables in database\n")
        print(table_columns)

        # primary key
        tables_primry=execute_query("""
            SELECT DISTINCT kcu.table_name, 
                   kcu.column_name AS primary_key
            FROM information_schema.table_constraints tco
            JOIN information_schema.key_column_usage kcu
              ON tco.constraint_name = kcu.constraint_name
             AND tco.table_schema = kcu.table_schema
            WHERE tco.constraint_type = 'PRIMARY KEY'
              AND tco.table_schema = 'esame'
        """)
        print("\n## table name and primary keys\n")
        print(tables_primry)

        # Foreign key
        tables_foreign=execute_query("""
            SELECT kcu.table_name,
                   kcu.column_name,
                   kcu.referenced_table_name,
                   kcu.referenced_column_name
            FROM information_schema.referential_constraints rc
            JOIN information_schema.key_column_usage kcu
              ON rc.constraint_name = kcu.constraint_name
             AND rc.constraint_schema = kcu.constraint_schema
            WHERE rc.constraint_schema = 'esame'
        """)
        print("\n## Foreign key\n")
        print(tables_foreign)
        print("\n\n\n")
        

        # data organization
        db_structure = {}

        # adding columns
        for table, column in table_columns:
            db_structure.setdefault(table, {})
            db_structure[table].setdefault('columns', []).append(column)

        #  primary keys
        for table, primary_k in tables_primry:
            db_structure.setdefault(table, {})
            db_structure[table]['primary_key'] = primary_k

        #  foreign keys
        for foreign_k_table, foreign_k_column, connected_table, connected_column in tables_foreign:
            db_structure.setdefault(foreign_k_table, {})
            db_structure[foreign_k_table].setdefault('foreign_keys', []).append({
                'column': foreign_k_column,
                'connected_table': connected_table,
                'connected_column': connected_column
            })
        return  db_structure
    except mariadb.Error as e:
        raise(f"Error while finding the database structure: {e}")

# print function
def print_db_structure(db_struct):
    '''print of the database structure for us humans, its the base for stringify_structure'''
    for table, info in db_struct.items():
        print(f"table: {table}")
        print(f"columns: {', '.join(info.get('columns', []))}")
        primary_key = info.get('primary_key')
        if primary_key:
            print(f"primary key: {primary_key}")
        foreign_key = info.get('foreign_keys', [])
        if foreign_key:
            print(f"  foreign key:")
            for key in foreign_key:
                print(f"- columns '{key['column']}' related to '{key['connected_table']}.{key['connected_column']}'")
        print()  # space between prints

def stringify_structure(db_struct)->str:
    '''transform the database structure into a string ready for the ai to read'''
    string_to_ai=""
    for table, info in db_struct.items():
        string_to_ai+=f"this table name is: {table}, "
        string_to_ai+=f"it has as columns: {', '.join(info.get('columns', []))}. "
        string_to_ai+=f"the primary key of this table is: {info.get('primary_key')}. "
        foreign_key = info.get('foreign_keys', [])
        if foreign_key:
            string_to_ai+=f"the foreign key of this table are: "
            for key in foreign_key:
                string_to_ai+=f"- columns '{key['column']}' it is related to the column'{key['connected_column']}' of the table {key['connected_table']}', "
    return string_to_ai

def ai_database_string()->str:
    '''this function is only used by the ai to get information on the schema'''
    return stringify_structure(get_db_struct())
    
if __name__== "__main__":
  struct=get_db_struct()
  stringForAi=stringify_structure(struct)
  print("\n\n\n")
  print(stringForAi)
