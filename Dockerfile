FROM python:3.11-slim

WORKDIR /app

# 1. Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copier tout le code
COPY . .

# 3. Railway fournit la variable d'environnement PORT
#    - En local : PORT n'existe pas → on utilise 8000
#    - Sur Railway : PORT est défini → uvicorn écoute dessus
EXPOSE 8000
CMD sh -c "uvicorn api.main:app --host 0.0.0.0 --port \${PORT:-8000}"