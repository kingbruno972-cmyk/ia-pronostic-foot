from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO

app = FastAPI(
    title="IA Pronostic Foot",
    version="1.0.0"
)


@app.get("/")
def home():
    """
    Endpoint de santé simple pour vérifier que l'API tourne.
    """
    return {
        "status": "ok",
        "message": "API pronostic foot en ligne 🔥"
    }


@app.post("/predict_fixtures")
async def predict_fixtures(file: UploadFile = File(...)):
    """
    Reçoit un fichier CSV de fixtures et renvoie (pour l'instant)
    un résultat de test.

    ⚠️ C'est ici que tu brancheras ton vrai code de prédiction
    (features + modèle) quand on l'aura recopié depuis
    fixtures/predict_fixtures.py.
    """
    # 1) Vérifier le type de fichier
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être un CSV (.csv)."
        )

    try:
        # 2) Lire le CSV en mémoire
        raw_bytes = await file.read()
        df = pd.read_csv(BytesIO(raw_bytes))

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Impossible de lire le CSV : {e}"
        )

    # 👉 👉 👉
    # ICI on branchera ton vrai pipeline :
    #   - construire les features
    #   - charger le modèle
    #   - prédire
    #
    # Pour l’instant, on renvoie juste un résultat de test
    # pour vérifier que l’endpoint fonctionne bien.
    # 👇👇👇

    nb_matchs = len(df)

    return JSONResponse(
        {
            "status": "ok",
            "info": "Endpoint /predict_fixtures opérationnel ✅ "
                    "(pipeline ML à brancher ensuite).",
            "nb_matchs_dans_csv": nb_matchs,
            "columns": list(df.columns)
        }
    )