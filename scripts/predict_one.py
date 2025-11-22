# scripts/predict_one.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PredictResult:
    prediction: str
    p_home: float
    p_draw: float
    p_away: float
    comment: str
    status: str = "ok"

    def to_dict(self) -> Dict:
        return {
            "prediction": self.prediction,
            "p_home": self.p_home,
            "p_draw": self.p_draw,
            "p_away": self.p_away,
            "comment": self.comment,
            "status": self.status,
        }


def predict_one_match(home: str, away: str) -> Dict:
    """
    Version simple (démo) pour que l’appli iPhone fonctionne.
    Tu auras VRAIMENT p_home, p_draw, p_away dans le JSON.
    Ensuite on branchera ton vrai modèle si tu veux.
    """

    # 👉 Ici tu peux à terme utiliser ton vrai modèle (model_1x2.pkl + features)
    # Pour l’instant : pseudo-prono pour que tout le pipeline fonctionne.

    # Exemple simple : on donne 50% à l’extérieur (team away), 30% au home, 20% au nul
    p_home = 0.30
    p_draw = 0.20
    p_away = 0.50

    # On choisit l’issue la plus probable
    if p_home >= p_draw and p_home >= p_away:
        prediction = f"Victoire de {home}"
    elif p_away >= p_home and p_away >= p_draw:
        prediction = f"Victoire de {away}"
    else:
        prediction = "Match nul"

    comment = (
        f"Prono calculé (démo) : p_home={p_home:.3f}, "
        f"p_draw={p_draw:.3f}, p_away={p_away:.3f}. "
        f"Issue la plus probable : {prediction}"
    )

    res = PredictResult(
        prediction=prediction,
        p_home=p_home,
        p_draw=p_draw,
        p_away=p_away,
        comment=comment,
    )
    return res.to_dict()