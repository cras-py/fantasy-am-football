"""
Fantasy Football 2026-2027 - Player Database & Projections
===========================================================
ESPN League 756823 | Half PPR | 4pt Passing TDs

Contains ~175 player projections based on 2026 consensus rankings
(FantasyPros, CBS, PFF, NBC Sports - July 2026).

Scoring:
  Passing:  1pt per 25 yds, 4pt TD, -2 INT, 2pt 2PC
  Rushing:  1pt per 10 yds, 6pt TD, 2pt 2PC
  Receiving: 0.5pt per reception, 1pt per 10 yds, 6pt TD, 2pt 2PC
  Kicking:  FG 0-39 = 3pt, FG 40-49 = 4pt, FG 50+ = 5pt, PAT = 1pt, Miss = -1pt
  Defense:  Sack 1pt, INT 2pt, FR 2pt, TD 6pt, Safety 2pt, PA tiers
  Misc:     Fumble Lost = -2pt

Usage:
  from player_data import get_all_players, get_players_by_position, calculate_fantasy_points
"""

# ---------------------------------------------------------------------------
# Scoring constants (ESPN League 756823, 2026 season)
# ---------------------------------------------------------------------------
SCORING = {
    "pass_yd_per_pt": 25,      # 1 point per 25 passing yards
    "pass_td": 4,
    "pass_int": -2,
    "pass_2pc": 2,
    "rush_yd_per_pt": 10,      # 1 point per 10 rushing yards
    "rush_td": 6,
    "rush_2pc": 2,
    "rec_ppr": 0.5,            # Half PPR
    "rec_yd_per_pt": 10,       # 1 point per 10 receiving yards
    "rec_td": 6,
    "rec_2pc": 2,
    "fumble_lost": -2,
    "fg_0_39": 3,
    "fg_40_49": 4,
    "fg_50_plus": 5,
    "pat": 1,
    "fg_miss": -1,
    "dst_sack": 1,
    "dst_int": 2,
    "dst_fr": 2,
    "dst_td": 6,
    "dst_safety": 2,
    "dst_pa_0": 5,
    "dst_pa_1_6": 4,
    "dst_pa_7_13": 3,
    "dst_pa_14_17": 1,
    "dst_pa_18_27": 0,
    "dst_pa_28_34": -1,
    "dst_pa_35_45": -3,
    "dst_pa_46_plus": -5,
}

# Roster requirements
ROSTER_REQUIREMENTS = {
    "QB": 2,
    "RB": 4,
    "WR": 5,
    "TE": 2,
    "DEF": 1,
    "K": 1,
}
TOTAL_ROSTER = sum(ROSTER_REQUIREMENTS.values())  # 15


def calculate_fantasy_points(player: dict) -> float:
    """Calculate projected Half-PPR fantasy points for a player based on their stats."""
    pos = player.get("pos", "")
    pts = 0.0

    if pos == "QB":
        pts += player.get("pass_yds", 0) / SCORING["pass_yd_per_pt"]
        pts += player.get("pass_tds", 0) * SCORING["pass_td"]
        pts += player.get("pass_ints", 0) * SCORING["pass_int"]
        pts += player.get("pass_2pc", 0) * SCORING["pass_2pc"]
        pts += player.get("rush_yds", 0) / SCORING["rush_yd_per_pt"]
        pts += player.get("rush_tds", 0) * SCORING["rush_td"]
        pts += player.get("fumbles_lost", 0) * SCORING["fumble_lost"]

    elif pos == "RB":
        pts += player.get("rush_yds", 0) / SCORING["rush_yd_per_pt"]
        pts += player.get("rush_tds", 0) * SCORING["rush_td"]
        pts += player.get("receptions", 0) * SCORING["rec_ppr"]
        pts += player.get("rec_yds", 0) / SCORING["rec_yd_per_pt"]
        pts += player.get("rec_tds", 0) * SCORING["rec_td"]
        pts += player.get("fumbles_lost", 0) * SCORING["fumble_lost"]

    elif pos == "WR":
        pts += player.get("receptions", 0) * SCORING["rec_ppr"]
        pts += player.get("rec_yds", 0) / SCORING["rec_yd_per_pt"]
        pts += player.get("rec_tds", 0) * SCORING["rec_td"]
        pts += player.get("rush_yds", 0) / SCORING["rush_yd_per_pt"]
        pts += player.get("rush_tds", 0) * SCORING["rush_td"]
        pts += player.get("fumbles_lost", 0) * SCORING["fumble_lost"]

    elif pos == "TE":
        pts += player.get("receptions", 0) * SCORING["rec_ppr"]
        pts += player.get("rec_yds", 0) / SCORING["rec_yd_per_pt"]
        pts += player.get("rec_tds", 0) * SCORING["rec_td"]
        pts += player.get("fumbles_lost", 0) * SCORING["fumble_lost"]

    elif pos == "K":
        pts += player.get("fg_0_39", 0) * SCORING["fg_0_39"]
        pts += player.get("fg_40_49", 0) * SCORING["fg_40_49"]
        pts += player.get("fg_50_plus", 0) * SCORING["fg_50_plus"]
        pts += player.get("pat", 0) * SCORING["pat"]
        pts += player.get("fg_miss", 0) * SCORING["fg_miss"]

    elif pos == "DEF":
        pts += player.get("sacks", 0) * SCORING["dst_sack"]
        pts += player.get("ints", 0) * SCORING["dst_int"]
        pts += player.get("fr", 0) * SCORING["dst_fr"]
        pts += player.get("tds", 0) * SCORING["dst_td"]
        pts += player.get("safeties", 0) * SCORING["dst_safety"]
        # Points-allowed tier projection (average weekly PA bucket * 17)
        pts += player.get("pa_pts", 0)

    return round(pts, 1)


