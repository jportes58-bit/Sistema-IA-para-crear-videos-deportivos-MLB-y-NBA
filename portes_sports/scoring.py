from __future__ import annotations
import re

POWER_WORDS = {
    "récord": 12, "histor": 11, "remont": 10, "último segundo": 12,
    "walk-off": 12, "grand slam": 11, "jonrón": 8, "triple-doble": 9,
    "expuls": 8, "lesión": 8, "sorpresa": 7, "increíble": 7,
    "debut": 6, "racha": 6, "controvers": 8, "viral": 5, "mvp": 6
}

def viral_score(headline: str, summary: str, recency_hours: float = 2.0,
                star_power: int = 5, visual_strength: int = 5) -> dict:
    text = f"{headline} {summary}".lower()
    score = 20
    reasons = []
    for word, value in POWER_WORDS.items():
        if word in text:
            score += value
            reasons.append(f"Palabra/tema fuerte: {word}")
    score += max(0, min(20, int((24 - min(recency_hours, 24)) / 24 * 20)))
    score += max(0, min(15, star_power * 2))
    score += max(0, min(15, visual_strength * 2))
    if re.search(r"\b\d{2,3}\b", text):
        score += 5
        reasons.append("Incluye una cifra llamativa")
    return {"score": min(100, score), "reasons": reasons or ["Tema deportivo oportuno"]}
