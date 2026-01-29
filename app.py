import streamlit as st
import requests
import pandas as pd

# Grundeinstellungen
API_BASE = "https://api.openligadb.de"
LEAGUE = "bl1"
SEASON = "2025"

st.set_page_config(page_title="Bundesliga Analyse", layout="wide")
st.title("⚽ Bundesliga Prognose-Tool")

# 1. Daten-Funktionen
@st.cache_data
def get_data(endpoint):
    return requests.get(f"{API_BASE}/{endpoint}").json()

def get_detailed_stats(team_name, matches):
    team_matches = [m for m in matches if (m['team1']['teamName'] == team_name or m['team2']['teamName'] == team_name) and m['matchIsFinished']]
    if not team_matches:
        return 0.0, 0.0, 0
    
    total_goals = 0
    btts_count = 0
    for m in team_matches:
        g1 = m['matchResults'][0]['pointsTeam1']
        g2 = m['matchResults'][0]['pointsTeam2']
        total_goals += (g1 + g2)
        if g1 > 0 and g2 > 0:
            btts_count += 1
    
    return total_goals / len(team_matches), btts_count / len(team_matches), len(team_matches)

# 2. Daten laden
try:
    current_matches = get_data(f"getmatchdata/{LEAGUE}")
    all_season_matches = get_data(f"getmatchdata/{LEAGUE}/{SEASON}")

    st.header("Analyse der nächsten Spiele")

    # 3. Hauptschleife: Jedes Spiel einzeln analysieren
    for match in current_matches:
        if not match['matchIsFinished']:
            team1 = match['team1']['teamName']
            team2 = match['team2']['teamName']
            
            # Statistiken berechnen
            avg_g1, btts1, count1 = get_detailed_stats(team1, all_season_matches)
            avg_g2, btts2, count2 = get_detailed_stats(team2, all_season_matches)
            
            expected_goals = (avg_g1 + avg_g2) / 2
            combined_btts = (btts1 + btts2) / 2

            # Anzeige
            with st.expander(f"{team1} vs. {team2}", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(match['team1']['teamIconUrl'], width=50)
                    st.write(f"**{team1}**")
                    st.caption(f"Schnitt: {avg_g1:.1f} Tore")
                
                with col2:
                    st.metric("Tore Erwartet", f"{expected_goals:.2f}")
                    st.metric("Beide treffen", f"{combined_btts:.0%}")
                
                with col3:
                    st.image(match['team2']['teamIconUrl'], width=50)
                    st.write(f"**{team2}**")
                    st.caption(f"Schnitt: {avg_g2:.1f} Tore")
                
                # Ecken-Schätzung (simuliert)
                st.info(f"Geschätzte Ecken: ~{9.5 + (expected_goals - 2.5):.1f}")

except Exception as e:
    st.error(f"Fehler beim Laden der Daten: {e}")
