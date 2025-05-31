from contextlib import asynccontextmanager
from io import StringIO
import requests
from csv import DictReader
from fastapi import FastAPI, HTTPException

from src.backend.school import *
from src.backend.mariadb_manager import execute_query
from src.backend.add_request import add_from_row
from src.backend.get_request import schema_summary
from src.backend.init_tables import init_tables
from src.backend.ai_support import * 

@asynccontextmanager
async def lifespan(app: FastAPI):
    ''''taken by fastapi documentation, will set up the  tables with the starting elements and download gemma3:1b-it-qat as model for ollama'''
    init_tables()#initialize the database
    try:#download the ai model for the question in natural language
        res=requests.post("http://ollama_esame:11434/api/pull", json={ "model": "gemma3:1b-it-qat" })
        if (res.status_code != 200):
            raise Exception("the download of the ai model was unsuccessful")    
    except requests.exceptions.Timeout:
        raise Exception("the download of the ai model went in timeout ")
    except requests.exceptions.RequestException as e:
        raise Exception(f"the download of the ai model was unsuccessful, here is the error:\n{e}")
    yield

app=FastAPI(title="Film Questioner API",lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello from the Film Questioner API server"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/schema_summary")
def get_schema_summary():
    res=schema_summary()
    return res



@app.post("/search")
def search(question:SearchPayload)->ResultMacro:
    '''Take in input the question in natural language and return data from the database '''
    ai_sql=question_to_sql(question.question)
    sql=clean_ai(ai_sql) 
    sql_output= None
    validation=check_validation(sql)
    if validation=="valid":
        sql_output=execute_query(sql)
    
    data_type="film"

    search_result=result_builder(sql=ai_sql, vali=validation, sql_output=sql_output, request_type=data_type )

    return search_result

@app.post("/sql_search")
def sql_search(question:SqlSearchPayload)->ResultSqlSearch:
    '''Take in input a sql query and return data from the databse '''
    sql=question.sql_query
    validation=check_validation(sql)
    if validation=="valid":
        sql_output=execute_query(sql)
        data_type="film"
        result=result_micro_builder(sql_output=sql_output, type=data_type)
        return ResultSqlSearch(sql_validation=validation,results=result)
    return ResultSqlSearch(sql_validation=validation)


@app.post("/add")
def add(request:AddPayload):
    '''Take in input a csv string and add the data to the databse '''
    line=request.data_line
    row = next(DictReader(StringIO(line), fieldnames=("Titolo",	"Regista", "Età_Autore", "Anno", "Genere", "Piattaforma_1", "Piattaforma_2"))) #names taken from data.tsv
    emptiness= any((value is None or value == '') and key not in ("Piattaforma_1", "Piattaforma_2")for key, value in row.items())
    if emptiness or None in row.keys():#check if key or element is empty except "Piattaforma_2" and 1
        raise HTTPException(status_code=422, detail=f"the input is wrong")
    out=add_from_row(row)
    if out != "ok":
        raise HTTPException(status_code=422, detail=f"wrong input:\n{out}")
    res=AddValidation(status=out)
    return res

