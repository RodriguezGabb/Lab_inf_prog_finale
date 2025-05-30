import re
import requests

from src.backend.schema_info import ai_database_string
from src.backend.mariadb_manager import execute_query

def SQLinator(string:str, words:list[str])->str:
    # it merges the list in a str 
    pattern = '|'.join(words)
    # finds from one of the words to last ";"
    match = re.search(rf'\b({pattern})\b.*(;)', string.lower(), re.DOTALL)
    
    if match:
        # finds location and extract the sql
        start = match.start(1)  
        end = string.rfind(';') + 1
        return string[start:end]
    return None

def clean_ai(input:str)->str:
    ''' clean the sql from the ai, removing the ` and "sql" '''
    input=re.sub(r'`|sql', '', input, flags=re.IGNORECASE)
    commands = ['select','insert', 'update', 'delete', 'drop', 'alter', 'create', 'truncate', 'replace', 'grant', 'revoke', 'show', 'describe', 'explain']
    return SQLinator(input,commands)

def question_to_sql(prompt:str)->str:#TODO mettere anche il modello poi lo dobbiamo fissare ma se ci avvanza tempo facciamolo 
    '''this transform the question from the user into a sql query '''
    res=requests.post("http://ollama_esame:11434/api/chat",json={
        "model": "gemma3:1b-it-qat",
        "messages": [{ "role": "user", "content": prompt + "(answer only with a sql query for the following database without explanation or comments in the code. select only one column at the time.)"+ ai_database_string()}],
        "stream": False
    })
    return res.json().get("message").get("content")

def check_validation(sql:str)-> str:
    ''' this chek the validation of the sql query'''
    # commands that only read data from the dabase
    safe_commands = ['select'] 
    # commands that modify the data in the database , we consider 'show', 'describe' and 'explain' unsafe since it gives information on how the database is created to the user
    unsafe_commands = ['insert', 'update', 'delete', 'drop', 'alter', 'create', 'truncate', 'replace', 'grant', 'revoke', 'show', 'describe', 'explain']
    if sql:
        first_word=sql.split()[0].lower()

        if first_word not in safe_commands +unsafe_commands:
            #if first word is not a sql command
            return "invalid"
        elif first_word in unsafe_commands:
            #if first world is not select
            return "unsafe"
        
        try:
            #this will check if the sql is valid and safe by trying to execute it, it can't modify the databas
            execute_query("EXPLAIN " + sql)
            return "valid"
        except:
            #if sql has select as the first world but its not formatted correctly
            return "invalid"
    return "invalid"
    
