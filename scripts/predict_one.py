# scripts/predict_one.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass
class PredictResult:
    """
    Structure de sortie standard pour /predict_one.
    """
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


def _probs_from_odds(
    odds_home: float,
    odds_draw: float,
    odds_away: float,
) -> Tuple[float, float, float]:
    """
    Convertit des cotes 1X2 en probabilités en corrigeant la marge du bookmaker.

    Exemple :
        1.15 / 7.20 / 14.0  → p_home ≈ 0.80, p_draw ≈ 0.13, p_away ≈ 0.07
    """
    inv_home = 1.0 / odds_home
    inv_draw = 1.0 / odds_draw
    inv_away = 1.0 / odds_away

    total = inv_home + inv_draw + inv_away
    if total <= 0:
        # Cas ultra improbable, mais on protège:
        return 1.0 / 3, 1.0 / 3, 1.0 / 3

    p_home = inv_home / total
    p_draw = inv_draw / total
    p_away = inv_away / total
    return p_home, p_draw, p_away


def predict_one_match(
    home: str,
    away: str,
    odds_home: Optional[float] = None,
    odds_draw: Optional[float] = None,
    odds_away: Optional[float] = None,
) -> Dict:
    """
    Prono 1X2 pour un match unique.

    - Si les cotes 1X2 (odds_home / odds_draw / odds_away) sont fournies ET > 1.0,
      on calcule des probabilités réalistes à partir des cotes.
    - Sinon, on utilise un fallback (démo) pour que tout fonctionne quand même.

    Cette fonction est appelée par l’endpoint FastAPI /predict_one.
    """

    # ==============================
    # 1) Si les cotes sont fournies
    # ==============================
    use_odds = (
        odds_home is not None
        and odds_draw is not None
        and odds_away is not None
        and odds_home > 1.0
        and odds_draw > 1.0
        and odds_away > 1.0
    )

    if use_odds:
        p_home, p_draw, p_away = _probs_from_odds(
            odds_home=odds_home,
            odds_draw=odds_draw,
            odds_away=odds_away,
        )
        source = (
            "Probabilités calculées à partir des cotes 1X2 "
            f"(home={odds_home}, draw={odds_draw}, away={odds_away})."
        )
    else:
        # =========================================
        # 2) Fallback si pas de cotes (mode démo)
        # =========================================
        p_home, p_draw, p_away = 0.30, 0.20, 0.50
        source = (
            "Probabilités de démo (aucune cote valide fournie). "
            "À remplacer par de vraies cotes ou un modèle IA."
        )

    # ==========================
    # 3) Issue la plus probable
    # ==========================
    if p_home >= p_draw and p_home >= p_away:
        prediction = f"Victoire de {home}"
    elif p_away >= p_home and p_away >= p_draw:
        prediction = f"Victoire de {away}"
    else:
        prediction = "Match nul"

    comment = (
        f"{source} "
        f"p_home={p_home:.3f}, p_draw={p_draw:.3f}, p_away={p_away:.3f}. "
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