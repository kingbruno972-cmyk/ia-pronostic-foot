# api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scripts.predict_one import predict_one_match

app = FastAPI(
    title="IA Prono Foot",
    version="1.0.0",
)

# CORS pour que n’importe quel client (y compris ton iPhone) puisse appeler l’API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # si tu veux, on pourra restreindre plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    """
    Route de test simple : Render + iPhone peuvent vérifier que l’API est en ligne.
    """
    return {"status": "online", "message": "API pronostic foot OK"}


@app.get("/predict_one")
def predict_one(home: str, away: str):
    """
    Route utilisée par ton app iPhone :
    GET /predict_one?home=PSG&away=Marseille
    """
    result = predict_one_match(home=home, away=away)
    # FastAPI renvoie automatiquement du JSON UTF-8 correct
    return result