from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

def local_script(league: str, headline: str, summary: str) -> dict:
    hook = f"¡Atención! Esto acaba de sacudir la {league}."
    body = (
        f"{headline}. {summary} "
        "La clave no fue solamente el resultado: fue la manera en que cambió el momento del juego. "
        "Los fanáticos ya están debatiendo si esta fue la jugada más impactante de la jornada."
    )
    close = "¿Tú qué opinas? Comenta y síguenos para más MLB y NBA."
    return {
        "hook": hook,
        "body": body,
        "close": close,
        "full": f"{hook} {body} {close}",
        "title": f"🔥 {headline}: la jugada que todos comentan",
        "caption": f"{headline}. ¿Fue la jugada del día?",
        "hashtags": ["MLB" if league == "MLB" else "NBA", "Deportes", "SportsTok", "Viral", "PortesAISports"]
    }

def generate_script(league: str, headline: str, summary: str, score: int) -> dict:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return local_script(league, headline, summary)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        prompt = f"""Crea un guion factual en español dominicano neutral para un video vertical de 25-32 segundos.
Liga: {league}
Titular: {headline}
Datos confirmados: {summary}
Puntuación de interés: {score}/100
No inventes estadísticas. Estructura: hook de 2 segundos, cuerpo, cierre con pregunta.
Devuelve JSON con hook, body, close, full, title, caption, hashtags (lista)."""
        response = client.responses.create(
            model=model,
            input=prompt,
            text={"format": {"type": "json_object"}}
        )
        import json
        return json.loads(response.output_text)
    except Exception:
        return local_script(league, headline, summary)
