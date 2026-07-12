from __future__ import annotations
from datetime import date
from pathlib import Path
import json
import streamlit as st

from portes_sports.providers.registry import fetch_sport
from portes_sports.scoring import viral_score
from portes_sports.scriptwriter import generate_script
from portes_sports.video import render_video
from portes_sports.tiktok import publication_status

st.set_page_config(
    page_title="PORTES AI SPORTS PRO",
    page_icon="🏆",
    layout="wide",
)

st.title("🏆 PORTES AI SPORTS PRO")
st.caption("MLB · NBA · LIDOM · NFL · Fútbol · UFC · Tenis")

CONFIG_PATH = Path("sports_config.json")
config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

defaults = {
    "stories": [],
    "selected_story": None,
    "script": None,
    "video_path": None,
    "current_sport": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

with st.sidebar:
    st.header("Configuración")
    sport = st.selectbox(
        "Deporte",
        list(config.keys()),
        format_func=lambda name: f"{config[name]['icon']} {name}",
    )

    if st.session_state.current_sport != sport:
        st.session_state.current_sport = sport
        st.session_state.stories = []
        st.session_state.selected_story = None
        st.session_state.script = None
        st.session_state.video_path = None

    enabled = st.toggle(
        "Módulo activo",
        value=bool(config[sport]["enabled"]),
    )
    if enabled != config[sport]["enabled"]:
        config[sport]["enabled"] = enabled
        CONFIG_PATH.write_text(
            json.dumps(config, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        st.success("Configuración actualizada")

    st.caption(f"Fuente: `{config[sport]['provider']}`")
    st.caption(publication_status())

if not config[sport]["enabled"]:
    st.warning(
        f"El módulo {sport} está preparado, pero está desactivado. "
        "Actívalo desde la barra lateral."
    )
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    chosen_date = st.date_input("Fecha", value=date.today())
with col2:
    star_power = st.slider("Importancia de los protagonistas", 1, 10, 6)
with col3:
    visual_strength = st.slider("Fuerza visual del momento", 1, 10, 7)

if st.button("🔎 Buscar oportunidades", use_container_width=True):
    try:
        stories = fetch_sport(
            config[sport]["provider"],
            chosen_date.isoformat(),
        )
        for story in stories:
            story["viral"] = viral_score(
                story["headline"],
                story["summary"],
                star_power,
                visual_strength,
            )
        st.session_state.stories = sorted(
            stories,
            key=lambda item: item["viral"]["score"],
            reverse=True,
        )
        if not stories:
            st.info(
                "Este deporte utiliza entrada manual hasta conectar "
                "una fuente automática."
            )
    except Exception as exc:
        st.error(f"No se pudo consultar la fuente: {exc}")

st.subheader("Oportunidades encontradas")
for index, story in enumerate(st.session_state.stories[:5]):
    with st.container(border=True):
        left, middle, right = st.columns([5, 1, 1])
        with left:
            st.markdown(f"### {story['headline']}")
            st.write(story["summary"])
            st.caption(story.get("source", "Fuente deportiva"))
        with middle:
            st.metric("Interés", f"{story['viral']['score']}/100")
        with right:
            if st.button("Elegir", key=f"choose_{index}"):
                st.session_state.selected_story = story
                st.session_state.script = generate_script(
                    sport,
                    story["headline"],
                    story["summary"],
                    story["viral"]["score"],
                )

st.divider()
st.subheader("Entrada manual")
headline = st.text_input(
    "Titular o jugada",
    placeholder="Ej.: Remontada histórica en el último minuto",
)
summary = st.text_area(
    "Datos confirmados",
    placeholder="Escribe únicamente hechos comprobados.",
)

if st.button("Usar historia manual") and headline.strip() and summary.strip():
    result = viral_score(
        headline,
        summary,
        star_power,
        visual_strength,
    )
    story = {
        "sport": sport,
        "headline": headline,
        "summary": summary,
        "source": "Entrada manual",
        "viral": result,
    }
    st.session_state.selected_story = story
    st.session_state.script = generate_script(
        sport,
        headline,
        summary,
        result["score"],
    )

if st.session_state.script:
    st.divider()
    st.subheader("Guion y publicación")

    script = st.session_state.script
    script["hook"] = st.text_area("Hook", script["hook"])
    script["body"] = st.text_area("Cuerpo", script["body"], height=150)
    script["close"] = st.text_area("Cierre", script["close"])
    script["title"] = st.text_input("Título", script["title"])
    script["caption"] = st.text_area("Descripción", script["caption"])

    hashtags_text = st.text_input(
        "Hashtags",
        " ".join(f"#{tag.lstrip('#')}" for tag in script["hashtags"]),
    )
    script["hashtags"] = [
        item.lstrip("#")
        for item in hashtags_text.split()
        if item.strip()
    ]
    st.session_state.script = script

    if st.button("🎬 Crear video vertical", use_container_width=True):
        output = Path("outputs") / f"portes_{sport.lower()}_video.mp4"
        try:
            render_video(script, output, seconds=15)
            st.session_state.video_path = str(output)
            st.success("Video creado correctamente.")
        except Exception as exc:
            st.error(f"No se pudo crear el video: {exc}")

if (
    st.session_state.video_path
    and Path(st.session_state.video_path).exists()
):
    st.divider()
    st.subheader("Video listo")
    st.video(st.session_state.video_path)

    with open(st.session_state.video_path, "rb") as video_file:
        st.download_button(
            "⬇️ Descargar MP4",
            video_file,
            file_name=Path(st.session_state.video_path).name,
            mime="video/mp4",
            use_container_width=True,
        )

    st.button(
        "📤 Publicar en TikTok",
        disabled=True,
        use_container_width=True,
    )
    st.caption(
        "El botón se habilitará después de vincular TikTok "
        "mediante OAuth y aprobar los permisos oficiales."
    )
