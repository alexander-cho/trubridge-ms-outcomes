FROM python:3.14

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY analytics analytics
COPY data data
COPY models models
COPY schemas schemas
COPY main.py ./
COPY .env ./

EXPOSE 8030

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]