# ---------------------------------------------------------------------------
# 2026 Player Projections Database
# ---------------------------------------------------------------------------
# Sources: FantasyPros ECR, CBS, PFF, NBC Sports consensus (July 2026)
# Stats are full-season projections (17 games)

_RAW_PLAYERS = [
    # =========================================================================
    # QUARTERBACKS (20)
    # =========================================================================
    {"name": "Josh Allen",         "team": "BUF", "pos": "QB", "bye": 11, "tier": 1,
     "pass_yds": 4350, "pass_tds": 32, "pass_ints": 10, "rush_yds": 620, "rush_tds": 7, "fumbles_lost": 4},
    {"name": "Lamar Jackson",      "team": "BAL", "pos": "QB", "bye": 14, "tier": 1,
     "pass_yds": 3900, "pass_tds": 28, "pass_ints": 8, "rush_yds": 800, "rush_tds": 6, "fumbles_lost": 5},
    {"name": "Jalen Hurts",        "team": "PHI", "pos": "QB", "bye": 5, "tier": 1,
     "pass_yds": 3750, "pass_tds": 25, "pass_ints": 9, "rush_yds": 650, "rush_tds": 10, "fumbles_lost": 5},
    {"name": "Joe Burrow",         "team": "CIN", "pos": "QB", "bye": 12, "tier": 2,
     "pass_yds": 4500, "pass_tds": 34, "pass_ints": 10, "rush_yds": 180, "rush_tds": 2, "fumbles_lost": 4},
    {"name": "Drake Maye",         "team": "NE",  "pos": "QB", "bye": 14, "tier": 2,
     "pass_yds": 4100, "pass_tds": 30, "pass_ints": 12, "rush_yds": 450, "rush_tds": 4, "fumbles_lost": 5},
    {"name": "Caleb Williams",     "team": "CHI", "pos": "QB", "bye": 7, "tier": 2,
     "pass_yds": 4200, "pass_tds": 29, "pass_ints": 11, "rush_yds": 380, "rush_tds": 4, "fumbles_lost": 4},
    {"name": "Jayden Daniels",     "team": "WAS", "pos": "QB", "bye": 14, "tier": 2,
     "pass_yds": 3800, "pass_tds": 24, "pass_ints": 9, "rush_yds": 700, "rush_tds": 6, "fumbles_lost": 5},
    {"name": "Justin Herbert",     "team": "LAC", "pos": "QB", "bye": 6, "tier": 3,
     "pass_yds": 4150, "pass_tds": 27, "pass_ints": 10, "rush_yds": 220, "rush_tds": 2, "fumbles_lost": 3},
    {"name": "Dak Prescott",       "team": "DAL", "pos": "QB", "bye": 7, "tier": 3,
     "pass_yds": 4100, "pass_tds": 28, "pass_ints": 11, "rush_yds": 180, "rush_tds": 2, "fumbles_lost": 4},
    {"name": "Trevor Lawrence",    "team": "JAX", "pos": "QB", "bye": 9, "tier": 3,
     "pass_yds": 4000, "pass_tds": 26, "pass_ints": 10, "rush_yds": 280, "rush_tds": 3, "fumbles_lost": 3},
    {"name": "Patrick Mahomes",    "team": "KC",  "pos": "QB", "bye": 6, "tier": 3,
     "pass_yds": 4200, "pass_tds": 27, "pass_ints": 11, "rush_yds": 250, "rush_tds": 2, "fumbles_lost": 3},
    {"name": "Brock Purdy",        "team": "SF",  "pos": "QB", "bye": 9, "tier": 4,
     "pass_yds": 4050, "pass_tds": 27, "pass_ints": 9, "rush_yds": 160, "rush_tds": 2, "fumbles_lost": 3},
    {"name": "Jared Goff",         "team": "DET", "pos": "QB", "bye": 5, "tier": 4,
     "pass_yds": 4300, "pass_tds": 28, "pass_ints": 10, "rush_yds": 60, "rush_tds": 1, "fumbles_lost": 3},
    {"name": "Anthony Richardson", "team": "IND", "pos": "QB", "bye": 14, "tier": 4,
     "pass_yds": 3400, "pass_tds": 22, "pass_ints": 12, "rush_yds": 650, "rush_tds": 6, "fumbles_lost": 6},
    {"name": "Kyler Murray",       "team": "ARI", "pos": "QB", "bye": 11, "tier": 4,
     "pass_yds": 3700, "pass_tds": 23, "pass_ints": 10, "rush_yds": 450, "rush_tds": 4, "fumbles_lost": 4},
    {"name": "Bo Nix",             "team": "DEN", "pos": "QB", "bye": 10, "tier": 5,
     "pass_yds": 3800, "pass_tds": 24, "pass_ints": 11, "rush_yds": 350, "rush_tds": 3, "fumbles_lost": 4},
    {"name": "Sam Darnold",        "team": "MIN", "pos": "QB", "bye": 8, "tier": 5,
     "pass_yds": 3900, "pass_tds": 25, "pass_ints": 12, "rush_yds": 120, "rush_tds": 1, "fumbles_lost": 4},
    {"name": "C.J. Stroud",        "team": "HOU", "pos": "QB", "bye": 13, "tier": 5,
     "pass_yds": 4000, "pass_tds": 25, "pass_ints": 9, "rush_yds": 200, "rush_tds": 2, "fumbles_lost": 3},
    {"name": "Matthew Stafford",   "team": "LAR", "pos": "QB", "bye": 6, "tier": 6,
     "pass_yds": 3900, "pass_tds": 24, "pass_ints": 10, "rush_yds": 60, "rush_tds": 1, "fumbles_lost": 3},
    {"name": "Aaron Rodgers",      "team": "NYJ", "pos": "QB", "bye": 12, "tier": 6,
     "pass_yds": 3600, "pass_tds": 23, "pass_ints": 9, "rush_yds": 80, "rush_tds": 1, "fumbles_lost": 3},

    # =========================================================================
    # RUNNING BACKS (40)
    # =========================================================================
    {"name": "Jahmyr Gibbs",       "team": "DET", "pos": "RB", "bye": 5, "tier": 1,
     "rush_yds": 1250, "rush_tds": 12, "receptions": 65, "rec_yds": 580, "rec_tds": 3, "fumbles_lost": 2},
    {"name": "Bijan Robinson",     "team": "ATL", "pos": "RB", "bye": 12, "tier": 1,
     "rush_yds": 1300, "rush_tds": 11, "receptions": 58, "rec_yds": 480, "rec_tds": 3, "fumbles_lost": 2},
    {"name": "Christian McCaffrey", "team": "SF", "pos": "RB", "bye": 9, "tier": 1,
     "rush_yds": 1100, "rush_tds": 10, "receptions": 75, "rec_yds": 550, "rec_tds": 3, "fumbles_lost": 2},
    {"name": "Jonathan Taylor",    "team": "IND", "pos": "RB", "bye": 14, "tier": 2,
     "rush_yds": 1200, "rush_tds": 11, "receptions": 38, "rec_yds": 310, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "James Cook III",     "team": "BUF", "pos": "RB", "bye": 11, "tier": 2,
     "rush_yds": 1100, "rush_tds": 10, "receptions": 45, "rec_yds": 380, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Ashton Jeanty",      "team": "LV",  "pos": "RB", "bye": 10, "tier": 2,
     "rush_yds": 1050, "rush_tds": 10, "receptions": 40, "rec_yds": 320, "rec_tds": 2, "fumbles_lost": 3},
    {"name": "Saquon Barkley",     "team": "PHI", "pos": "RB", "bye": 5, "tier": 2,
     "rush_yds": 1150, "rush_tds": 9, "receptions": 48, "rec_yds": 380, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "De'Von Achane",      "team": "MIA", "pos": "RB", "bye": 6, "tier": 2,
     "rush_yds": 1000, "rush_tds": 9, "receptions": 55, "rec_yds": 450, "rec_tds": 3, "fumbles_lost": 2},
    {"name": "Omarion Hampton",    "team": "LAC", "pos": "RB", "bye": 6, "tier": 3,
     "rush_yds": 1050, "rush_tds": 9, "receptions": 35, "rec_yds": 280, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Kenneth Walker III", "team": "KC",  "pos": "RB", "bye": 6, "tier": 3,
     "rush_yds": 1000, "rush_tds": 9, "receptions": 35, "rec_yds": 260, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Chase Brown",        "team": "CIN", "pos": "RB", "bye": 12, "tier": 3,
     "rush_yds": 950, "rush_tds": 8, "receptions": 45, "rec_yds": 380, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Derrick Henry",      "team": "BAL", "pos": "RB", "bye": 14, "tier": 3,
     "rush_yds": 1150, "rush_tds": 10, "receptions": 22, "rec_yds": 160, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Breece Hall",        "team": "NYJ", "pos": "RB", "bye": 12, "tier": 3,
     "rush_yds": 950, "rush_tds": 7, "receptions": 50, "rec_yds": 380, "rec_tds": 2, "fumbles_lost": 3},
    {"name": "Kyren Williams",     "team": "LAR", "pos": "RB", "bye": 6, "tier": 3,
     "rush_yds": 900, "rush_tds": 8, "receptions": 45, "rec_yds": 340, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Josh Jacobs",        "team": "GB",  "pos": "RB", "bye": 10, "tier": 4,
     "rush_yds": 1000, "rush_tds": 8, "receptions": 35, "rec_yds": 260, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Travis Etienne Jr.", "team": "NO",  "pos": "RB", "bye": 8, "tier": 4,
     "rush_yds": 900, "rush_tds": 7, "receptions": 40, "rec_yds": 320, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Javonte Williams",   "team": "DAL", "pos": "RB", "bye": 7, "tier": 4,
     "rush_yds": 850, "rush_tds": 7, "receptions": 42, "rec_yds": 340, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Bucky Irving",       "team": "TB",  "pos": "RB", "bye": 11, "tier": 4,
     "rush_yds": 950, "rush_tds": 8, "receptions": 30, "rec_yds": 230, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "TreVeyon Henderson", "team": "NE",  "pos": "RB", "bye": 14, "tier": 4,
     "rush_yds": 850, "rush_tds": 7, "receptions": 38, "rec_yds": 300, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Cam Skattebo",       "team": "NYG", "pos": "RB", "bye": 8, "tier": 4,
     "rush_yds": 800, "rush_tds": 7, "receptions": 45, "rec_yds": 350, "rec_tds": 2, "fumbles_lost": 3},
    {"name": "David Montgomery",   "team": "HOU", "pos": "RB", "bye": 13, "tier": 5,
     "rush_yds": 800, "rush_tds": 7, "receptions": 30, "rec_yds": 220, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Quinshon Judkins",   "team": "CLE", "pos": "RB", "bye": 10, "tier": 5,
     "rush_yds": 800, "rush_tds": 6, "receptions": 30, "rec_yds": 220, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "D'Andre Swift",      "team": "CHI", "pos": "RB", "bye": 7, "tier": 5,
     "rush_yds": 750, "rush_tds": 5, "receptions": 45, "rec_yds": 350, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Bhayshul Tuten",     "team": "JAX", "pos": "RB", "bye": 9, "tier": 5,
     "rush_yds": 800, "rush_tds": 6, "receptions": 28, "rec_yds": 200, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "RJ Harvey",          "team": "DEN", "pos": "RB", "bye": 10, "tier": 5,
     "rush_yds": 780, "rush_tds": 6, "receptions": 32, "rec_yds": 240, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Jaylen Warren",      "team": "PIT", "pos": "RB", "bye": 9, "tier": 5,
     "rush_yds": 700, "rush_tds": 5, "receptions": 45, "rec_yds": 350, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Chuba Hubbard",      "team": "CAR", "pos": "RB", "bye": 8, "tier": 5,
     "rush_yds": 850, "rush_tds": 6, "receptions": 28, "rec_yds": 200, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Rhamondre Stevenson","team": "NE",  "pos": "RB", "bye": 14, "tier": 6,
     "rush_yds": 700, "rush_tds": 5, "receptions": 35, "rec_yds": 260, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Jadarian Price",     "team": "SEA", "pos": "RB", "bye": 11, "tier": 6,
     "rush_yds": 720, "rush_tds": 5, "receptions": 32, "rec_yds": 240, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Tony Pollard",       "team": "TEN", "pos": "RB", "bye": 5, "tier": 6,
     "rush_yds": 750, "rush_tds": 5, "receptions": 30, "rec_yds": 220, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Najee Harris",       "team": "PIT", "pos": "RB", "bye": 9, "tier": 6,
     "rush_yds": 800, "rush_tds": 6, "receptions": 22, "rec_yds": 160, "rec_tds": 0, "fumbles_lost": 2},
    {"name": "Zach Charbonnet",    "team": "SEA", "pos": "RB", "bye": 11, "tier": 6,
     "rush_yds": 650, "rush_tds": 5, "receptions": 30, "rec_yds": 220, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Tyjae Spears",       "team": "TEN", "pos": "RB", "bye": 5, "tier": 6,
     "rush_yds": 600, "rush_tds": 4, "receptions": 40, "rec_yds": 300, "rec_tds": 2, "fumbles_lost": 2},
    {"name": "Rico Dowdle",        "team": "DAL", "pos": "RB", "bye": 7, "tier": 6,
     "rush_yds": 680, "rush_tds": 5, "receptions": 28, "rec_yds": 200, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Jerome Ford",        "team": "CLE", "pos": "RB", "bye": 10, "tier": 7,
     "rush_yds": 600, "rush_tds": 4, "receptions": 32, "rec_yds": 240, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Raheem Mostert",     "team": "MIA", "pos": "RB", "bye": 6, "tier": 7,
     "rush_yds": 550, "rush_tds": 5, "receptions": 22, "rec_yds": 160, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Deuce Vaughn",       "team": "ARI", "pos": "RB", "bye": 11, "tier": 7,
     "rush_yds": 550, "rush_tds": 4, "receptions": 35, "rec_yds": 260, "rec_tds": 1, "fumbles_lost": 2},
    {"name": "Alexander Mattison", "team": "LV",  "pos": "RB", "bye": 10, "tier": 7,
     "rush_yds": 500, "rush_tds": 4, "receptions": 25, "rec_yds": 180, "rec_tds": 1, "fumbles_lost": 1},
    {"name": "Ty Chandler",        "team": "MIN", "pos": "RB", "bye": 8, "tier": 7,
     "rush_yds": 550, "rush_tds": 4, "receptions": 22, "rec_yds": 160, "rec_tds": 1, "fumbles_lost": 1},
    {"name": "Kareem Hunt",        "team": "KC",  "pos": "RB", "bye": 6, "tier": 7,
     "rush_yds": 500, "rush_tds": 5, "receptions": 22, "rec_yds": 160, "rec_tds": 0, "fumbles_lost": 1},

    # =========================================================================
    # WIDE RECEIVERS (45)
    # =========================================================================
    {"name": "Ja'Marr Chase",         "team": "CIN", "pos": "WR", "bye": 12, "tier": 1,
     "receptions": 100, "rec_yds": 1450, "rec_tds": 11, "rush_yds": 50, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Puka Nacua",            "team": "LAR", "pos": "WR", "bye": 6, "tier": 1,
     "receptions": 105, "rec_yds": 1380, "rec_tds": 9, "rush_yds": 40, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Jaxon Smith-Njigba",    "team": "SEA", "pos": "WR", "bye": 11, "tier": 1,
     "receptions": 100, "rec_yds": 1350, "rec_tds": 10, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Amon-Ra St. Brown",     "team": "DET", "pos": "WR", "bye": 5, "tier": 1,
     "receptions": 105, "rec_yds": 1300, "rec_tds": 9, "rush_yds": 60, "rush_tds": 1, "fumbles_lost": 1},
    {"name": "A.J. Brown",            "team": "NE",  "pos": "WR", "bye": 14, "tier": 1,
     "receptions": 85, "rec_yds": 1300, "rec_tds": 10, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "CeeDee Lamb",           "team": "DAL", "pos": "WR", "bye": 7, "tier": 2,
     "receptions": 95, "rec_yds": 1250, "rec_tds": 9, "rush_yds": 50, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Justin Jefferson",      "team": "MIN", "pos": "WR", "bye": 8, "tier": 2,
     "receptions": 90, "rec_yds": 1350, "rec_tds": 9, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Drake London",          "team": "ATL", "pos": "WR", "bye": 12, "tier": 2,
     "receptions": 90, "rec_yds": 1200, "rec_tds": 9, "rush_yds": 40, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Nico Collins",          "team": "HOU", "pos": "WR", "bye": 13, "tier": 2,
     "receptions": 80, "rec_yds": 1250, "rec_tds": 9, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "George Pickens",        "team": "DAL", "pos": "WR", "bye": 7, "tier": 2,
     "receptions": 78, "rec_yds": 1200, "rec_tds": 9, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Rashee Rice",           "team": "KC",  "pos": "WR", "bye": 6, "tier": 2,
     "receptions": 90, "rec_yds": 1150, "rec_tds": 8, "rush_yds": 40, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Chris Olave",           "team": "NO",  "pos": "WR", "bye": 8, "tier": 3,
     "receptions": 82, "rec_yds": 1150, "rec_tds": 8, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Tee Higgins",           "team": "CIN", "pos": "WR", "bye": 12, "tier": 3,
     "receptions": 80, "rec_yds": 1100, "rec_tds": 8, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Garrett Wilson",        "team": "NYJ", "pos": "WR", "bye": 12, "tier": 3,
     "receptions": 85, "rec_yds": 1080, "rec_tds": 7, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Ladd McConkey",         "team": "LAC", "pos": "WR", "bye": 6, "tier": 3,
     "receptions": 82, "rec_yds": 1100, "rec_tds": 7, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "DeVonta Smith",         "team": "PHI", "pos": "WR", "bye": 5, "tier": 3,
     "receptions": 80, "rec_yds": 1050, "rec_tds": 7, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Zay Flowers",           "team": "BAL", "pos": "WR", "bye": 14, "tier": 3,
     "receptions": 78, "rec_yds": 1050, "rec_tds": 7, "rush_yds": 50, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Emeka Egbuka",          "team": "TB",  "pos": "WR", "bye": 11, "tier": 3,
     "receptions": 80, "rec_yds": 1050, "rec_tds": 7, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Davante Adams",         "team": "LAR", "pos": "WR", "bye": 6, "tier": 4,
     "receptions": 80, "rec_yds": 1000, "rec_tds": 8, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Jaylen Waddle",         "team": "DEN", "pos": "WR", "bye": 10, "tier": 4,
     "receptions": 78, "rec_yds": 1000, "rec_tds": 7, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Tetairoa McMillan",     "team": "CAR", "pos": "WR", "bye": 8, "tier": 4,
     "receptions": 75, "rec_yds": 1050, "rec_tds": 7, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Terry McLaurin",        "team": "WAS", "pos": "WR", "bye": 14, "tier": 4,
     "receptions": 72, "rec_yds": 1020, "rec_tds": 7, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Luther Burden III",     "team": "CHI", "pos": "WR", "bye": 7, "tier": 4,
     "receptions": 75, "rec_yds": 980, "rec_tds": 7, "rush_yds": 40, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Jameson Williams",      "team": "DET", "pos": "WR", "bye": 5, "tier": 4,
     "receptions": 65, "rec_yds": 1050, "rec_tds": 7, "rush_yds": 60, "rush_tds": 1, "fumbles_lost": 1},
    {"name": "DJ Moore",              "team": "BUF", "pos": "WR", "bye": 11, "tier": 4,
     "receptions": 75, "rec_yds": 950, "rec_tds": 6, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Mike Evans",            "team": "SF",  "pos": "WR", "bye": 9, "tier": 4,
     "receptions": 70, "rec_yds": 1000, "rec_tds": 8, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Malik Nabers",          "team": "NYG", "pos": "WR", "bye": 8, "tier": 4,
     "receptions": 78, "rec_yds": 980, "rec_tds": 6, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Christian Watson",      "team": "GB",  "pos": "WR", "bye": 10, "tier": 5,
     "receptions": 55, "rec_yds": 950, "rec_tds": 8, "rush_yds": 40, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Rome Odunze",           "team": "CHI", "pos": "WR", "bye": 7, "tier": 5,
     "receptions": 70, "rec_yds": 900, "rec_tds": 6, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Brian Thomas Jr.",      "team": "JAX", "pos": "WR", "bye": 9, "tier": 5,
     "receptions": 68, "rec_yds": 950, "rec_tds": 6, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Khalil Shakir",         "team": "BUF", "pos": "WR", "bye": 11, "tier": 5,
     "receptions": 70, "rec_yds": 850, "rec_tds": 5, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Keenan Allen",          "team": "CHI", "pos": "WR", "bye": 7, "tier": 5,
     "receptions": 78, "rec_yds": 850, "rec_tds": 5, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Courtland Sutton",      "team": "DEN", "pos": "WR", "bye": 10, "tier": 5,
     "receptions": 68, "rec_yds": 900, "rec_tds": 5, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Calvin Ridley",         "team": "TEN", "pos": "WR", "bye": 5, "tier": 5,
     "receptions": 65, "rec_yds": 880, "rec_tds": 5, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Xavier Worthy",         "team": "KC",  "pos": "WR", "bye": 6, "tier": 5,
     "receptions": 58, "rec_yds": 850, "rec_tds": 6, "rush_yds": 100, "rush_tds": 1, "fumbles_lost": 1},
    {"name": "Quentin Johnston",      "team": "LAC", "pos": "WR", "bye": 6, "tier": 6,
     "receptions": 60, "rec_yds": 820, "rec_tds": 5, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Diontae Johnson",       "team": "BAL", "pos": "WR", "bye": 14, "tier": 6,
     "receptions": 68, "rec_yds": 780, "rec_tds": 4, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Wan'Dale Robinson",     "team": "NYG", "pos": "WR", "bye": 8, "tier": 6,
     "receptions": 70, "rec_yds": 750, "rec_tds": 4, "rush_yds": 30, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Josh Downs",            "team": "IND", "pos": "WR", "bye": 14, "tier": 6,
     "receptions": 72, "rec_yds": 780, "rec_tds": 4, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Amari Cooper",          "team": "KC",  "pos": "WR", "bye": 6, "tier": 6,
     "receptions": 62, "rec_yds": 780, "rec_tds": 5, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Jayden Reed",           "team": "GB",  "pos": "WR", "bye": 10, "tier": 6,
     "receptions": 60, "rec_yds": 780, "rec_tds": 5, "rush_yds": 60, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Tyler Lockett",         "team": "SEA", "pos": "WR", "bye": 11, "tier": 6,
     "receptions": 60, "rec_yds": 750, "rec_tds": 5, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 0},
    {"name": "DK Metcalf",            "team": "SEA", "pos": "WR", "bye": 11, "tier": 6,
     "receptions": 58, "rec_yds": 850, "rec_tds": 5, "rush_yds": 20, "rush_tds": 0, "fumbles_lost": 1},
    {"name": "Stefon Diggs",          "team": "HOU", "pos": "WR", "bye": 13, "tier": 6,
     "receptions": 65, "rec_yds": 780, "rec_tds": 5, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 0},
    {"name": "Adam Thielen",          "team": "CAR", "pos": "WR", "bye": 8, "tier": 7,
     "receptions": 55, "rec_yds": 680, "rec_tds": 4, "rush_yds": 10, "rush_tds": 0, "fumbles_lost": 0},

    # =========================================================================
    # TIGHT ENDS (15)
    # =========================================================================
    {"name": "Brock Bowers",       "team": "LV",  "pos": "TE", "bye": 10, "tier": 1,
     "receptions": 95, "rec_yds": 1050, "rec_tds": 7, "fumbles_lost": 1},
    {"name": "Trey McBride",       "team": "ARI", "pos": "TE", "bye": 11, "tier": 1,
     "receptions": 90, "rec_yds": 950, "rec_tds": 6, "fumbles_lost": 1},
    {"name": "Colston Loveland",   "team": "SEA", "pos": "TE", "bye": 11, "tier": 2,
     "receptions": 70, "rec_yds": 780, "rec_tds": 6, "fumbles_lost": 1},
    {"name": "Tyler Warren",       "team": "PIT", "pos": "TE", "bye": 9, "tier": 2,
     "receptions": 68, "rec_yds": 750, "rec_tds": 5, "fumbles_lost": 1},
    {"name": "Tucker Kraft",       "team": "GB",  "pos": "TE", "bye": 10, "tier": 2,
     "receptions": 60, "rec_yds": 720, "rec_tds": 6, "fumbles_lost": 1},
    {"name": "Sam LaPorta",        "team": "DET", "pos": "TE", "bye": 5, "tier": 3,
     "receptions": 65, "rec_yds": 720, "rec_tds": 5, "fumbles_lost": 1},
    {"name": "Evan Engram",        "team": "JAX", "pos": "TE", "bye": 9, "tier": 3,
     "receptions": 70, "rec_yds": 680, "rec_tds": 4, "fumbles_lost": 1},
    {"name": "Mark Andrews",       "team": "BAL", "pos": "TE", "bye": 14, "tier": 3,
     "receptions": 55, "rec_yds": 650, "rec_tds": 6, "fumbles_lost": 1},
    {"name": "Travis Kelce",       "team": "KC",  "pos": "TE", "bye": 6, "tier": 3,
     "receptions": 68, "rec_yds": 680, "rec_tds": 4, "fumbles_lost": 1},
    {"name": "George Kittle",      "team": "SF",  "pos": "TE", "bye": 9, "tier": 4,
     "receptions": 55, "rec_yds": 650, "rec_tds": 5, "fumbles_lost": 1},
    {"name": "David Njoku",        "team": "CLE", "pos": "TE", "bye": 10, "tier": 4,
     "receptions": 58, "rec_yds": 620, "rec_tds": 4, "fumbles_lost": 1},
    {"name": "Dallas Goedert",     "team": "PHI", "pos": "TE", "bye": 5, "tier": 4,
     "receptions": 55, "rec_yds": 600, "rec_tds": 4, "fumbles_lost": 1},
    {"name": "Pat Freiermuth",     "team": "PIT", "pos": "TE", "bye": 9, "tier": 5,
     "receptions": 50, "rec_yds": 550, "rec_tds": 4, "fumbles_lost": 1},
    {"name": "Jake Ferguson",      "team": "DAL", "pos": "TE", "bye": 7, "tier": 5,
     "receptions": 52, "rec_yds": 560, "rec_tds": 4, "fumbles_lost": 1},
    {"name": "Dalton Kincaid",     "team": "BUF", "pos": "TE", "bye": 11, "tier": 5,
     "receptions": 55, "rec_yds": 580, "rec_tds": 3, "fumbles_lost": 1},

    # =========================================================================
    # KICKERS (10)
    # =========================================================================
    {"name": "Brandon Aubrey",  "team": "DAL", "pos": "K", "bye": 7, "tier": 1,
     "fg_0_39": 18, "fg_40_49": 10, "fg_50_plus": 8, "pat": 38, "fg_miss": 3},
    {"name": "Will Reichard",   "team": "MIN", "pos": "K", "bye": 8, "tier": 1,
     "fg_0_39": 16, "fg_40_49": 9, "fg_50_plus": 5, "pat": 40, "fg_miss": 3},
    {"name": "Chase McLaughlin","team": "TB",  "pos": "K", "bye": 11, "tier": 2,
     "fg_0_39": 15, "fg_40_49": 8, "fg_50_plus": 5, "pat": 38, "fg_miss": 3},
    {"name": "Jake Bates",      "team": "DET", "pos": "K", "bye": 5, "tier": 2,
     "fg_0_39": 14, "fg_40_49": 9, "fg_50_plus": 5, "pat": 40, "fg_miss": 3},
    {"name": "Ka'imi Fairbairn","team": "HOU", "pos": "K", "bye": 13, "tier": 2,
     "fg_0_39": 15, "fg_40_49": 8, "fg_50_plus": 4, "pat": 38, "fg_miss": 2},
    {"name": "Tyler Bass",      "team": "BUF", "pos": "K", "bye": 11, "tier": 3,
     "fg_0_39": 14, "fg_40_49": 8, "fg_50_plus": 4, "pat": 38, "fg_miss": 3},
    {"name": "Younghoe Koo",    "team": "ATL", "pos": "K", "bye": 12, "tier": 3,
     "fg_0_39": 14, "fg_40_49": 8, "fg_50_plus": 4, "pat": 36, "fg_miss": 3},
    {"name": "Cameron Dicker",  "team": "LAC", "pos": "K", "bye": 6, "tier": 3,
     "fg_0_39": 14, "fg_40_49": 7, "fg_50_plus": 4, "pat": 36, "fg_miss": 2},
    {"name": "Evan McPherson",  "team": "CIN", "pos": "K", "bye": 12, "tier": 3,
     "fg_0_39": 13, "fg_40_49": 8, "fg_50_plus": 4, "pat": 36, "fg_miss": 3},
    {"name": "Jason Sanders",   "team": "MIA", "pos": "K", "bye": 6, "tier": 3,
     "fg_0_39": 13, "fg_40_49": 7, "fg_50_plus": 4, "pat": 35, "fg_miss": 3},

    # =========================================================================
    # DEFENSES (12)
    # =========================================================================
    # pa_pts = projected total season points from "points allowed" buckets
    {"name": "Rams",          "team": "LAR", "pos": "DEF", "bye": 6, "tier": 1,
     "sacks": 48, "ints": 16, "fr": 10, "tds": 4, "safeties": 1, "pa_pts": 40},
    {"name": "Seahawks",      "team": "SEA", "pos": "DEF", "bye": 11, "tier": 1,
     "sacks": 45, "ints": 15, "fr": 10, "tds": 3, "safeties": 1, "pa_pts": 38},
    {"name": "Eagles",        "team": "PHI", "pos": "DEF", "bye": 5, "tier": 1,
     "sacks": 46, "ints": 14, "fr": 10, "tds": 3, "safeties": 1, "pa_pts": 36},
    {"name": "Broncos",       "team": "DEN", "pos": "DEF", "bye": 10, "tier": 2,
     "sacks": 44, "ints": 15, "fr": 9, "tds": 3, "safeties": 0, "pa_pts": 34},
    {"name": "Steelers",      "team": "PIT", "pos": "DEF", "bye": 9, "tier": 2,
     "sacks": 46, "ints": 13, "fr": 9, "tds": 3, "safeties": 1, "pa_pts": 32},
    {"name": "Ravens",        "team": "BAL", "pos": "DEF", "bye": 14, "tier": 2,
     "sacks": 44, "ints": 14, "fr": 8, "tds": 3, "safeties": 0, "pa_pts": 34},
    {"name": "Bears",         "team": "CHI", "pos": "DEF", "bye": 7, "tier": 2,
     "sacks": 42, "ints": 14, "fr": 9, "tds": 3, "safeties": 0, "pa_pts": 32},
    {"name": "Chiefs",        "team": "KC",  "pos": "DEF", "bye": 6, "tier": 3,
     "sacks": 40, "ints": 14, "fr": 8, "tds": 2, "safeties": 0, "pa_pts": 34},
    {"name": "49ers",         "team": "SF",  "pos": "DEF", "bye": 9, "tier": 3,
     "sacks": 40, "ints": 13, "fr": 8, "tds": 2, "safeties": 1, "pa_pts": 30},
    {"name": "Vikings",       "team": "MIN", "pos": "DEF", "bye": 8, "tier": 3,
     "sacks": 42, "ints": 13, "fr": 8, "tds": 2, "safeties": 0, "pa_pts": 30},
    {"name": "Bills",         "team": "BUF", "pos": "DEF", "bye": 11, "tier": 3,
     "sacks": 40, "ints": 13, "fr": 7, "tds": 2, "safeties": 0, "pa_pts": 30},
    {"name": "Texans",        "team": "HOU", "pos": "DEF", "bye": 13, "tier": 3,
     "sacks": 38, "ints": 14, "fr": 8, "tds": 2, "safeties": 0, "pa_pts": 28},
]


