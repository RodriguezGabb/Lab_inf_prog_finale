from typing import List
from pydantic import BaseModel
import requests
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
import os

app= FastAPI()
path_folder = os.path.dirname(os.path.abspath(__file__))
path_folder_src=os.path.dirname(os.path.dirname(path_folder))
path=os.path.join(path_folder_src, 'templates')
templates=Jinja2Templates(directory=path)
SERVICE_SERVER_URL="http://server_esame:8003"

def get_response(url:str)->requests.models.Response:
    try:
        response=requests.get(f"{SERVICE_SERVER_URL}/{url}")
        response.raise_for_status()
        response=response.json()
    except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"error with the comunication with the api at the link {SERVICE_SERVER_URL}/{url}\nError:{e}")
    return response

@app.get("/")
def landing_page(request:Request):
    data_response=get_response("")
    return templates.TemplateResponse("index.html",{"request":request, "response":data_response})

@app.get("/schema_summary")
def schema_summary(request:Request):
     schema=get_response("/schema_summary")
     return templates.TemplateResponse("schema_summary.html",{"request":request, "schema_summary":schema})

@app.post("/search")
async def search(request:Request, data_line:str =Form(default=...)):
    '''search to ai'''
    try:
        payload={"question":data_line}
        response=requests.post(f"{SERVICE_SERVER_URL}/search", json=payload)
        response.raise_for_status()
        message=response.json()
    except requests.RequestException as e:
        message = f"error with the comunication with API at the link {SERVICE_SERVER_URL}/search \n with question {data_line}\nError:{e}"
    if not isinstance(message, dict):
        message=[{"item_type":"error", 'properties': message}]#error in a way that jinja can read it
    return templates.TemplateResponse("search.html",{"request":request, "result":message})

@app.post("/sql_search")
async def sql_search(request:Request, data_line:str =Form(default=...)):
    '''search sql'''
    try:
        payload={"sql_query":data_line}
        response=requests.post(f"{SERVICE_SERVER_URL}/sql_search", json=payload)
        response.raise_for_status()
        message=response.json()
    except requests.RequestException as e:
        message = f"error with the comunication with API at the link {SERVICE_SERVER_URL}/search \n with the folowing querry {data_line}\nError:{e}"
    return templates.TemplateResponse("sql_search.html",{"request":request, "result":message})

@app.post("/add")
async def add(request:Request, data_line:str =Form(default=...)):
    try:
        payload ={"data_line":data_line}  
        response=requests.post(f"{SERVICE_SERVER_URL}/add",json=payload)
        response.raise_for_status()
        result=response.json()
        add_result={"status":"success","data":result}

    except requests.exceptions.HTTPError as e:
        message = "unknown error"
        try:# try to get the error message from the backend
            error = e.response.json()
            # if error is a str
            if isinstance(error.get("detail"), str):
                message = error["detail"]
            elif isinstance(error.get("detail"), list):
                # if error is a list
                message = "; ".join(str(item) for item in error["detail"])
        except Exception:
            message = str(e)
        add_result = {"status": "error", "message": message}
    except Exception as e:
        add_result = {"status": "error", "message": str(e)}
    return templates.TemplateResponse("add.html", {"request": request, "result": add_result})
