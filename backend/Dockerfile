FROM python:3.9-slim

WORKDIR /app

ADD src /app/src

COPY requirements.txt .

RUN pip install --upgrade pip
#installamento e aggiornamento di quello che serve per far funzionare mariadb
RUN apt-get update && apt-get install -y gcc libmariadb-dev default-libmysqlclient-dev build-essential curl

#rimmozione di tutto ciò che è in eccesso 
RUN rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt



EXPOSE 8003


#CMD [ "python","/app/src/backend/init_tables.py","&&","uvicorn", "src.backend.backend:app", "--host", "0.0.0.0", "--port", "8003"]
CMD ["uvicorn", "src.backend.backend:app", "--host", "0.0.0.0", "--port", "8003"]