def _build_players():
    """Process raw player data: calculate fantasy points, assign positional ranks."""
    players = []
    for p in _RAW_PLAYERS:
        entry = dict(p)
        entry["fpts"] = calculate_fantasy_points(entry)
        players.append(entry)

    # Assign positional ranks
    pos_counters = {}
    for pos in ["QB", "RB", "WR", "TE", "K", "DEF"]:
        pos_players = sorted(
            [p for p in players if p["pos"] == pos],
            key=lambda x: x["fpts"],
            reverse=True
        )
        for i, p in enumerate(pos_players, 1):
            p["pos_rank"] = i
            p["pos_label"] = f"{pos}{i}"

    # Assign overall rank by fantasy points
    players.sort(key=lambda x: x["fpts"], reverse=True)
    for i, p in enumerate(players, 1):
        p["overall_rank"] = i

    return players


# Build the master player list on import
ALL_PLAYERS = _build_players()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_all_players():
    """Return all players sorted by overall rank (descending fantasy points)."""
    return list(ALL_PLAYERS)


def get_players_by_position(pos: str):
    """Return players for a given position, sorted by positional rank."""
    return sorted(
        [p for p in ALL_PLAYERS if p["pos"] == pos.upper()],
        key=lambda x: x["pos_rank"]
    )


