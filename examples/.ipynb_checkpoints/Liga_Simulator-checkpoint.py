
from dataclasses import dataclass
import pandas as pd
import numpy as np
import os
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from typing import List, Tuple
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.console import Group, Console
from rich.live import Live
from rich import box
from scipy.stats import beta
from sklearn.linear_model import LinearRegression



class DataPreprocessor:
    def __init__(self, filename: str):
        self.filename = filename

    def load_and_clean_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        tabellen_df = pd.read_excel(self.filename, sheet_name="Tabellen")
        spieler_df = pd.read_excel(self.filename, sheet_name="Spieler")
        karten_df = pd.read_excel(self.filename, sheet_name="Karten")
        goals_df = pd.read_excel(self.filename, sheet_name="BL")

        tabellen_df.columns = tabellen_df.columns.str.strip()
        tabellen_df["Team"] = tabellen_df["Team"].str.strip().str.replace(r"\s+", " ", regex=True)
        tabellen_df = tabellen_df[tabellen_df["Liga"] == "BL"].copy()

        spieler_df["Team"] = spieler_df["Team"].str.strip()
        tabellen_df["WappenPfad"] = tabellen_df["Team"].apply(self.get_logo_path)

        return tabellen_df, spieler_df, karten_df, goals_df

    def get_logo_path(self, team_name: str) -> str:
        path = os.path.join("Wappen", f"{team_name}.png")
        return path if os.path.exists(path) else ""

    def merge_karten_data(self, spieler_df: pd.DataFrame, karten_df: pd.DataFrame) -> pd.DataFrame:
        # Nur Datenstruktur bereinigen und zusammenführen, keine Ratings
        karten_df["Karten_pro_Spiel"] = karten_df["Karten_pro_Spiel"].str.replace(",", ".").astype(float)
        merged = spieler_df.merge(karten_df, on="NAME", how="left")
        merged["Gelbe_Karten"] = merged["Gelbe_Karten"].fillna(0).astype(int)
        merged["Rote_Karten"] = merged["Rote_Karten"].fillna(0).astype(int)
        merged["Karten_pro_Spiel"] = merged["Karten_pro_Spiel"].fillna(0).astype(float)
        return merged
    
    def prepare_simulation_data(
        self,
        tabellen_df: pd.DataFrame,
        goals_df: pd.DataFrame,
        spieler_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Liefert zwei DataFrames zurück:
        - team_df mit allen relevanten Teamwerten
        - spieler_df reduziert auf nur relevante Spalten
        """
        team_df = pd.merge(tabellen_df, goals_df, on="Team")

        team_df = team_df[[
            "Team", "Heim_Rating", "Auswärts_Rating", "Goal_Rating", "GoalA_Rating",
            "AVG_POSS", "XG", "XGA", "SHOTS_PER_GAME", "SHOTS_A_PER_GAME", "XG_PER_SHOT"
        ]].copy()

        spieler_df = spieler_df[[
            "NAME", "Team", "GOALS", "XG", "Spielzeit_Rating",
            "yellow_card_rating", "red_card_rating"
        ]].copy()

        return team_df, spieler_df


class RatingCalculator:
    def berechne_heim_auswaerts_ratings(self, df: pd.DataFrame) -> pd.DataFrame:
        MAX_PTS, MAX_DIFF, MAX_XPTS = 51, 40, 75
        df["Heim_Rating"] = (
            0.6 * (df["HPTS"] / MAX_PTS) +
            0.2 * (df["HD"].clip(lower=0) / MAX_DIFF) +
            0.2 * (df["xPTS"] / MAX_XPTS)
        ) * 100
        df["Auswärts_Rating"] = (
            0.6 * (df["APTS"] / MAX_PTS) +
            0.2 * (df["AD"].clip(lower=0) / MAX_DIFF) +
            0.2 * (df["xPTS"] / MAX_XPTS)
        ) * 100
        return df

    def berechne_goal_ratings(self, goals_df: pd.DataFrame, tabelle_df: pd.DataFrame) -> pd.DataFrame:
        goals_df["Goal_Raw"] = 0.7 * goals_df["GOALS"] + 0.3 * goals_df["XG"]
        goals_df["GoalA_Raw"] = 0.7 * goals_df["GOALS_A"] + 0.3 * goals_df["XGA"]

        MAX_RAW = 0.7 * 95 + 0.3 * 80
        MIN_RAW = 0.7 * 20 + 0.3 * 20

        goals_df["Goal_Rating"] = (goals_df["Goal_Raw"] / MAX_RAW) * 100
        goals_df["GoalA_Rating"] = (MIN_RAW / goals_df["GoalA_Raw"]) * 100

        ratings_df = goals_df[["Team", "Goal_Rating", "GoalA_Rating"]].copy()
        return pd.merge(tabelle_df[["Team", "Heim_Rating", "Auswärts_Rating"]], ratings_df, on="Team")

    def berechne_kartenratings(self, spieler_df: pd.DataFrame) -> pd.DataFrame:
        spieler_df["yellow_card_rating"] = (
            0.7 * (spieler_df["Gelbe_Karten"] / spieler_df["APPS"])
        ).fillna(0).clip(lower=0.01)

        spieler_df["red_card_rating"] = (
            spieler_df["Rote_Karten"] / spieler_df["APPS"]
        ).fillna(0).clip(lower=0.01)

        return spieler_df

    def berechne_spielzeit_rating(self, spieler_df: pd.DataFrame) -> pd.DataFrame:
        def normalize(series, min_val=0.005, max_val=0.995):
            norm = (series - series.min()) / (series.max() - series.min())
            return norm * (max_val - min_val) + min_val

        spieler_df["Spielzeit_Rating"] = (
            0.4 * normalize(spieler_df["APPS"]) +
            0.3 * normalize(spieler_df["MINS PER APP"]) +
            0.3 * normalize(spieler_df["MINS"])
        )
        return spieler_df




class ScheduleBuilder:
    def round_robin_random(self, teams: List[str]) -> List[List[Tuple[str, str]]]:
        teams = list(teams)
        if len(teams) % 2 != 0:
            teams.append("FREI")
        n = len(teams)
        matchdays = []
        for i in range(n - 1):
            mid = n // 2
            l1, l2 = teams[:mid], teams[mid:]
            l2.reverse()
            pairs = []
            for j in range(mid):
                if "FREI" in (l1[j], l2[j]):
                    continue
                if random.random() < 0.5:
                    pairs.append((l1[j], l2[j]))
                else:
                    pairs.append((l2[j], l1[j]))
            matchdays.append(pairs)
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        return matchdays

    def erzeuge_spielplan_df(self, teams: List[str]) -> pd.DataFrame:
        hinrunde = self.round_robin_random(teams)
        spiele_hin = [
            {"matchday": i + 1, "hometeam": home, "awayteam": away}
            for i, pairs in enumerate(hinrunde)
            for home, away in pairs
        ]
        spiele_rueck = [
            {"matchday": spiel["matchday"] + len(hinrunde), "hometeam": spiel["awayteam"], "awayteam": spiel["hometeam"]}
            for spiel in spiele_hin
        ]
        return pd.DataFrame(spiele_hin + spiele_rueck)




from dataclasses import dataclass, field
import pandas as pd
from typing import List, Optional


@dataclass
class Player:
    name: str
    team_name: str
    goal_score: float
    goal_rate: float
    yellow_card_rating: float
    red_card_rating: float
    spielzeit_rating: float
    apps: int
    mins: int
    mins_per_app: float

    @staticmethod
    def from_dataframe(row: pd.Series, team_goal_score: float, team_goal_rating: float) -> "Player":
        tor_score = 0.7 * row["GOALS"] + 0.3 * row["XG"]
        goal_rate = (tor_score / team_goal_score) * team_goal_rating if team_goal_score > 0 else 0.01

        return Player(
            name=row["NAME"],
            team_name=row["Team"],
            goal_score=tor_score,
            goal_rate=goal_rate,
            yellow_card_rating=max(0.01, row.get("yellow_card_rating", 0.01)),
            red_card_rating=max(0.01, row.get("red_card_rating", 0.01)),
            spielzeit_rating=row["Spielzeit_Rating"],
            apps=row["APPS"],
            mins=row["MINS"],
            mins_per_app=row["MINS PER APP"]
        )


@dataclass
class Team:
    name: str
    wappen_path: Optional[str]
    heim_rating: float
    auswärts_rating: float
    goal_rating: float
    goal_against_rating: float
    players: List[Player] = field(default_factory=list)

    @staticmethod
    def from_dataframes(team_row: pd.Series, player_df: pd.DataFrame, ratings_df: pd.DataFrame) -> "Team":
        team_name = team_row["Team"]
        team_players_df = player_df[player_df["Team"] == team_name].copy()

        # Tor_Score berechnen
        team_players_df["Tor_Score"] = 0.7 * team_players_df["GOALS"] + 0.3 * team_players_df["XG"]
        team_score_sum = team_players_df["Tor_Score"].sum()
        team_goal_rating = ratings_df.loc[ratings_df["Team"] == team_name, "Goal_Rating"].values[0]

        players = [
            Player.from_dataframe(row, team_score_sum, team_goal_rating)
            for _, row in team_players_df.iterrows()
        ]

        return Team(
            name=team_name,
            wappen_path=team_row.get("WappenPfad"),
            heim_rating=team_row["Heim_Rating"],
            auswärts_rating=team_row["Auswärts_Rating"],
            goal_rating=team_goal_rating,
            goal_against_rating=ratings_df.loc[ratings_df["Team"] == team_name, "GoalA_Rating"].values[0],
            players=players
        )
    
    
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
from datetime import datetime

@dataclass
class Match:
    matchday: int
    home_team: "Team"
    away_team: "Team"
    kickoff: str
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    halftime_result: Optional[str] = None
    goal_log: List[Tuple[str, str]] = field(default_factory=list)
    yellow_card_log: List[str] = field(default_factory=list)
    red_card_log: List[str] = field(default_factory=list)
    yellowred_card_log: List[str] = field(default_factory=list)
    possession: Dict[str, float] = field(default_factory=dict)
    shots: Dict[str, int] = field(default_factory=dict)

    def is_played(self) -> bool:
        return self.home_goals is not None and self.away_goals is not None

    def result_str(self) -> str:
        if not self.is_played():
            return "- : -"
        return f"{self.home_goals} : {self.away_goals}"

    def kickoff_time(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self.kickoff, "%a %H:%M")  # Bsp: "Sa 15:30"
        except Exception:
            return None
        

from dataclasses import dataclass
from typing import List

@dataclass
class Matchday:
    number: int
    matches: List[Match]

    def is_completed(self) -> bool:
        return all(match.is_played() for match in self.matches)

    def summary(self) -> str:
        return f"📅 Spieltag {self.number}: " + ", ".join(
            f"{m.home_team.name} {m.result_str()} {m.away_team.name}" for m in self.matches
        )


@dataclass
class Schedule:
    matchdays: List[Matchday]
    current_index: int = 0

    def current(self) -> Matchday:
        return self.matchdays[self.current_index]

    def next(self) -> Optional[Matchday]:
        if self.current_index + 1 < len(self.matchdays):
            self.current_index += 1
            return self.current()
        return None

    def reset(self):
        self.current_index = 0
        
        
import pandas as pd
import random


class KickoffAssigner:
    def __init__(self, ratings_df: pd.DataFrame):
        self.ratings_df = ratings_df.copy()
        self.zeitfenster_schema = [
            "Fr 20:30",
            "Sa 15:30", "Sa 15:30", "Sa 15:30", "Sa 15:30", "Sa 15:30",
            "Sa 18:30",
            "So 15:30",
            "So 17:30"
        ]

    def weise_zeitfenster_zu(self, spielplan_df: pd.DataFrame) -> pd.DataFrame:
        df = spielplan_df.copy()

        # Ratings den Teams zuordnen
        heim_ratings = self.ratings_df.set_index("Team")["Heim_Rating"]
        auswärts_ratings = self.ratings_df.set_index("Team")["Auswärts_Rating"]
        df["avg_rating_home"] = df["hometeam"].map(heim_ratings)
        df["avg_rating_away"] = df["awayteam"].map(auswärts_ratings)
        df["avg_rating"] = (df["avg_rating_home"] + df["avg_rating_away"]) / 2

        df["Anpfiff"] = ""

        for matchday, gruppe in df.groupby("matchday"):
            slots = self.zeitfenster_schema.copy()

            # Bestes Spiel: Höchste Ratingkombination → Topspiel Sa 18:30
            top_idx = gruppe["avg_rating"].idxmax()
            df.at[top_idx, "Anpfiff"] = "Sa 18:30"
            slots.remove("Sa 18:30")

            # Rest zufällig auf Slots verteilen
            rest_idx = [i for i in gruppe.index if i != top_idx]
            random.shuffle(slots)
            for idx, zeit in zip(rest_idx, slots):
                df.at[idx, "Anpfiff"] = zeit

        # Optional: nach Anpfiff sortieren
        df["__tag"] = df["Anpfiff"].str.extract(r"^(Fr|Sa|So)")
        df["__zeit"] = df["Anpfiff"].str.extract(r"(\d{2}:\d{2})")
        df["__tag_order"] = df["__tag"].map({"Fr": 1, "Sa": 2, "So": 3})
        df["__zeit_dt"] = pd.to_datetime(df["__zeit"], format="%H:%M")
        df = df.sort_values(["matchday", "__tag_order", "__zeit_dt"]).drop(columns=["__tag", "__zeit", "__tag_order", "__zeit_dt"]).reset_index(drop=True)

        return df




preprocessor = DataPreprocessor("stats.xlsx")
rating_calc = RatingCalculator()

# 1. Daten laden und bereinigen
tabellen_df, spieler_df, karten_df, goals_df = preprocessor.load_and_clean_data()

# 2. Merge durchführen (noch keine Bewertung!)
spieler_df = preprocessor.merge_karten_data(spieler_df, karten_df)

# 3. Ratings berechnen
tabellen_df = rating_calc.berechne_heim_auswaerts_ratings(tabellen_df)
spieler_df = rating_calc.berechne_kartenratings(spieler_df)
spieler_df = rating_calc.berechne_spielzeit_rating(spieler_df)
ratings_df = rating_calc.berechne_goal_ratings(goals_df, tabellen_df)


teams = [
    Team.from_dataframes(team_row, spieler_df, ratings_df)
    for _, team_row in tabellen_df.iterrows()
]

team_dict = {team.name: team for team in teams}


schedule_builder = ScheduleBuilder()
spielplan_df = schedule_builder.erzeuge_spielplan_df(list(team_dict.keys()))


matchdays = []

for matchday_num, group in spielplan_df.groupby("matchday"):
    matches = []
    for _, row in group.iterrows():
        match = Match(
            matchday=int(row["matchday"]),
            home_team=team_dict[row["hometeam"]],
            away_team=team_dict[row["awayteam"]],
            kickoff=row["Anpfiff"] if "Anpfiff" in row else "Sa 15:30"
        )
        matches.append(match)
    
    matchdays.append(Matchday(number=matchday_num, matches=matches))
    
    

schedule = Schedule(matchdays=matchdays)


# 1. Erzeuge den Spielplan
schedule_builder = ScheduleBuilder()
spielplan_df = schedule_builder.erzeuge_spielplan_df(list(team_dict.keys()))

# 2. Weise Anpfiff-Zeiten anhand der Ratings zu
kickoff_assigner = KickoffAssigner(ratings_df=ratings_df)
spielplan_df = kickoff_assigner.weise_zeitfenster_zu(spielplan_df)

# 3. Erzeuge die Match-Objekte mit den aktualisierten Anpfiff-Zeiten
matchdays = []

for matchday_num, group in spielplan_df.groupby("matchday"):
    matches = []
    for _, row in group.iterrows():
        match = Match(
            matchday=int(row["matchday"]),
            home_team=team_dict[row["hometeam"]],
            away_team=team_dict[row["awayteam"]],
            kickoff=row["Anpfiff"]  # ✅ Hier steht jetzt der echte Slot drin!
        )
        matches.append(match)
    matchdays.append(Matchday(number=matchday_num, matches=matches))

schedule = Schedule(matchdays=matchdays)




from dataclasses import dataclass, field
from typing import Dict, List
from collections import defaultdict


@dataclass
class StatTracker:
    team_stats: Dict[str, Dict[str, int]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))
    player_goals: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    player_yellow_cards: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    player_red_cards: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    player_yellowred_cards: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    team_forms: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    team_home_stats: Dict[str, Dict[str, int]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))
    team_away_stats: Dict[str, Dict[str, int]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))
    team_possession: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    team_shots: Dict[str, List[int]] = field(default_factory=lambda: defaultdict(list))
    
    

    def initialize(self, teams: List[str], players_df: pd.DataFrame):
        for team in teams:
            for key in ["GF", "GA", "SP", "S", "U", "N", "PTS", "D"]:
                self.team_stats[team][key] = 0
            self.team_forms[team] = []

        for name in players_df["NAME"]:
            self.player_goals[name] = 0
            self.player_yellow_cards[name] = 0
            self.player_red_cards[name] = 0
            self.player_yellowred_cards[name] = 0

    def update_after_match(self, match):
        # Teamnamen
        home = match.home_team.name
        away = match.away_team.name
        hg = match.home_goals
        ag = match.away_goals
    
        # --- 1. Team-Statistiken ---
        self.team_stats[home]["GF"] += hg
        self.team_stats[home]["GA"] += ag
        self.team_stats[away]["GF"] += ag
        self.team_stats[away]["GA"] += hg
    
        self.team_stats[home]["SP"] += 1
        self.team_stats[away]["SP"] += 1
    
        if hg > ag:
            self.team_stats[home]["S"] += 1
            self.team_stats[home]["PTS"] += 3
            self.team_stats[away]["N"] += 1
            self.team_forms[home].append("S")
            self.team_forms[away].append("N")
        elif hg == ag:
            self.team_stats[home]["U"] += 1
            self.team_stats[away]["U"] += 1
            self.team_stats[home]["PTS"] += 1
            self.team_stats[away]["PTS"] += 1
            self.team_forms[home].append("U")
            self.team_forms[away].append("U")
        else:
            self.team_stats[away]["S"] += 1
            self.team_stats[away]["PTS"] += 3
            self.team_stats[home]["N"] += 1
            self.team_forms[away].append("S")
            self.team_forms[home].append("N")
    
        # Tordifferenz aktualisieren
        self.team_stats[home]["D"] = self.team_stats[home]["GF"] - self.team_stats[home]["GA"]
        self.team_stats[away]["D"] = self.team_stats[away]["GF"] - self.team_stats[away]["GA"]
    
        # --- 2. Spielerstatistiken ---
        # ⛔ Du brauchst hier eine "event log" Struktur, z. B. match.events oder match.goal_events
        # Angenommen match.goal_log: List[Tuple[str teamname, str scorername]]
    
        if hasattr(match, "goal_log"):
            for team, scorer, _, red, yellow in match.goal_log:
                self.player_goals[scorer] += 1
                if red and yellow:
                    self.player_yellowred_cards[scorer] += 1
                elif yellow and not red:
                    self.player_yellow_cards[scorer] += 1
                elif red and not yellow:
                    self.player_red_cards[scorer] += 1
    
        # Teamform auf max 5 Einträge beschränken
        self.team_forms[home] = self.team_forms[home][-5:]
        self.team_forms[away] = self.team_forms[away][-5:]
        
        self.team_home_stats[home]["SP"] += 1
        self.team_away_stats[away]["SP"] += 1
        
        self.team_home_stats[home]["GF"] += hg
        self.team_home_stats[home]["GA"] += ag
        self.team_away_stats[away]["GF"] += ag
        self.team_away_stats[away]["GA"] += hg
        
        if hg > ag:
            self.team_home_stats[home]["S"] += 1
            self.team_away_stats[away]["N"] += 1
        elif hg == ag:
            self.team_home_stats[home]["U"] += 1
            self.team_away_stats[away]["U"] += 1
        else:
            self.team_home_stats[home]["N"] += 1
            self.team_away_stats[away]["S"] += 1
        
        self.team_home_stats[home]["PTS"] += 3 if hg > ag else 1 if hg == ag else 0
        self.team_away_stats[away]["PTS"] += 3 if ag > hg else 1 if ag == hg else 0
        
        # 📈 Ballbesitz erfassen
        if hasattr(match, "live_possession_home") and len(match.live_possession_home) > 0:
            home_avg = np.mean(match.live_possession_home)
            away_avg = 100 - home_avg
            self.team_possession[match.home_team.name].append(home_avg)
            self.team_possession[match.away_team.name].append(away_avg)
        
        # 🎯 Schüsse erfassen
        home_shots = len(match.shot_min_home) if hasattr(match, "shot_min_home") else 0
        away_shots = len(match.shot_min_away) if hasattr(match, "shot_min_away") else 0
        self.team_shots[match.home_team.name].append(home_shots)
        self.team_shots[match.away_team.name].append(away_shots)

    def top_scorer_table(self, top_n=10):
        return sorted(self.player_goals.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def yellow_card_table(self, top_n=10):
        return sorted(self.player_yellow_cards.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    def red_card_table(self, top_n=10):
        return sorted(self.player_red_cards.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def team_table(self):
        table = []
        for team, stats in self.team_stats.items():
            table.append({
                "Team": team,
                "SP": stats["SP"],
                "S": stats["S"],
                "U": stats["U"],
                "N": stats["N"],
                "PTS": stats["PTS"],
                "Goals": stats["GF"],
                "Goals Against": stats["GA"],
                "D": stats["D"],
                "Form": "-".join(self.team_forms[team][-5:])
            })
        return sorted(table, key=lambda x: (x["PTS"], x["D"], x["Goals"]), reverse=True)
    
    def sending_off_table(self, top_n=10):
        combined = defaultdict(int)
        for player in set(self.player_red_cards.keys()).union(self.player_yellowred_cards.keys()):
            combined[player] = (
                self.player_red_cards.get(player, 0) +
                self.player_yellowred_cards.get(player, 0)
            )
        return sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def initialize_player_tracking(self, spieler_df):
        """Initialisiert alle Spieler mit 0 Toren, Gelben und Roten Karten."""
        for name in spieler_df["NAME"]:
            self.player_goals[name] = 0
            self.player_yellow_cards[name] = 0
            self.player_red_cards[name] = 0


stat_tracker = StatTracker()
stat_tracker.initialize(tabellen_df["Team"].tolist(), spieler_df)







class LeagueTable:
    def __init__(self, stat_tracker: StatTracker):
        self.stat_tracker = stat_tracker

    def get_table(self) -> pd.DataFrame:
        raw = self.stat_tracker.team_table()
        df = pd.DataFrame(raw)
        df["Goals"] = df["Goals"].astype(str) + " : " + df["Goals Against"].astype(str)
        df["Platz"] = range(1, len(df) + 1)
        return df[["Platz", "Team", "SP", "S", "U", "N", "PTS", "Goals", "D", "Form"]]

league_table = LeagueTable(stat_tracker)




import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


class Plotter:
    def __init__(self):
        pass

    def plot_matchday_games(self, df: pd.DataFrame, title: str, tabellen_df: pd.DataFrame = None, block_column=None):
        self._plot_df(df, title, block_column, tabellen_df, table_type="matchday")

    def plot_table(self, df: pd.DataFrame, title: str, tabellen_df: pd.DataFrame):
        self._plot_df(df, title, block_column=None, tabellen_df=tabellen_df, table_type="league")

    def _plot_df(self, df, title, block_column, tabellen_df, table_type="matchday"):
        df = df.copy()

        if "Anpfiff" in df.columns:
            cols = df.columns.tolist()
            cols = ["Anpfiff"] + [c for c in cols if c != "Anpfiff"]
            df = df[cols]

        for spalte in ["Heim", "Auswärts", "Team"]:
            if spalte in df.columns:
                df[spalte] = df[spalte].astype(str).str.strip()

        if "Halbzeit" in df.columns:
            df["Halbzeit"] = df["Halbzeit"].astype(str).str.replace(r"(\d):(\d)", r"( \1 : \2 )", regex=True)

        def calc_col_widths(df, offset=0.5):
            return [max(df[col].astype(str).map(len).max(), len(str(col))) + offset for col in df.columns]

        fig, ax = plt.subplots(figsize=(16, 8))
        ax.set_title(title, fontsize=18, y=1.05)
        ax.axis("off")
        fig.subplots_adjust(top=0.88, bottom=0.12)

        widths = calc_col_widths(df)
        col_widths = [w / sum(widths) for w in widths]

        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            colWidths=col_widths,
            loc="center",
            bbox=[-0.08, 0, 1.16, 1],
        )
        table.scale(1.1, 2.2)
        table.auto_set_font_size(False)
        table.set_fontsize(17)
        fig.canvas.draw()
        ax.set_xlim(-0.05, 1.05)

        # 🎨 Farben für Spieltagsübersicht (z. B. nach Zeitfenster)
        if block_column is not None:
            if isinstance(block_column, str) and block_column in df.columns:
                df["_block_group"] = df[block_column]
            elif isinstance(block_column, pd.Series):
                df["_block_group"] = block_column.reset_index(drop=True)
            else:
                raise ValueError("block_column muss entweder Spaltenname oder Series sein")

            cmap = plt.get_cmap("Pastel2")
            unique_blocks = df["_block_group"].unique()
            block_colors = {block: cmap(i % cmap.N) for i, block in enumerate(unique_blocks)}

        n_rows, n_cols = df.shape
        for row in range(len(df)):
            for col, col_name in enumerate(df.columns):
                key = (row + 1, col)
                if key not in table._cells:
                    continue
                cell = table[key]

                # Zeitblock-Farben
                if block_column is not None:
                    block = df["_block_group"].iloc[row]
                    cell.set_facecolor(block_colors[block])

                # Ausrichtung
                if col_name == "Heim":
                    cell.get_text().set_ha("right")
                elif col_name == "Auswärts":
                    cell.get_text().set_ha("left")
                elif col_name in ["Ergebnis", "Halbzeit", "PTS", "Tore", "D"]:
                    cell.get_text().set_ha("center")
                elif col_name == "Platz":
                    cell.get_text().set_ha("right")
                else:
                    cell.get_text().set_ha("left")

        if "_block_group" in df.columns:
            df.drop(columns=["_block_group"], inplace=True)

        # ⚽ Tabellen-Extras nur für Ligatabelle
        # Logos immer einfügen, falls Wappen vorhanden
        if "WappenPfad" in tabellen_df.columns:
            self._insert_team_logos(ax, df, table, tabellen_df, ["Heim", "Auswärts"], zoom=0.3)
        
        # Tabellenfarben nur für Ligatabelle
        if table_type == "league":
            self._apply_table_colors(df, table, ax)

        plt.tight_layout()
        plt.show()

    def _apply_table_colors(self, df, table, ax):
        colors = {
            "CL": "#4390dd",
            "EL": "#88bbee",
            "ECL": "#cce6ff",
            "REL": "#ffcc99",
            "ABS": "#ff9933"
        }

        for i, col in enumerate(df.columns):
            col_name = str(col)
            for j in range(len(df)):
                key = (j + 1, i)
                if key not in table._cells:
                    continue
                cell = table[key]

                if "Platz" in df.columns:
                    platz = df.iloc[j]["Platz"]
                    if platz in range(1, 5):
                        cell.set_facecolor(colors["CL"])
                    elif platz in [5, 6]:
                        cell.set_facecolor(colors["EL"])
                    elif platz == 7:
                        cell.set_facecolor(colors["ECL"])
                    elif platz == 16:
                        cell.set_facecolor(colors["REL"])
                    elif platz in [17, 18]:
                        cell.set_facecolor(colors["ABS"])

            # Header-Zellen fett
            header_cell = table[(0, i)]
            header_cell.set_facecolor("#DDDDDD")
            header_cell.get_text().set_weight("bold")
            header_cell.get_text().set_ha("left")

        # 🖼️ Wappen einfügen
        if "WappenPfad" in tabellen_df.columns:
            self._insert_team_logos(ax, df, table, tabellen_df, ["Team", "Heim", "Auswärts"], zoom=0.3)

        # 📚 Legende
        if "Platz" in df.columns:
            patches = [
                Patch(color=colors["CL"], label="Champions League"),
                Patch(color=colors["EL"], label="Europa League"),
                Patch(color=colors["ECL"], label="Conference League"),
                Patch(color=colors["REL"], label="Relegation"),
                Patch(color=colors["ABS"], label="Abstieg")
            ]
            ax.legend(
                handles=patches,
                loc='lower center',
                bbox_to_anchor=(0.5, -0.1),
                ncol=3,
                fontsize=13,
                frameon=False
            )

    def _insert_team_logos(self, ax, df, table, tabellen_df, spalten, zoom=0.8):
        fig = ax.get_figure()
        renderer = fig.canvas.get_renderer()
    
        for j in range(len(df)):
            for spalte in spalten:
                if spalte not in df.columns:
                    continue
    
                col_index = df.columns.get_loc(spalte)
                team_name = df.iloc[j][spalte]
                match = tabellen_df[tabellen_df["Team"] == team_name]
    
                if match.empty:
                    continue
    
                logo_path = match["WappenPfad"].values[0]
                if not os.path.exists(logo_path):
                    continue
    
                try:
                    cell = table[(j + 1, col_index)]
                    bbox = cell.get_window_extent(renderer)
                    inv = ax.transData.inverted()
                    x0, y0 = inv.transform((bbox.x0, bbox.y0))
                    x1, y1 = inv.transform((bbox.x1, bbox.y1))
                    y = (y0 + y1) / 2
    
                    # Positionierung: je nach Spalte leicht versetzt
                    x_rel_map = {
                        "Team": 0.03,
                        "Heim": 0.91,
                        "Auswärts": 0.02
                    }
                    x_rel = x_rel_map.get(spalte, 0.05)
                    x = x0 + x_rel * (x1 - x0)
    
                    img = mpimg.imread(logo_path)
                    imagebox = OffsetImage(img, zoom=0.8)
                    ab = AnnotationBbox(imagebox, (x, y), frameon=False, box_alignment=(0, 0.5), zorder=10)
                    ax.add_artist(ab)
    
                except Exception:
                    continue
            
    def plot_goalgetter(self, stat_tracker, tabellen_df, spieler_df):
        self._plot_player_stat_table(
            stat_tracker.top_scorer_table(),
            "Top-Torjäger",
            stat_tracker,
            tabellen_df,
            spieler_df,
            farbcode="#4444aa"
        )

    def plot_yellow_cards(self, stat_tracker, tabellen_df, spieler_df):
        self._plot_player_stat_table(
            stat_tracker.yellow_card_table(),
            "Gelbe Karten",
            stat_tracker,
            tabellen_df,
            spieler_df,
            farbcode="#d1c53f"
        )

    def plot_sending_offs(self, stat_tracker, tabellen_df, spieler_df):
        self._plot_player_stat_table(
            stat_tracker.sending_off_table(),
            "Platzverweise",
            stat_tracker,
            tabellen_df,
            spieler_df,
            farbcode="#cc3333"
        )

    def _plot_player_stat_table(self, data_list, title, stat_tracker, tabellen_df, spieler_df, farbcode):
        if not data_list:
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.axis("off")
            ax.set_title(title, fontsize=18, weight="bold")
            ax.text(0.5, 0.5, f"Keine {title.split()[1]} bisher", ha="center", va="center", fontsize=14)
            plt.tight_layout()
            plt.show()
            return
    
        # DataFrame mit Team + Spiele
        rows = []
        for spieler, wert in data_list:
            team = spieler_df.loc[spieler_df["NAME"] == spieler, "Team"].values[0]
            spiele = stat_tracker.team_stats[team]["SP"]
            rows.append([spieler, team, wert, spiele])
        
        df = pd.DataFrame(rows, columns=["Spieler", "Team", "Anzahl", "Spiele"]).head(10)
    
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(title, fontsize=18, y=1.05)
        ax.axis("off")
    
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            loc="center",
            cellLoc="left",
            colWidths=[0.4, 0.6, 0.1, 0.1],  # ✅ neu
            bbox=[0, 0, 1, 1]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(14)
        table.scale(1.5, 2)
        
        fig.canvas.draw()  # ✅ Hier zwingend erforderlich
    
        # Logos neben Team
        for i in range(len(df)):
            teamname = df.iloc[i]["Team"]
            match = tabellen_df[tabellen_df["Team"] == teamname]
            if not match.empty:
                logo_path = match["WappenPfad"].values[0]
                if os.path.exists(logo_path):
                    try:
                        cell = table[(i + 1, 1)]  # Teamspalte
                        bbox = cell.get_window_extent(fig.canvas.get_renderer())
                        inv = ax.transData.inverted()
                        x0, y0 = inv.transform((bbox.x0, bbox.y0))
                        x1, y1 = inv.transform((bbox.x1, bbox.y1))
                        y = (y0 + y1) / 2
                        x = x0 + 0.02 * (x1 - x0)  # Wappen leicht links vom Teamnamen
                        img = mpimg.imread(logo_path)
                        imagebox = OffsetImage(img, zoom=0.7)
                        ab = AnnotationBbox(imagebox, (x, y), frameon=False, box_alignment=(0, 0.5))
                        ax.add_artist(ab)
                    except Exception:
                        continue
    
            # Farbliche Zahl
            table[(i + 1, 2)].get_text().set_color(farbcode)
            table[(i + 1, 2)].get_text().set_ha("center")
    
        # Header-Styling
        for col in range(len(df.columns)):
            cell = table[(0, col)]
            cell.set_facecolor("#DDDDDD")
            cell.get_text().set_weight("bold")
    
        plt.tight_layout()
        plt.show()
        
class PlotHelper:
    def __init__(self, stat_tracker, tabellen_df):
        self.stat_tracker = stat_tracker
        self.tabellen_df = tabellen_df

    def plot_metric_bar_chart(
        self,
        data_func,
        title,
        ylabel,
        colormap,
        vcenter=None,
        ylim=None,
        ref_line=None,
        logo_offset=0.6,
        ref_label=None  # 🆕
    ):
        teams = self.tabellen_df["Team"].tolist()
        diffs = [(team, data_func(team)) for team in teams]
        df = pd.DataFrame(diffs, columns=["Team", "Wert"]).sort_values(by="Wert", ascending=False)
    
        values = df["Wert"]
        max_val = values.max()
        min_val = values.min()
    
        if vcenter is not None:
            max_abs = max(abs(min_val - vcenter), abs(max_val - vcenter))
            norm = mcolors.TwoSlopeNorm(vcenter=vcenter, vmin=vcenter - max_abs, vmax=vcenter + max_abs)
        else:
            norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    
        cmap = cm.get_cmap(colormap)
        colors = cmap(norm(values))
    
        fig, ax = plt.subplots(figsize=(14, 6))
        bars = ax.bar(range(len(df)), df["Wert"] - vcenter if vcenter is not None else df["Wert"], color=colors)
    
        # ↕️ Achse symmetrisch skalieren
        if ylim:
            ax.set_ylim(ylim)
        else:
            max_offset = max(abs(max_val - vcenter), abs(min_val - vcenter))
            ax.set_ylim(-max_offset - 1.5, max_offset + 1.5)
    
        if ref_line is not None:
            ax.axhline(0, color="black", linewidth=1.5)
            if ref_label:
                ax.text(len(df) + 0.2, 0, f"{ref_label}", va="center", ha="left", fontsize=10, fontweight="bold")
    
        # Logos
        for idx, (team, value) in enumerate(zip(df["Team"], df["Wert"])):
            logo_path = self.tabellen_df[self.tabellen_df["Team"] == team]["WappenPfad"].values[0]
            if os.path.exists(logo_path):
                img = mpimg.imread(logo_path)
                imagebox = OffsetImage(img, zoom=0.8)
                y_val = value - vcenter if vcenter is not None else value
                y_logo = y_val + logo_offset if y_val >= 0 else y_val - logo_offset
                ab = AnnotationBbox(imagebox, (idx, y_logo), frameon=False, box_alignment=(0.5, 0.5))
                ax.add_artist(ab)
    
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels([""] * len(df))
    
        # 🎨 Colorbar
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label(ylabel)
    
        plt.tight_layout()
        plt.show()
        
        
    def plot_home_vs_away_difference(self):
        self.plot_metric_bar_chart(
            data_func=lambda team: self.stat_tracker.team_home_stats[team]["PTS"] - self.stat_tracker.team_away_stats[team]["PTS"],
            title="Bundesliga: Heim-/Auswärtsdifferenz",
            ylabel="Heimpunkte – Auswärtspunkte",
            colormap="RdBu_r",
            vcenter=0,
            ref_line=0
        )


    def plot_avg_possession(self):
        self.plot_metric_bar_chart(
            data_func=lambda team: np.mean(self.stat_tracker.team_possession[team]),
            title="Ballbesitz – Durchschnitt pro Team",
            ylabel="Ballbesitz in %",
            colormap="RdYlGn",
            vcenter=50,
            ylim=(-30, 30),
            ref_line=50,  # Wichtig: visuelle Linie
            ref_label="Ø 50%"
        )
        

    def plot_avg_shots(self):
        league_avg = np.mean([
            np.mean(self.stat_tracker.team_shots[team])
            for team in self.tabellen_df["Team"]
        ])
        self.plot_metric_bar_chart(
            data_func=lambda team: np.mean(self.stat_tracker.team_shots[team]),
            title="Schüsse – Durchschnitt pro Spiel",
            ylabel="Schüsse pro Spiel",
            colormap="RdYlGn",
            vcenter=league_avg,
            ref_line=league_avg,
            ref_label=f"Ø {league_avg:.1f}"
        )
        
    def plot_scatter_with_logos(
        self,
        x_data_func,
        y_data_func,
        title,
        xlabel,
        ylabel,
        show_regression=False,
        show_background=False,
        background_cmap="RdBu_r",
        background_label=None
    ):
        teams = self.tabellen_df["Team"].tolist()
        x_vals = np.array([x_data_func(team) for team in teams])
        y_vals = np.array([y_data_func(team) for team in teams])
    
        fig, ax = plt.subplots(figsize=(12, 8))
    
        # 🔲 Hintergrund: Heatmap auf Basis von (y - x)
        if show_background:
            xi, yi = np.meshgrid(
                np.linspace(x_vals.min() - 5, x_vals.max() + 5, 300),
                np.linspace(y_vals.min() - 5, y_vals.max() + 5, 300)
            )
            zi = yi - xi
            norm = mcolors.TwoSlopeNorm(vmin=zi.min(), vcenter=0, vmax=zi.max())
            cmap = cm.get_cmap(background_cmap)
            ax.imshow(zi, origin="lower", extent=(xi.min(), xi.max(), yi.min(), yi.max()),
                      cmap=cmap, norm=norm, aspect='auto', alpha=0.3)
            cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
            if background_label:
                cbar.set_label(background_label)
    
        # ⚽ Teamlogos als Punkte
        for team, x, y in zip(teams, x_vals, y_vals):
            logo_path = self.tabellen_df[self.tabellen_df["Team"] == team]["WappenPfad"].values[0]
            if os.path.exists(logo_path):
                img = mpimg.imread(logo_path)
                imagebox = OffsetImage(img, zoom=0.6)
                ab = AnnotationBbox(imagebox, (x, y), frameon=False)
                ax.add_artist(ab)
            else:
                ax.plot(x, y, "o", label=team)
    
        # 📈 Regressionslinie
        if show_regression:
            model = LinearRegression().fit(x_vals.reshape(-1, 1), y_vals)
            x_fit = np.linspace(x_vals.min(), x_vals.max(), 100)
            y_fit = model.predict(x_fit.reshape(-1, 1))
            ax.plot(x_fit, y_fit, "k--", label=f"y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}")
            ax.legend()
    
        # ➖ Diagonale (Heim = Auswärts)
        ax.plot([x_vals.min(), x_vals.max()], [x_vals.min(), x_vals.max()],
                linestyle="--", color="green", label="Heim = Auswärts")
        ax.legend(loc="upper left")
    
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.tight_layout()
        plt.show()
        

plotter = Plotter()
plot_helper = PlotHelper(stat_tracker, tabellen_df)


# 🔄 Aktuellen Spieltag als DataFrame vorbereiten
matchday_df = pd.DataFrame([
    {
        "Anpfiff": match.kickoff,
        "Heim": match.home_team.name,
        "Ergebnis": match.result_str(),
        "Auswärts": match.away_team.name,
        "Halbzeit": match.halftime_result
    }
    for match in schedule.current().matches
])

# 🕒 Zeitfenster extrahieren (z. B. Fr/Sa/So)
def extrahiere_zeitblock(anpfiff: str) -> str:
    if anpfiff.startswith("Fr"):
        return "Freitagabend"
    elif anpfiff.startswith("Sa 15:30"):
        return "Samstagnachmittag"
    elif anpfiff.startswith("Sa 18:30"):
        return "Samstagabend"
    elif anpfiff.startswith("So 15:30"):
        return "Sonntagnachmittag"
    elif anpfiff.startswith("So 17:30"):
        return "Sonntagabend"
    return "Unbekannt"

zeitblock_series = matchday_df["Anpfiff"].apply(extrahiere_zeitblock)


team_df, _ = preprocessor.prepare_simulation_data(tabellen_df, goals_df, spieler_df)


plotter.plot_matchday_games(matchday_df, "Spieltag 1", tabellen_df, block_column=zeitblock_series)
plotter.plot_table(league_table.get_table(), "Tabelle nach Spieltag 1", tabellen_df)

plotter.plot_goalgetter(stat_tracker, tabellen_df, spieler_df)
plotter.plot_yellow_cards(stat_tracker, tabellen_df, spieler_df)
plotter.plot_sending_offs(stat_tracker, tabellen_df, spieler_df)





class Simulator:
    def __init__(self, schedule, stat_tracker, plotter, league_table, tabellen_df, spieler_df, team_df, team_colors):
        self.schedule = schedule
        self.stat_tracker = stat_tracker
        self.plotter = plotter
        self.league_table = league_table
        self.tabellen_df = tabellen_df
        self.spieler_df = spieler_df
        self.team_df = team_df 
        self.team_colors = team_colors

    def simulate_matchday(self):
        matchday = self.schedule.current()
        for match in matchday.matches:
            self.simulate_match(match, mode="fast")

        self.show_matchday_results(matchday)
        self.show_current_table()
        self.show_top_scorers()
        self.show_card_stats()
        self.schedule.next()

    def simulate_match(self, match, mode="fast"):
        self._run_match_logic(match)

        if mode == "fast":
            self._simulate_match_fast(match)
        elif mode == "live":
            self._simulate_match_live(match)
        else:
            raise ValueError("Unknown mode: choose 'fast' or 'live'")

        self.stat_tracker.update_after_match(match)

    def _run_match_logic(self, match):
        """
        Vollständige Spielsimulation für ein einzelnes Match.
        - Poisson-Tore
        - Karten (inkl. Gelb-Rot)
        - dynamischer Ballbesitz
        - Schüsse + xG
        - Ereignislog
        Speichert Ergebnis direkt in `match`-Objekt.
        """
    
        # Teams
        home = match.home_team.name
        away = match.away_team.name
    
        # Team Stats laden
        home_stats = self._get_team_stats(home)
        away_stats = self._get_team_stats(away)
    
        # Startelfs
        starting_eleven_home = self._choose_starting_eleven(home)
        starting_eleven_away = self._choose_starting_eleven(away)
    
        # Karten
        yellow_log, red_log, gelbrot_log, total_min = self._sample_cards(
            starting_eleven_home, starting_eleven_away
        )
    
        num_reds_home = len({s for s, _ in red_log + gelbrot_log if s in starting_eleven_home})
        num_reds_away = len({s for s, _ in red_log + gelbrot_log if s in starting_eleven_away})
    
        # Ratings angepasst
        xg_home, spg_home, poss_home, hr_adj = self._adjust_for_red_cards(
            home_stats["XG"], home_stats["SHOTS_PER_GAME"], home_stats["AVG_POSS"], home_stats["Heim_Rating"], num_reds_home
        )
        xg_away, spg_away, poss_away, ar_adj = self._adjust_for_red_cards(
            away_stats["XG"], away_stats["SHOTS_PER_GAME"], away_stats["AVG_POSS"], away_stats["Auswärts_Rating"], num_reds_away
        )
    
        # Ballbesitzverlauf
        poss_series = self._generate_possession_series(hr_adj, ar_adj, total_min, num_reds_home, num_reds_away)
    
        # Tore per Poisson
        mu_home = self._simulate_poisson_score(hr_adj, ar_adj, home_stats["Goal_Rating"], away_stats["GoalA_Rating"])
        mu_away = self._simulate_poisson_score(ar_adj, hr_adj, away_stats["Goal_Rating"], home_stats["GoalA_Rating"])
        gh, ga = np.random.poisson(mu_home), np.random.poisson(mu_away)
    
        # Torzeitpunkte
        tor_minuten = sorted(np.random.choice(range(1, total_min + 1), gh + ga, replace=False))
    
        # Torschützen
        def assign_goals(n, team_name, elf):
            log = []
            scorer_df = self.spieler_df[self.spieler_df["NAME"].isin(elf)].copy()
            scorer_df["goal_rate"] = scorer_df["GOALS"].clip(lower=0.001)
            weights = scorer_df["goal_rate"] / scorer_df["goal_rate"].sum()
            for m in n:
                scorer = np.random.choice(scorer_df["NAME"], p=weights)
                log.append((team_name, scorer, m, 0, 0))
            return log
    
        goal_log = (
            assign_goals(tor_minuten[:gh], home, starting_eleven_home) +
            assign_goals(tor_minuten[gh:], away, starting_eleven_away)
        )
        
    
        # Schüsse + xG
        def sample_xg_beta(mean_xg, n):
            var = 0.01
            alpha = ((1 - mean_xg) / var - 1 / mean_xg) * mean_xg**2
            beta_val = alpha * (1 / mean_xg - 1)
            return beta.rvs(alpha, beta_val, size=n).clip(0.02, 0.95)
    
        mu_shots_home = np.sqrt(spg_home * away_stats["SHOTS_A_PER_GAME"])
        mu_shots_away = np.sqrt(spg_away * home_stats["SHOTS_A_PER_GAME"])
    
        n_shots_home = np.random.poisson(mu_shots_home)
        n_shots_away = np.random.poisson(mu_shots_away)
    
        shot_min_home = sorted(np.random.choice(range(1, total_min + 1), n_shots_home, replace=False))
        shot_min_away = sorted(np.random.choice(range(1, total_min + 1), n_shots_away, replace=False))
    
        xg_shots_home = sample_xg_beta(home_stats["XG_PER_SHOT"], len(shot_min_home))
        xg_shots_away = sample_xg_beta(away_stats["XG_PER_SHOT"], len(shot_min_away))
    
        # Halbzeitergebnis
        hz_home = sum(1 for t, _, m, _, _ in goal_log if t == home and m <= 45)
        hz_away = sum(1 for t, _, m, _, _ in goal_log if t == away and m <= 45)
        
        
                # Karten als Events in goal_log hinzufügen
        for spieler, minute in yellow_log:
            goal_log.append((home if spieler in starting_eleven_home else away, spieler, minute, False, True))
        
        for spieler, minute in red_log:
            goal_log.append((home if spieler in starting_eleven_home else away, spieler, minute, True, False))
        
        for spieler, minute in gelbrot_log:
            goal_log.append((home if spieler in starting_eleven_home else away, spieler, minute, True, True))
        
        # Jetzt alle Events nach Minute sortieren
        goal_log.sort(key=lambda x: x[2])
        
    
        # Speichern ins Match-Objekt
        match.home_goals = gh
        match.away_goals = ga
        match.goal_log = goal_log
        match.halftime_result = f"{hz_home}:{hz_away}"
        match.yellow_card_log = yellow_log
        match.red_card_log = red_log
        match.gelbrot_card_log = gelbrot_log
        match.live_possession_home = poss_series
        match.shot_min_home = shot_min_home
        match.shot_min_away = shot_min_away
        match.xg_shots_home = xg_shots_home
        match.xg_shots_away = xg_shots_away
        match.starting_eleven_home = starting_eleven_home
        match.starting_eleven_away = starting_eleven_away
        
                
    def _adjust_for_red_cards(self, xg, spg, poss, rating, red_count, base=0.7, decay=0.6):
        if red_count == 0:
            return xg, spg, poss, rating
        factor = base * (decay ** (red_count - 1))
        return xg * factor, spg * factor, poss * factor, rating * factor
    
    def _generate_possession_series(self, home_rating, away_rating, length=90, red_cards_home=0, red_cards_away=0, smoothing=6):
        rating_ratio = home_rating / (home_rating + away_rating)
        card_shift = 0.2 * (red_cards_away - red_cards_home)
        shift_strength = (rating_ratio - 0.5 + card_shift) * 1.4
        base_home = 50 + shift_strength * 50
    
        noise = np.random.normal(0, 12, size=length)
        smoothed = np.convolve(noise, np.ones(smoothing) / smoothing, mode="same")
    
        series = base_home + smoothed
        lower = max(15, base_home - 40)
        upper = min(90, base_home + 40)
    
        return np.clip(series, lower, upper)
    
    def _sample_cards(self, starting_eleven_home, starting_eleven_away):
        from numpy.random import choice, rand, normal
    
        yellow_log = []
        red_log = []
        gelbrot_log = []
    
        def sample_team_cards(team_elf):
            team_yellow = []
            team_red = []
            team_gelbrot = []
        
            seen_yellow = set()
            seen_yellowred = set()
        
            for player in team_elf:
                row = self.spieler_df[self.spieler_df["NAME"] == player]
                if row.empty:
                    continue
            
                yellow_p = row["yellow_card_rating"].values[0] * np.random.uniform(1.1, 1.3)
                red_p = row["red_card_rating"].values[0]
            
                # Gelbe Karte
                if rand() < yellow_p:
                    minute = np.random.randint(1, 91)
                    team_yellow.append((player, minute))
            
                    # Prüfe auf Gelb-Rot
                    if rand() < 0.08 and minute + 1 < 91:
                        minute2 = np.random.randint(minute + 1, 91)
                        # ⛔ NICHT nochmal gelb hinzufügen!
                        # ✅ Stattdessen nur Gelb-Rot loggen
                        team_gelbrot.append((player, minute2))
            
                # Direkte Rote Karte
                if rand() < red_p:
                    minute = np.random.randint(1, 91)
                    team_red.append((player, minute))
        
            return team_yellow, team_red, team_gelbrot
    
        yh, rh, grh = sample_team_cards(starting_eleven_home)
        ya, ra, gra = sample_team_cards(starting_eleven_away)
        
                # Spieler mit Platzverweis entfernen
        sent_off = {s for s, _ in red_log + gelbrot_log}
        starting_eleven_home = [p for p in starting_eleven_home if p not in sent_off]
        starting_eleven_away = [p for p in starting_eleven_away if p not in sent_off]
    
        yellow_log.extend(yh + ya)
        red_log.extend(rh + ra)
        gelbrot_log.extend(grh + gra)
    
        self.first_half_extra = int(np.clip(np.random.normal(1.0, 0.3), 0, 3))
        self.second_half_extra = int(np.clip(np.random.normal(3.0, 1.0), 1, 6))
        
        total_min = 45 + self.first_half_extra + 45 + self.second_half_extra
        return yellow_log, red_log, gelbrot_log, total_min
    
    def _render_stats_table(self, stats: list[tuple[str, float, float, bool]], home_team: str, away_team: str) -> Table:
        from rich.table import Table
        from rich.text import Text
    
        home_color = self.team_colors.get_primary(home_team)
        away_color = self.team_colors.get_primary(away_team)
        bar_width = 21
    
        def make_bar(value, total, is_home):
            filled = int(bar_width * (value / total))
            empty = bar_width - filled
            if is_home:
                bar = " " * empty + "█" * filled
            else:
                bar = "█" * filled + " " * empty
            return f"[{bar}]"
    
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="left")
        table.add_column(justify="right")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="center")
        table.add_column(justify="left")
    
        for label, home_val, away_val, is_percent in stats:
            total = max(home_val + away_val, 1e-6)
            home_bar = make_bar(home_val, total, is_home=True)
            away_bar = make_bar(away_val, total, is_home=False)
    
            home_text = f"{home_val:.1f}%" if is_percent else f"{home_val:.2f}" if label == "xG" else str(int(home_val))
            away_text = f"{away_val:.1f}%" if is_percent else f"{away_val:.2f}" if label == "xG" else str(int(away_val))
    
            if home_color == away_color:
                away_color = self.team_colors.get_secondary(away_team)
    
            table.add_row(
                Text(f"{label}:", style="bold"),
                Text(home_bar, style=home_color),
                Text(home_text),
                Text("–", style="dim"),
                Text(away_text),
                Text(away_bar, style=away_color)
            )
    
        return table
    
    def _ereignis_table_columns(self, match):
        """Berechnet dynamisch die Spaltenstruktur basierend auf Spielernamen."""
        # Alle Spielernamen aus Toren & Karten
        names_home = [p for team, p, *_ in match.goal_log if team == match.home_team.name]
        names_away = [p for team, p, *_ in match.goal_log if team == match.away_team.name]
    
        # Länge berechnen
        max_name_len = max(
            max((len(n) for n in names_home), default=0),
            max((len(n) for n in names_away), default=0)
        )
    
        # Dynamische Breite (mit Begrenzung)
        name_col_width = min(max(max_name_len + 2, 18), 28)  # mindestens 18, maximal 28
    
        # ⬇️ Gib Spaltenliste zurück
        return [
            {"justify": "left", "width": 6},               # Heim Minute
            {"justify": "center", "width": 6},             # Heim Emoji
            {"justify": "left", "width": name_col_width},  # Heim Spieler
            {"justify": "right", "width": name_col_width},             # Mitte
            {"justify": "right", "width": 3}, # Auswärts Spieler ✅ gleich breit
            {"justify": "center", "width": 6},             # Auswärts Emoji
            {"justify": "right", "width": 6},              # Auswärts Minute
        ]
        
    
    def _build_layout(self, minute, match, halbzeit=False) -> Group:

        def minute_to_text(m):
            if m <= 45:
                return f"{m}."
            elif m <= 45 + self.first_half_extra:
                return f"45+{m - 45}"
            elif m <= 90:
                return f"{m}."
            else:
                return f"90+{m - 90}"
    
        home = match.home_team.name
        away = match.away_team.name
        tor_log = match.goal_log
        xg_shots_home = match.xg_shots_home
        xg_shots_away = match.xg_shots_away
        shot_min_home = match.shot_min_home
        shot_min_away = match.shot_min_away
        poss_series = match.live_possession_home
    
        gh = sum(1 for t, _, m, r, y in tor_log if t == home and m <= minute and not r and not y)
        ga = sum(1 for t, _, m, r, y in tor_log if t == away and m <= minute and not r and not y)
    
        score_table = Table.grid(expand=True)
        score_table.add_column(justify="right", ratio=1)      # Heimteam
        score_table.add_column(justify="center", ratio=1)     # Spielstand
        score_table.add_column(justify="left", ratio=1)       # Auswärtsteam
        score_table.add_column(justify="right", ratio=0.7)      # Halbzeitstand
        
        # Halbzeit-String
        hz_str = f"({match.halftime_result})" if match.halftime_result else ""
        
        score_table.add_row(
            Text(home),
            Text(f"{gh} : {ga}", style="magenta" if not halbzeit else ""),
            Text(away),
            Text(hz_str, style="dim")
        )
        spielstand_panel = Panel(score_table, title=f"Spielminute: {minute_to_text(minute)}", expand=True, width=80)    
        stats_table = self._render_stats_table(
            stats=[
                ("Tore", gh, ga, False),
                ("xG", sum(x for m, x in zip(shot_min_home, xg_shots_home) if m <= minute),
                       sum(x for m, x in zip(shot_min_away, xg_shots_away) if m <= minute), False),
                ("Schüsse", sum(1 for m in shot_min_home if m <= minute),
                            sum(1 for m in shot_min_away if m <= minute), False),
                ("Ballbesitz", poss_series[minute - 1], 100 - poss_series[minute - 1], True),
                ("Gelbe Karten",
                 sum(1 for t, _, m, r, y in tor_log if t == home and y and not r and m <= minute),
                 sum(1 for t, _, m, r, y in tor_log if t == away and y and not r and m <= minute),
                 False),
            ],
            home_team=home,
            away_team=away
        )
    
        stats_panel = Panel(stats_table, title="Live-Statistiken", expand=True, width=80)
    
        ereignisse = []
        
        home_score = 0
        away_score = 0
        
        for team, player, min, red, yellow in sorted([e for e in tor_log if e[2] <= minute], key=lambda x: x[2]):
            minute_str = minute_to_text(min)
        
            if not red and not yellow:
                if team == home:
                    home_score += 1
                else:
                    away_score += 1
                emoji = Text(f"{home_score}:{away_score}", style="bold white")
            elif red and yellow:
                emoji = Text("▉", style="bold yellow") + Text("▉", style="bold red")
            elif red:
                emoji = Text("▉", style="bold red")
            elif yellow:
                emoji = Text("▉", style="bold yellow")
        
            if team == home:
                ereignisse.append((minute_str, emoji, Text(player), "", "", ""))
            else:
                ereignisse.append(("", "", "", Text(player, justify="right"), emoji, minute_str))
        
        ereignis_table = Table.grid(expand=True)
        
        # 6 Spalten mit ratio=1 → gleich breit
        ereignis_table.add_column(justify="left", ratio=0.3)   # Spalte 1: Heim-Minute
        ereignis_table.add_column(justify="left", ratio=0.3)  # Spalte 2: Heim-Emoji
        ereignis_table.add_column(justify="left", ratio=1)    # Spalte 3: Heim-Spielername
        ereignis_table.add_column(justify="right", ratio=1)   # Spalte 4: Auswärts-Spielername
        ereignis_table.add_column(justify="right", ratio=0.3)  # Spalte 5: Auswärts-Emoji
        ereignis_table.add_column(justify="right", ratio=0.3)    # Spalte 6: Auswärts-Minute ✅ wie gewünscht
        
        # 4. Füge Zeilen hinzu
        for row in ereignisse:
            ereignis_table.add_row(*row)    
        # 5. Packe in Panel
        ereignis_panel = Panel(ereignis_table, title="Tore & Karten",box=box.DOUBLE_EDGE, expand=True, width=80)
        return Group(
            Align.center(spielstand_panel),
            Align.center(ereignis_panel),
            Align.center(stats_panel)
        )
    
    def _simulate_match_fast(self, match):
        from rich.console import Console
        from rich.align import Align
    
        last_minute = 90 + self.second_half_extra  # Falls du die Nachspielzeit wie oben integriert hast
        layout = self._build_layout(minute=last_minute, match=match)
        Console().print(layout)

    def _simulate_match_live(self, match):
        from rich.live import Live
        from rich.console import Console
        from rich.align import Align
        import time
        
        print(f"\nLIVE: {match.home_team.name} vs {match.away_team.name}")
        
        with Live(refresh_per_second=30) as live:
            for minute in range(1, len(match.live_possession_home) + 1):
                layout = self._build_layout(minute=minute, match=match)
                live.update(Align.center(layout))
                time.sleep(0.5)  # 👈 Geschwindigkeit anpassbar
        
        print(f"\n📊 Endstand: {match.result_str()}")

    def show_matchday_results(self, matchday):
        df = self._build_matchday_df(matchday)
        zeitblock_series = df["Anpfiff"].apply(self._extrahiere_zeitblock)
        self.plotter.plot_matchday_games(df, f"📅 Spieltag {matchday.number}", self.tabellen_df, zeitblock_series)

    def show_current_table(self):
        df = self.league_table.get_table()
        self.plotter.plot_table(df, "📊 Tabelle", self.tabellen_df)

    def show_top_scorers(self):
        self.plotter.plot_goalgetter(self.stat_tracker, self.tabellen_df, self.spieler_df)

    def show_card_stats(self, stat=None):
        if stat == "yellow":
            self.plotter.plot_yellow_cards(self.stat_tracker, self.tabellen_df, self.spieler_df)
        elif stat == "sending_off":
            self.plotter.plot_sending_offs(self.stat_tracker, self.tabellen_df, self.spieler_df)
        else:
            # Standardverhalten: beides
            self.plotter.plot_yellow_cards(self.stat_tracker, self.tabellen_df, self.spieler_df)
            self.plotter.plot_sending_offs(self.stat_tracker, self.tabellen_df, self.spieler_df)
        
    def _build_matchday_df(self, matchday):
        """
        🔄 Nutze Matchday-Objekt, um DataFrame mit Ergebnissen zu erzeugen.
        """
        return pd.DataFrame([
            {
                "Anpfiff": match.kickoff,
                "Heim": match.home_team.name,
                "Ergebnis": match.result_str(),
                "Auswärts": match.away_team.name,
                "Halbzeit": match.halftime_result
            }
            for match in matchday.matches
        ])

    def _extrahiere_zeitblock(self, anpfiff):
        if anpfiff.startswith("Fr"):
            return "Freitagabend"
        elif anpfiff.startswith("Sa 15:30"):
            return "Samstagnachmittag"
        elif anpfiff.startswith("Sa 18:30"):
            return "Samstagabend"
        elif anpfiff.startswith("So 15:30"):
            return "Sonntagnachmittag"
        elif anpfiff.startswith("So 17:30"):
            return "Sonntagabend"
        return "Unbekannt"
    
    def _get_team_stats(self, team_name: str) -> dict:
        row = self.team_df[self.team_df["Team"] == team_name]
        if row.empty:
            raise ValueError(f"Team '{team_name}' nicht gefunden.")
        row = row.iloc[0]
        return {
            "Heim_Rating": row["Heim_Rating"],
            "Auswärts_Rating": row["Auswärts_Rating"],
            "Goal_Rating": row["Goal_Rating"],
            "GoalA_Rating": row["GoalA_Rating"],
            "AVG_POSS": row["AVG_POSS"],
            "XG": row["XG"],
            "XGA": row["XGA"],
            "SHOTS_PER_GAME": row["SHOTS_PER_GAME"],
            "SHOTS_A_PER_GAME": row["SHOTS_A_PER_GAME"],
            "XG_PER_SHOT": row["XG_PER_SHOT"]
        }
    
    def _simulate_poisson_score(self, hr, ar, gr, gar):
        base_mu = np.random.uniform(0.9, 1.3)
        return base_mu * np.sqrt(hr / ar) * np.sqrt(gr / gar)
    
    def _choose_starting_eleven(self, team_name: str):
        df = self.spieler_df[self.spieler_df["Team"] == team_name].copy()
        df["Gewichtung"] = df["Spielzeit_Rating"].clip(lower=0.001)
        return df.sample(n=11, weights="Gewichtung", replace=False)["NAME"].tolist()
    
    def simulate_match_silent(self, match):
        self._run_match_logic(match)
        self.stat_tracker.update_after_match(match)
    
    


class TeamColorManager:
    def __init__(self, color_config: dict):
        self.color_config = color_config

    def get_primary(self, team: str) -> str:
        return self.color_config.get(team, {}).get("primary", "cyan")

    def get_secondary(self, team: str) -> str:
        return self.color_config.get(team, {}).get("secondary", "magenta")
    

team_colors = TeamColorManager({
    "Bayern München": {"primary": "red", "secondary": "white"},
    "Borussia Dortmund": {"primary": "yellow", "secondary": "black"},
    "RB Leipzig": {"primary": "white", "secondary": "red"},
    "Eintracht Frankfurt": {"primary": "red", "secondary": "white"},
    "VfB Stuttgart": {"primary": "white", "secondary": "red"},
    "Bayer 04 Leverkusen": {"primary": "red", "secondary": "bright_black"},
    "Bor. Mönchengladbach": {"primary": "white", "secondary": "green"},
    "Werder Bremen": {"primary": "green", "secondary": "bright_black"},
    "1. FSV Mainz 05": {"primary": "red", "secondary": "blue"},
    "VfL Wolfsburg": {"primary": "green", "secondary": "white"},
    "SC Freiburg": {"primary": "red", "secondary": "bright_black"},
    "TSG Hoffenheim": {"primary": "cyan", "secondary": "white"},
    "VfL Bochum": {"primary": "cyan", "secondary": "white"},
    "Holstein Kiel": {"primary": "cyan", "secondary": "white"},
    "1. FC Heidenheim": {"primary": "red", "secondary": "blue"},
    "1. FC Union Berlin": {"primary": "red", "secondary": "white"},
    "FC St. Pauli": {"primary": "#8B4513", "secondary": "white"},
    "FC Augsburg": {"primary": "white", "secondary": "#8B0000"},
})



simulator = Simulator(
    schedule=schedule,
    stat_tracker=stat_tracker,
    plotter=plotter,
    league_table=league_table,
    tabellen_df=tabellen_df,
    spieler_df=spieler_df,
    team_df=team_df,  # ✅ Jetzt korrekt
    team_colors=team_colors
)

simulator.simulate_matchday()

        

class SeasonRunner:
    def __init__(self, simulator, stat_tracker, schedule, league_table, spieler_df, tabellen_df, plotter, plot_helper):
        self.simulator = simulator
        self.stat_tracker = stat_tracker
        self.schedule = schedule
        self.league_table = league_table
        self.spieler_df = spieler_df
        self.tabellen_df = tabellen_df
        self.plotter = plotter
        self.plot_helper = PlotHelper(stat_tracker, tabellen_df)
        self.should_exit = False

    def run(self):
        while self.schedule.current_index < len(self.schedule.matchdays) and not self.should_exit:
            matchday = self.schedule.current()
            self.simulate_matchday_interactive(matchday)
            if self.should_exit:
                print("🏁 Simulation beendet.")
                return
    
            # 📊 Nach dem Spieltag: Ergebnisse & Statistiken
            print(f"\n✅ Spieltag {matchday.number} abgeschlossen.")
            input("📊 Drücke ENTER für die Ergebnisübersicht...")
            self.simulator.show_matchday_results(matchday)
            
            input("📊 Drücke ENTER für die aktuelle Tabelle...")
            self.simulator.show_current_table()
            
            input("📊 Drücke ENTER für die Torjägerliste...")
            self.simulator.show_top_scorers()
            
            input("📊 Drücke ENTER für die Liste der Gelben Karten...")
            self.simulator.show_card_stats(stat="yellow")
            
            input("📊 Drücke ENTER für die Liste der Platzverweise...")
            self.simulator.show_card_stats(stat="sending_off")
    
            # 🧭 Spieltags-Menü
            while True:
                choice = input("Optionen: [n] Nächster Spieltag | [f] Saison fast | [r] Reset | [q] Quit | [h] Heim/Auswärts | [o] Formtabelle | [p] Ballbesitz | [s] Schüsse: ").lower()
    
                if choice == "n":
                    input("🔜 Drücke ENTER für Vorschau...")
                    next_md = self.schedule.next()
                    if next_md is None:
                        print("✅ Saison abgeschlossen.")
                        self._post_season_prompt()
                        return
                    self.plot_matchday_preview(next_md)
    
                    sub = input("🎮 Spieltag starten? [a] Alle fast | [s] Spielweise wählen: ").lower()
                    if sub == "a":
                        for match in next_md.matches:
                            self.simulator.simulate_match(match, "fast")
                            self.stat_tracker.update_after_match(match)
                    
                        print(f"✅ Spieltag {next_md.number} abgeschlossen.")
                        input("➡️  Drücke ENTER für die Ergebnisübersicht...")
                        self.simulator.show_matchday_results(next_md)
                    
                        input("➡️  Drücke ENTER für die Tabelle...")
                        self.simulator.show_current_table()
                    
                        input("➡️  Drücke ENTER für die Torjägerliste...")
                        self.simulator.show_top_scorers()
                    
                        input("➡️  Drücke ENTER für die Liste der Gelben Karten...")
                        self.simulator.show_card_stats(stat="yellow")
                    
                        input("➡️  Drücke ENTER für die Liste der Platzverweise...")
                        self.simulator.show_card_stats(stat="sending_off")
                    
                        break  # 🔁 zurück in den Hauptloop
                    elif sub == "s":
                        self.simulate_matchday_interactive(next_md)
                        # und dann wieder ins Menü
                        self.simulator.show_matchday_results(next_md)
                        self.simulator.show_current_table()
                        self.simulator.show_top_scorers()
                        self.simulator.show_card_stats()
                        continue
                    else:
                        print("Ungültige Eingabe.")
                elif choice == "f":
                    self.simulate_season_fast()
                    self._post_season_prompt()
                    return
                elif choice == "r":
                    if self.reset_simulation():
                        return
                elif choice == "q":
                    self.should_exit = True
                    print("🏁 Simulation beendet.")
                    return
                elif choice == "h":
                    self.plot_helper.plot_home_vs_away_difference()
                elif choice == "o":
                    self.plot_helper.plot_form_table()
                elif choice == "p":
                    self.plot_helper.plot_avg_possession()
                elif choice == "s":
                    self.plot_helper.plot_avg_shots()
                else:
                    print("Ungültige Eingabe.")

    def simulate_matchday_interactive(self, matchday):
        for match in matchday.matches:
            while True:
                print(f"\n🎮 Spiel: {match.home_team.name} vs {match.away_team.name}")
                option = input("Optionen: [f] Fast | [l] Live | [s] Skip | [t] Tabelle | [r] Reset | [q] Beenden: ").lower()
    
                if option == "f":
                    self.simulator.simulate_match(match, "fast")
                    break
                elif option == "l":
                    self.simulator.simulate_match(match, "live")
                    break
                elif option == "s":
                    break
                elif option == "t":
                    self.simulator.show_current_table()
                elif option == "r":
                    if self.reset_simulation():
                        return  # Restart
                elif option == "q":
                    self.should_exit = True
                    return


    def simulate_season_fast(self):
        while self.schedule.current_index < len(self.schedule.matchdays):
            matchday = self.schedule.current()
            for match in matchday.matches:
                self.simulator.simulate_match_silent(match)
            self.schedule.next()
    
        # ✅ Nur hier Ausgabe
        last_matchday = self.schedule.matchdays[-1]
        self.simulator.show_matchday_results(last_matchday)
        self.simulator.show_current_table()
        self.simulator.show_top_scorers()
        self.simulator.show_card_stats()

    def reset_simulation(self) -> bool:
        print("\n🔄 Simulation wird zurückgesetzt...")
        self.stat_tracker.initialize(self.tabellen_df["Team"].tolist(), self.spieler_df)
        self.schedule.reset()
        # Du musst hier auch alle Spiele "zurücksetzen", falls du z. B. in Match Objekten Tore gespeichert hast
        for matchday in self.schedule.matchdays:
            for match in matchday.matches:
                match.home_goals = None
                match.away_goals = None
                match.goal_log.clear()
                match.yellow_card_log.clear()
                match.red_card_log.clear()
                match.yellowred_card_log.clear()

        while True:
            choice = input("🔁 Neu starten? [y] Ja | [q] Beenden: ").lower()
            if choice == "y":
                self.run()
                return True
            elif choice == "q":
                print("🏁 Saison beendet.")
                return False
            else:
                print("Ungültige Eingabe.")

    def _post_season_prompt(self):
        while True:
            choice = input("\n🔁 [r] Reset & Neustart | [q] Beenden: ").lower()
            if choice == "r":
                if self.reset_simulation():
                    return
            elif choice == "q":
                self.should_exit = True
                print("🏁 Simulation beendet.")
                return
            else:
                print("Ungültige Eingabe.")
                
    
    def plot_matchday_preview(self, matchday):
        preview_df = pd.DataFrame([
            {
                "Anpfiff": match.kickoff,
                "Heim": match.home_team.name,
                "Ergebnis": "- : -",
                "Auswärts": match.away_team.name,
                "Halbzeit": "(- : -)"
            }
            for match in matchday.matches
        ])
        zeitblock_series = preview_df["Anpfiff"].apply(self.simulator._extrahiere_zeitblock)
        self.plotter.plot_matchday_games(preview_df, f"🔮 Vorschau Spieltag {matchday.number}", self.tabellen_df, zeitblock_series)
    

runner = SeasonRunner(
    simulator=simulator,
    stat_tracker=stat_tracker,
    schedule=schedule,
    league_table=league_table,
    spieler_df=spieler_df,
    tabellen_df=tabellen_df,
    plotter=plotter,
    plot_helper=plot_helper
)








        