from datetime import date
from pathlib import Path
import json,pandas as pd,plotly.graph_objects as go,streamlit as st
from portes_sports.providers.registry import get_games,get_teams,get_players
from portes_sports.projection import project
from portes_sports.scoring import viral_score
from portes_sports.scriptwriter import generate_script

st.set_page_config(page_title="PORTES AI SPORTS PRO 4",page_icon="🏆",layout="wide")
st.title("🏆 PORTES AI SPORTS PRO 4.0")
st.caption("Partidos · Equipos · Jugadores · Comparación · Proyecciones · Contenido")
config=json.loads(Path("sports_config.json").read_text(encoding="utf-8"))
with st.sidebar:
    sport=st.selectbox("Deporte",list(config),format_func=lambda x:f"{config[x]['icon']} {x}")
    section=st.radio("Sección",["Partidos","Equipos","Jugadores","Comparador","Proyecciones","Crear contenido"])
provider=config[sport]["provider"]
teams=get_teams(sport,provider);players=get_players(sport,provider)

if section=="Partidos":
    d=st.date_input("Fecha",date.today())
    if st.button("Consultar partidos"): st.session_state["games"]=get_games(sport,provider,d.isoformat())
    games=st.session_state.get("games",[])
    st.dataframe(pd.DataFrame(games),use_container_width=True,hide_index=True) if games else st.info("No hay partidos para esa fecha o falta conectar una API.")
elif section=="Equipos":
    st.dataframe(pd.DataFrame(teams),use_container_width=True,hide_index=True) if teams else st.info("No hay equipos cargados.")
elif section=="Jugadores":
    st.dataframe(pd.DataFrame(players),use_container_width=True,hide_index=True) if players else st.info("No hay jugadores cargados.")
elif section=="Comparador":
    if len(teams)<2: st.info("Se necesitan dos participantes.")
    else:
        names=[x["team"] for x in teams]
        a=st.selectbox("Participante A",names,index=0);b=st.selectbox("Participante B",names,index=min(1,len(names)-1))
        A=next(x for x in teams if x["team"]==a);B=next(x for x in teams if x["team"]==b)
        cats=["Forma","Ataque","Defensa","Disponibilidad","Elo"]
        av=[float(A["recent_form"])*100,float(A["attack_rating"]),float(A["defense_rating"]),float(A["availability"])*100,float(A["elo"])/20]
        bv=[float(B["recent_form"])*100,float(B["attack_rating"]),float(B["defense_rating"]),float(B["availability"])*100,float(B["elo"])/20]
        fig=go.Figure();fig.add_trace(go.Scatterpolar(r=av,theta=cats,fill="toself",name=a));fig.add_trace(go.Scatterpolar(r=bv,theta=cats,fill="toself",name=b));fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100])))
        st.plotly_chart(fig,use_container_width=True)
elif section=="Proyecciones":
    if len(teams)<2: st.info("Se necesitan dos participantes.")
    else:
        names=[x["team"] for x in teams]
        h=st.selectbox("Local / A",names,index=0);a=st.selectbox("Visitante / B",names,index=min(1,len(names)-1))
        H=next(x for x in teams if x["team"]==h);A=next(x for x in teams if x["team"]==a);p=project(H,A,sport)
        c1,c2,c3=st.columns(3);c1.metric(h,f"{p['home_probability']}%");c2.metric(a,f"{p['away_probability']}%");c3.metric("Confianza",p["confidence"])
        st.subheader(f"Marcador estimado: {h} {p['home_score']} – {p['away_score']} {a}")
        st.caption("Estimación probabilística; no garantiza resultados ni constituye consejo de apuestas.")
else:
    headline=st.text_input("Titular");summary=st.text_area("Datos confirmados");star=st.slider("Figuras",1,10,7);visual=st.slider("Fuerza visual",1,10,8)
    if st.button("Generar contenido") and headline and summary:
        score=viral_score(headline,summary,star,visual);st.session_state["script"]=generate_script(sport,headline,summary,score);st.session_state["score"]=score
    if st.session_state.get("script"):
        s=st.session_state["script"];st.metric("Potencial",f"{st.session_state['score']}/100");st.text_area("Hook",s["hook"]);st.text_area("Cuerpo",s["body"]);st.text_area("Cierre",s["close"])
