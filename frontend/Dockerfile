FROM python:3.9-slim

WORKDIR /app

COPY src /app/src

ADD templates /app/templates

COPY requirements.txt .

RUN pip install -r requirements.txt


EXPOSE 8001

CMD [ "uvicorn", "src.frontend.frontend:app", "--host", "0.0.0.0", "--port", "8001" ]