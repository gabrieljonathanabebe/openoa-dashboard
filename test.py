# Dummy-Daten für Fußballspieler
player_stats = {
    "Messi": {"goals": 30, "assists": 12, "team": "PSG"},
    "Ronaldo": {"goals": 28, "assists": 5, "team": "Man United"},
    "Haaland": {"goals": 35, "team": "Man City"},
    "Neymar": {"assists": 14, "team": "PSG"},
    "Kane": {"goals": 25, "assists": 10, "team": "Tottenham"}
}




player_info = []

for player, stats in player_stats.items():
    goals = stats.get("goals", 0)
    assists = stats.get("assists", 0)
    if goals == 0:
        goals_text = "keine Tore"
    else:
        goals_text = f"{goals} Tore"
    if assists == 0:
        assists_text = "keine Assists"
    else:
        assists_text = f"{assists} Assists"
    player_info.append(f"{player} hat {goals_text} und {assists_text}.")
print(player_info)
    