from __future__ import annotations
from pathlib import Path
from datetime import date
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from portes_sports.mlb import get_schedule
from portes_sports.nba import get_scoreboard
from portes_sports.scoring import viral_score
from portes_sports.scriptwriter import generate_script
from portes_sports.video import render_video
from portes_sports.tiktok import configured as tiktok_configured

st.set_page_config(page_title="PORTES AI SPORTS", page_icon="🏆", layout="wide")

st.title("🏆 PORTES AI SPORTS")
st.write("Busca temas deportivos, genera un video vertical y prepáralo para publicar.")

if "stories" not in st.session_state:
    st.session_state.stories = []
if "selected" not in st.session_state:
    st.session_state.selected = None
if "script" not in st.session_state:
    st.session_state.script = None
if "video_path" not in st.session_state:
    st.session_state.video_path = None

c1, c2, c3 = st.columns(3)
with c1:
    league = st.selectbox("Liga", ["MLB", "NBA"])
with c2:
    selected_day = st.date_input("Fecha", value=date.today())
with c3:
    st.write("")
    st.write("")
    search = st.button("🔎 Buscar videos virales", use_container_width=True)

if search:
    try:
        raw = get_schedule(selected_day.isoformat()) if league == "MLB" else get_scoreboard(selected_day.isoformat())
        ranked = []
        for item in raw:
            v = viral_score(item["headline"], item["summary"], 2, 7, 8)
            item["viral"] = v
            ranked.append(item)
        st.session_state.stories = sorted(ranked, key=lambda x: x["viral"]["score"], reverse=True)
        if not ranked:
            st.warning("No se encontraron juegos para esa fecha. Usa la entrada manual más abajo.")
    except Exception as e:
        st.error(f"No se pudo consultar la fuente deportiva: {e}")

st.subheader("Mejores oportunidades")
for i, story in enumerate(st.session_state.stories[:5]):
    with st.container(border=True):
        a, b, c = st.columns([5, 1, 1])
        with a:
            st.markdown(f"### {story['headline']}")
            st.write(story["summary"])
        with b:
            st.metric("Potencial", f"{story['viral']['score']}/100")
        with c:
            if st.button("Elegir", key=f"pick_{i}", use_container_width=True):
                st.session_state.selected = story
                st.session_state.script = generate_script(
                    story.get("league", league),
                    story["headline"],
                    story["summary"],
                    story["viral"]["score"]
                )

st.divider()
st.subheader("Entrada manual")
manual_headline = st.text_input("Titular", placeholder="Ej.: Jonrón decisivo en la novena entrada")
manual_summary = st.text_area("Datos confirmados", placeholder="Escribe únicamente hechos comprobados.")
if st.button("Usar historia manual") and manual_headline and manual_summary:
    story = {
        "league": league,
        "headline": manual_headline,
        "summary": manual_summary,
        "viral": viral_score(manual_headline, manual_summary, 1, 7, 8)
    }
    st.session_state.selected = story
    st.session_state.script = generate_script(
        league, manual_headline, manual_summary, story["viral"]["score"]
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
        out = Path("outputs") / "portes_ai_sports_web.mp4"
        render_video(s, out, 18)
        st.session_state.video_path = str(out)

if st.session_state.video_path and Path(st.session_state.video_path).exists():
    st.divider()
    st.subheader("Video listo")
    st.video(st.session_state.video_path)
    with open(st.session_state.video_path, "rb") as f:
        st.download_button(
            "⬇️ Descargar video",
            f,
            file_name="portes_ai_sports.mp4",
            mime="video/mp4",
            use_container_width=True
        )

    if tiktok_configured():
        st.success("TikTok está configurado. La publicación automática se habilita después de validar permisos.")
        st.button("📤 Publicar", use_container_width=True, disabled=True)
    else:
        st.warning("TikTok todavía no está vinculado. Por seguridad, publica manualmente hasta completar OAuth.")
        st.button("📤 Publicar", use_container_width=True, disabled=True)
