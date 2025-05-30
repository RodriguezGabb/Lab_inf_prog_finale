FROM python:3.9-slim

WORKDIR /app

ADD src /app/src

COPY requirements.txt .

RUN pip install --upgrade pip
#installing and updating for mariadb
RUN apt-get update && apt-get install -y gcc libmariadb-dev default-libmysqlclient-dev build-essential curl

#removes extra packages
RUN rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt



EXPOSE 8003


CMD ["uvicorn", "src.backend.backend:app", "--host", "0.0.0.0", "--port", "8003"]
