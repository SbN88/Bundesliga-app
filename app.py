def get_detailed_stats(team_name, matches):
    team_matches = [m for m in matches if (m['team1']['teamName'] == team_name or m['team2']['teamName'] == team_name) and m['matchIsFinished']]
    
    total_matches = len(team_matches)
    if total_matches == 0:
        return 0, 0, 0
    
    total_goals = 0
    btts_count = 0
    
    for m in team_matches:
        g1 = m['matchResults'][0]['pointsTeam1']
        g2 = m['matchResults'][0]['pointsTeam2']
        total_goals += (g1 + g2)
        if g1 > 0 and g2 > 0:
            btts_count += 1
            
    avg_goals = total_goals / total_matches
    btts_chance = btts_count / total_matches
    return avg_goals, btts_chance, total_matches

# In der Hauptschleife (wo die Spiele angezeigt werden):
avg_g1, btts1, count1 = get_detailed_stats(team1, all_season_matches)
avg_g2, btts2, count2 = get_detailed_stats(team2, all_season_matches)

# Prognose-Berechnungen
expected_goals = (avg_g1 + avg_g2) / 2
combined_btts = (btts1 + btts2) / 2

# Anzeige in der App
st.markdown(f"### 📊 Analyse: {team1} vs. {team2}")
col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.metric("Erwartete Tore", f"{expected_goals:.2f}")
    st.caption("Schnitt beider Teams")

with col_stat2:
    st.metric("Beide treffen (BTTS)", f"{combined_btts:.0%}")
    st.progress(combined_btts)

with col_stat3:
    # Da Ecken selten in Gratis-APIs sind, nutzen wir den Liga-Schnitt (ca. 9.5) 
    # und modifizieren ihn leicht nach der Offensivkraft
    estimated_corners = 9.5 + (avg_g1 + avg_g2 - 3) 
    st.metric("Ecken Prognose", f"~{estimated_corners:.1f}")
