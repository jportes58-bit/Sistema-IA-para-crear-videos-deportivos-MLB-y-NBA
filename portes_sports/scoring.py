from __future__ import annotations
import re

KEYWORDS = {
    "récord": 12,
    "histor": 11,
    "remont": 10,
    "último segundo": 12,
    "walk-off": 12,
    "grand slam": 11,
    "jonrón": 8,
    "triple-doble": 9,
    "nocaut": 12,
    "knockout": 12,
    "sumisión": 10,
    "título": 8,
    "golazo": 10,
    "hat-trick": 11,
    "penal": 7,
    "tie-break": 8,
    "match point": 10,
    "sorpresa": 7,
    "lesión": 8,
    "controvers": 8,
    "expuls": 8,
    "debut": 6,
    "racha": 6,
}

def viral_score(
    headline: str,
    summary: str,
    star_power: int = 6,
    visual_strength: int = 7,
) -> dict:
    text = f"{headline} {summary}".lower()
    score = 25
    reasons: list[str] = []

    for word, points in KEYWORDS.items():
        if word in text:
            score += points
            reasons.append(f"Tema fuerte: {word}")

    score += min(20, max(0, star_power) * 2)
    score += min(20, max(0, visual_strength) * 2)

    if re.search(r"\b\d{2,3}\b", text):
        score += 5
        reasons.append("Incluye una cifra llamativa")

    return {
        "score": min(100, score),
        "reasons": reasons or ["Tema deportivo oportuno"],
    }