def get_top_n(n: int = 150):
    """Return the top N players by projected fantasy points."""
    return ALL_PLAYERS[:n]


def get_player_by_name(name: str):
    """Find a player by name (case-insensitive partial match)."""
    name_lower = name.lower()
    for p in ALL_PLAYERS:
        if name_lower in p["name"].lower():
            return p
    return None


def get_replacement_level():
    """
    Calculate the 'replacement level' player for each position.
    This is the Nth-ranked player at each position where N = roster requirement + a small buffer.
    Used for VORP (Value Over Replacement Player) calculations.
    """
    # In a 10-team league, replacement level is roughly:
    # QB: 20th (2 per team), RB: 30th (3-4 per team), WR: 35th (4-5 per team), TE: 15th
    replacement_ranks = {
        "QB": 15,  # ~12-14 teams * 1-2 starters, replacement around QB15
        "RB": 25,  # Heavy demand, replacement around RB25
        "WR": 30,  # Deep position, replacement around WR30
        "TE": 12,  # Shallow, replacement around TE12
        "K": 10,
        "DEF": 10,
    }
    replacement = {}
    for pos, rank in replacement_ranks.items():
        pos_players = get_players_by_position(pos)
        if rank <= len(pos_players):
            replacement[pos] = pos_players[rank - 1]["fpts"]
        else:
            replacement[pos] = 0
    return replacement


