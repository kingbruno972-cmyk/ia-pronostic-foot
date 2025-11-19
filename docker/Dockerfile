FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# On expose 8000, mais Railway va utiliser son propre PORT en interne.
EXPOSE 8000

# Railway fournit automatiquement la variable $PORT → on l'utilise ici
CMD sh -c "uvicorn api.main:app --host 0.0.0.0 --port ${PORT}"