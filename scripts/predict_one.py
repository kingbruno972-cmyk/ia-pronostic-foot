import numpy as np
import pandas as pd
import joblib
from pathlib import Path

# -------------------------------------------------------
# Chargement du modèle 1X2 et des colonnes de features
# -------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]  # dossier racine du projet
MODEL_PATH = ROOT / "models" / "model_1x2.pkl"
COLUMNS_PATH = ROOT / "models" / "feature_columns.pkl"

# On charge une seule fois au démarrage
try:
    MODEL_1X2 = joblib.load(MODEL_PATH)
    FEATURE_COLUMNS = joblib.load(COLUMNS_PATH)
except Exception as e:
    # Si ça plante au chargement, on le verra dans les logs Render
    MODEL_1X2 = None
    FEATURE_COLUMNS = None
    print(f"[predict_one] Erreur de chargement du modèle: {e}")


# -------------------------------------------------------
# Construction d'une ligne de features pour UN match
# (version simple : tout à 0 + one-hot des équipes si dispo)
# -------------------------------------------------------

def make_feature_row(home: str, away: str) -> pd.DataFrame:
    """
    Crée un DataFrame avec exactement les mêmes colonnes que
    lors de l'entraînement (FEATURE_COLUMNS).

    Ici on fait une version minimale :
      - toutes les features à 0
      - si des colonnes one-hot existent pour les équipes,
        on les met à 1 (ex: 'home_team_PSG', 'away_team_Marseille').

    C'est un vrai passage dans le modèle, mais avec des features
    très simples. Tu pourras enrichir plus tard.
    """
    if FEATURE_COLUMNS is None:
        raise RuntimeError("FEATURE_COLUMNS non chargé")

    # 1 ligne, toutes les colonnes = 0
    row = pd.DataFrame([[0] * len(FEATURE_COLUMNS)], columns=FEATURE_COLUMNS)

    # Tentative de one-hot sur les noms d'équipes
    home_col = f"home_team_{home}"
    away_col = f"away_team_{away}"

    if home_col in row.columns:
        row.loc[0, home_col] = 1

    if away_col in row.columns:
        row.loc[0, away_col] = 1

    # Si le modèle a des colonnes "is_home" / "is_away" etc.
    for col, val in {
        "is_home": 1,
        "is_away": 0,
    }.items():
        if col in row.columns:
            row.loc[0, col] = val

    return row


# -------------------------------------------------------
# Fonction appelée par l'API FastAPI (api/main.py)
# -------------------------------------------------------

def predict_one_match(home: str, away: str) -> dict:
    """
    Utilise le modèle 1X2 entraîné pour prédire un match.

    Retourne un dict avec :
      - prediction : texte lisible
      - p_home, p_draw, p_away : probabilités
      - comment : texte détaillé
    """
    if MODEL_1X2 is None:
        return {
            "prediction": "ERREUR_MODELE",
            "p_home": 0.33,
            "p_draw": 0.33,
            "p_away": 0.33,
            "comment": "Impossible de charger le modèle sur le serveur.",
        }

    # Construire la ligne de features
    X = make_feature_row(home, away)

    # Passe dans le modèle
    proba = MODEL_1X2.predict_proba(X)[0]  # [p_home, p_draw, p_away] en général
    classes = getattr(MODEL_1X2, "classes_", np.array([0, 1, 2]))

    # On suppose que les classes sont dans l'ordre [0,1,2] = [home, draw, away]
    # ou ["H","D","A"], etc. On crée une petite table de mapping.
    label_map = {
        "H": "home",
        "D": "draw",
        "A": "away",
        0: "home",
        1: "draw",
        2: "away",
    }

    best_idx = int(np.argmax(proba))
    best_label = classes[best_idx]
    outcome = label_map.get(best_label, "home")

    if outcome == "home":
        prediction_text = f"Victoire de {home}"
    elif outcome == "away":
        prediction_text = f"Victoire de {away}"
    else:
        prediction_text = "Match nul"

    comment = (
        "Prono issu du modèle 1X2 (clubs) : "
        f"p_home={proba[0]:.3f}, p_draw={proba[1]:.3f}, p_away={proba[2]:.3f}. "
        f"Issue la plus probable : {prediction_text}"
    )

    return {
        "prediction": prediction_text,
        "p_home": float(proba[0]),
        "p_draw": float(proba[1]),
        "p_away": float(proba[2]),
        "comment": comment,
    }


# Petit test local (optionnel)
if __name__ == "__main__":
    print(predict_one_match("PSG", "Marseille"))