def calculate_vorp(player: dict, replacement_levels: dict = None):
    """Calculate Value Over Replacement Player for a given player."""
    if replacement_levels is None:
        replacement_levels = get_replacement_level()
    pos = player["pos"]
    return round(player["fpts"] - replacement_levels.get(pos, 0), 1)


# ---------------------------------------------------------------------------
# Quick test / preview
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 72)
    print("  FANTASY FOOTBALL 2026 - PLAYER DATABASE")
    print("  ESPN League 756823 | Half PPR | 4pt Pass TD")
    print("=" * 72)
    print(f"\n  Total players in database: {len(ALL_PLAYERS)}")
    print()

    for pos in ["QB", "RB", "WR", "TE", "K", "DEF"]:
        players = get_players_by_position(pos)
        top3 = players[:3]
        print(f"  {pos} Top 3:")
        for p in top3:
            print(f"    {p['pos_label']:>6}  {p['name']:<24} {p['team']:<4}  {p['fpts']:>6.1f} pts")
        print()

    print("  REPLACEMENT LEVELS:")
    for pos, pts in get_replacement_level().items():
        print(f"    {pos:<4} = {pts:>6.1f} pts")
    print()

    print("  TOP 10 OVERALL:")
    for p in get_top_n(10):
        vorp = calculate_vorp(p)
        print(f"    #{p['overall_rank']:<3} {p['pos_label']:>6}  {p['name']:<24} {p['team']:<4}  "
              f"{p['fpts']:>6.1f} pts  (VORP: {vorp:>+6.1f})")
    print()
