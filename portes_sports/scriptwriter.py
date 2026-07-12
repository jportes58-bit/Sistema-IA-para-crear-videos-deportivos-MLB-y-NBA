from __future__ import annotations
import json
import os
from dotenv import load_dotenv

load_dotenv()

HOOKS = {
    "MLB": "¡Atención! Esta jugada acaba de sacudir las Grandes Ligas.",
    "NBA": "¡La NBA acaba de vivir un momento increíble!",
    "LIDOM": "¡La pelota invernal dominicana está encendida!",
    "NFL": "¡La NFL acaba de cambiar en una sola jugada!",
    "FUTBOL": "¡Este momento del fútbol está dando la vuelta al mundo!",
    "UFC": "¡El octágono explotó con este momento!",
    "TENIS": "¡Este punto cambió por completo el partido!",
}

def local_script(sport: str, headline: str, summary: str) -> dict:
    hook = HOOKS.get(sport, "¡Este momento deportivo está dando de qué hablar!")
    body = (
        f"{headline}. {summary} "
        "La clave estuvo en cómo cambió el ritmo, la presión y la reacción de los protagonistas."
    )
    close = "¿Tú qué opinas? Comenta y síguenos para más contenido deportivo."
    return {
        "hook": hook,
        "body": body,
        "close": close,
        "title": f"🔥 {headline}",
        "caption": f"{headline}. ¿Fue el momento del día?",
        "hashtags": [sport, "Deportes", "SportsTok", "Viral", "PortesAISports"],
    }

def generate_script(
    sport: str,
    headline: str,
    summary: str,
    score: int,
) -> dict:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return local_script(sport, headline, summary)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""
Crea un guion factual en español para un video vertical de 25 a 32 segundos.
Deporte: {sport}
Titular: {headline}
Datos confirmados: {summary}
Puntuación de interés: {score}/100

No inventes estadísticas. Devuelve JSON con:
hook, body, close, title, caption y hashtags.
"""
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=prompt,
            text={"format": {"type": "json_object"}},
        )
        return json.loads(response.output_text)
    except Exception:
        return local_script(sport, headline, summary)
