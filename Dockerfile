FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# On utilise le port 8000 dans le conteneur
EXPOSE 8000

# On lance uvicorn sur api.main:app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]