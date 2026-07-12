from pathlib import Path
from datetime import date
import json
import streamlit as st

from portes_sports.providers.registry import fetch_sport
from portes_sports.scoring import viral_score
from portes_sports.scriptwriter import generate_script
from portes_sports.video import render_video

st.set_page_config(page_title="PORTES AI SPORTS PRO", page_icon="🏆", layout="wide")
st.title("🏆 PORTES AI SPORTS PRO")
st.caption("MLB · NBA · LIDOM · NFL · Fútbol · UFC · Tenis")

CONFIG_PATH = Path("sports_config.json")
config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

with st.sidebar:
    st.header("Deportes")
    sport = st.selectbox("Selecciona", list(config.keys()))
    enabled = st.toggle("Módulo activo", value=config[sport]["enabled"])
    if enabled != config[sport]["enabled"]:
        config[sport]["enabled"] = enabled
        CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        st.success("Configuración actualizada")
    st.caption(f"Proveedor: {config[sport]['provider']}")

for key, default in {
    "stories": [], "selected_story": None, "script": None, "video": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if not config[sport]["enabled"]:
    st.warning(f"El módulo {sport} está preparado, pero desactivado. Actívalo en la barra lateral.")
else:
    c1, c2, c3 = st.columns(3)
    with c1:
        chosen_date = st.date_input("Fecha", value=date.today())
    with c2:
        star_power = st.slider("Figuras involucradas", 1, 10, 6)
    with c3:
        visual_strength = st.slider("Fuerza visual", 1, 10, 7)

    if st.button("🔎 Buscar oportunidades", use_container_width=True):
        try:
            stories = fetch_sport(sport, chosen_date.isoformat())
            for item in stories:
                item["viral"] = viral_score(
                    item["headline"], item["summary"], 2, star_power, visual_strength
                )
            st.session_state.stories = sorted(
                stories, key=lambda x: x["viral"]["score"], reverse=True
            )
            if not stories:
                st.info("Este deporte usa entrada manual hasta conectar una fuente automática.")
        except Exception as exc:
            st.error(f"No se pudo consultar la fuente: {exc}")

    for i, story in enumerate(st.session_state.stories[:5]):
        with st.container(border=True):
            a, b, c = st.columns([5, 1, 1])
            with a:
                st.subheader(story["headline"])
                st.write(story["summary"])
            with b:
                st.metric("Interés", f"{story['viral']['score']}/100")
            with c:
                if st.button("Elegir", key=f"choose_{i}"):
                    st.session_state.selected_story = story
                    st.session_state.script = generate_script(
                        sport, story["headline"], story["summary"], story["viral"]["score"]
                    )

    st.divider()
    st.subheader("Entrada manual")
    headline = st.text_input("Titular o jugada")
    summary = st.text_area("Datos confirmados")
    if st.button("Usar historia manual") and headline and summary:
        result = viral_score(headline, summary, 1, star_power, visual_strength)
        story = {"headline": headline, "summary": summary, "viral": result}
        st.session_state.selected_story = story
        st.session_state.script = generate_script(
            sport, headline, summary, result["score"]
        )

    if st.session_state.script:
        st.divider()
        st.subheader("Guion")
        s = st.session_state.script
        s["hook"] = st.text_area("Hook", s["hook"])
        s["body"] = st.text_area("Cuerpo", s["body"], height=150)
        s["close"] = st.text_area("Cierre", s["close"])
        s["title"] = st.text_input("Título", s["title"])
        s["caption"] = st.text_area("Descripción", s["caption"])
        s["full"] = f"{s['hook']} {s['body']} {s['close']}"
        st.session_state.script = s

        if st.button("🎬 Crear video", use_container_width=True):
            out = Path("outputs") / f"portes_{sport.lower()}_video.mp4"
            render_video(s, out, 18)
            st.session_state.video = str(out)

    if st.session_state.video and Path(st.session_state.video).exists():
        st.video(st.session_state.video)
        with open(st.session_state.video, "rb") as f:
            st.download_button(
                "⬇️ Descargar MP4", f,
                file_name=Path(st.session_state.video).name,
                mime="video/mp4", use_container_width=True
            )
        st.button("📤 Publicar", disabled=True, use_container_width=True)
        st.caption("Se habilitará después de conectar TikTok mediante OAuth.")
