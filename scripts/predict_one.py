# scripts/predict_one.py

def predict_one_match(home: str, away: str) -> dict:
    """
    Fonction simple pour prédire un match entre deux équipes.
    Pour l'instant, c'est une version "fake" qui renvoie juste un message.
    On branchera le vrai modèle (model_1x2.pkl) plus tard.
    """
    return {
        "status": "ok",
        "home": home,
        "away": away,
        "prediction": "TODO_brancher_modele",
        "comment": "Fonction predict_one_match exécutée depuis scripts/predict_one.py."
    } 