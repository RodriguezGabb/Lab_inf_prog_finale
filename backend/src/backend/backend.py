from contextlib import asynccontextmanager
from io import StringIO
from typing import Any, Callable, Dict
from src.backend.add_request import add_from_row
from src.backend.get_request import get_film_da_anno, get_film_da_eta_regista, get_film_da_genere,get_regista_da_piattaforma, get_registi_con_piu_film,schema_summary
from src.backend.init_tables import init_tables
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from csv import DictReader


@asynccontextmanager
async def lifespan(app: FastAPI):#preso dalla documentazione serve a inizializzare le tabelle del database
    init_tables()
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

@app.get("/search/{question}")
def search(question:str):
    '''Rivela la domanda fatta grazie a un dizzionario che combina domanda (key) a funzione per la rispettiva domamda'''
    
    possible_question:Dict[str,Callable[[str],Any]]={
        "Elenca i film del ":get_film_da_anno,
        "Quali sono i registi presenti su ":get_regista_da_piattaforma,
        "Elenca tutti i film di ":get_film_da_genere,
        "Quali film sono stati fatti da un regista di almeno ":get_film_da_eta_regista,
        "Quali registi hanno fatto più di":get_registi_con_piu_film
    }
    sql_output=-1
    for que in possible_question:
        if que in question:
            question=question.replace(que,"")
            sql_output=possible_question[que](question)#question.split()[0])
         
    if sql_output==-1:#La richiesta non faceva parte di quelle eseguibili
        raise HTTPException(status_code=422, detail=f"La richiesta fatta \"{question}\" non è supportata")
    if isinstance(sql_output,str):
        raise HTTPException(status_code=400, detail=sql_output)
    return sql_output

class AddPayload(BaseModel):
    data_line:str
class AddValidation(BaseModel):
    status:str


@app.post("/add")
def add(request:AddPayload):
    line=request.data_line
    row = next(DictReader(StringIO(line), fieldnames=("Titolo",	"Regista", "Età_Autore", "Anno", "Genere", "Piattaforma_1", "Piattaforma_2")))
    if None in row:#controlla se cisono chiavi col valore None
        raise HTTPException(status_code=422, detail=f"La riga fornita per l'inserimento è troppo lunga")
    out=add_from_row(row)
    if out != "ok":
        raise HTTPException(status_code=422, detail=f"La richiesta di inserimento fatta non è conforme al modello richiesto:\n{out}")
    res=AddValidation(status=out)
    
    return res