FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway donne un port dynamique, mais on expose 8000 quand même
EXPOSE 8000

# LA SEULE COMMANDE QUI FONCTIONNE SUR RAILWAY
CMD sh -c "uvicorn api.main:app --host 0.0.0.0 --port $PORT"