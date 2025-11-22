# scripts/predict_one.py

from typing import Dict

def predict_one_match(home: str, away: str) -> Dict[str, str]:
    """
    Fonction appelée par l'API /predict_one.
    Pour l'instant, c'est un mock (pas de vrai modèle).
    """

    return {
        "status": "ok",
        "home": home,
        "away": away,
        "prediction": "TODO_brancher_modele",
        "comment": "Fonction predict_one_match exécutée depuis scripts/predict_one.py."
    }