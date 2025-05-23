from pydantic import BaseModel
import requests
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
import os

app= FastAPI()
path_cartella_corrente = os.path.dirname(os.path.abspath(__file__))
path_cartella_src=os.path.dirname(os.path.dirname(path_cartella_corrente))
path=os.path.join(path_cartella_src, 'templates')
templates=Jinja2Templates(directory=path)
SERVICE_SERVER_URL="http://server_esonero:8003"

def get_response(url:str)->requests.models.Response:
    try:
        response=requests.get(f"{SERVICE_SERVER_URL}/{url}")
        response.raise_for_status()
        response=response.json()
    except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Errore di comunicazione con l'API al link {SERVICE_SERVER_URL}/{url}\nErrore:{e}")
    return response

@app.get("/")
def landing_page(request:Request):
    data_response=get_response("")
    return templates.TemplateResponse("index.html",{"request":request, "response":data_response})

@app.get("/schema_summary")
def schema_summary(request:Request):
     schema=get_response("/schema_summary")
     return templates.TemplateResponse("schema_summary.html",{"request":request, "schema_summary":schema})

@app.get("/search/{query}")
def search(request:Request, query):
    try:
        response=requests.get(f"{SERVICE_SERVER_URL}/search/{query}")
        response.raise_for_status()
        messaggio=response.json()
    except requests.RequestException as e:
        try:#provo a prendere il messaggio di errore del backend
            error = e.response.json()
            # in caso l'errore sia una str
            if isinstance(error.get("detail"), str):
                messaggio = error["detail"]
            elif isinstance(error.get("detail"), list):
            # in caso l'errore sia una list
                messaggio = "; ".join(str(item) for item in error["detail"])
        except Exception:
            messaggio = f"Errore di comunicazione con l'API al link {SERVICE_SERVER_URL}/search/{query}\nErrore:{e}"
    
    if not isinstance(messaggio, list):
        messaggio=[{"item_type":"error", 'properties': messaggio}]#passo l'errore in modo tale che jinja2 possa leggerlo
    return templates.TemplateResponse("search.html",{"request":request, "result":messaggio})

class AddItem(BaseModel):
    name: str
    value: int

@app.post("/add")
async def add(request:Request, richiesta:str =Form(default=...)):
    try:
        payload ={"data_line":richiesta}  
        response=requests.post(f"{SERVICE_SERVER_URL}/add",json=payload)
        response.raise_for_status()
        result=response.json()
        add_result={"status":"success","data":result}

    except requests.exceptions.HTTPError as e:
        messaggio = "Errore sconosciuto"
        try:#provo a prendere il messaggio di errore del backend
            error = e.response.json()
            # in caso l'errore sia una str
            if isinstance(error.get("detail"), str):
                messaggio = error["detail"]
            elif isinstance(error.get("detail"), list):
                # in caso l'errore sia una list
                messaggio = "; ".join(str(item) for item in error["detail"])
        except Exception:
            messaggio = str(e)
        add_result = {"status": "error", "message": messaggio}
    except Exception as e:
        add_result = {"status": "error", "message": str(e)}
    return templates.TemplateResponse("add.html", {"request": request, "result": add_result})
