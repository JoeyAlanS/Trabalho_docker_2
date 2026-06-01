FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn networkx matplotlib pydantic locust

COPY . .

EXPOSE 8000 8089

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]