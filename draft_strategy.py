"""
Fantasy Football 2026-2027 - Draft Strategy & Roster Optimizer
================================================================
ESPN League 756823 | Half PPR | 4pt Passing TDs
Roster: 2 QB, 4 RB, 5 WR, 2 TE, 1 DEF, 1 K (15 total)

Features:
  1. Round-by-round strategy recommendations
  2. Best Player Available (BPA) vs Positional Need
  3. VORP calculations for draft decisions
  4. Interactive draft tracker - mark picks and get updated suggestions
  5. Sleeper picks & value targets

Usage:
  python draft_strategy.py              # Show round-by-round strategy guide
  python draft_strategy.py --draft      # Start interactive draft tracker
  python draft_strategy.py --sleepers   # Show sleeper picks & value targets
  python draft_strategy.py --vorp       # Show VORP analysis
"""

import sys
from player_data import (
    get_all_players, get_players_by_position, get_top_n,
    get_replacement_level, calculate_vorp, ROSTER_REQUIREMENTS, TOTAL_ROSTER
)

# ---------------------------------------------------------------------------
# ANSI Colors
# ---------------------------------------------------------------------------
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    MAGENTA= "\033[95m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"

POS_COLORS = {"QB": C.RED, "RB": C.GREEN, "WR": C.BLUE, "TE": C.MAGENTA, "K": C.YELLOW, "DEF": C.CYAN}


def separator(char="-", width=80):
    print(f"{C.DIM}{char * width}{C.RESET}")


def thick_separator(width=80):
    print(f"{C.BOLD}{'=' * width}{C.RESET}")


# ---------------------------------------------------------------------------
# Round-by-Round Strategy Guide
# ---------------------------------------------------------------------------
ROUND_STRATEGY = {
    1: {
        "targets": ["RB1/RB2", "WR1/WR2"],
        "advice": "Take the best RB or WR available. Gibbs, Bijan, Chase, and Nacua "
                  "are the elite tier. Don't reach for QB here.",
        "positions": ["RB", "WR"],
    },
    2: {
        "targets": ["RB (if took WR in R1)", "WR (if took RB in R1)"],
        "advice": "Balance your roster. If you went RB first, grab a WR1/WR2. "
                  "Players like J. Taylor, Achane, JSN, Amon-Ra available here.",
        "positions": ["RB", "WR"],
    },
    3: {
        "targets": ["WR2", "RB2", "Elite TE"],
        "advice": "This is where Brock Bowers and elite TEs may fall. If Bowers is here, "
                  "strongly consider him - the TE cliff is steep. Otherwise, keep stacking RB/WR.",
        "positions": ["RB", "WR", "TE"],
    },
    4: {
        "targets": ["QB1", "WR3", "RB3"],
        "advice": "If Allen, Lamar, or Hurts are here, it's time for your QB1. "
                  "You need 2 QBs, so getting one elite arm early pays off. "
                  "Otherwise, grab RB/WR depth.",
        "positions": ["QB", "RB", "WR"],
    },
    5: {
        "targets": ["QB1 (if not yet)", "RB3", "WR3"],
        "advice": "Last chance for a top-tier QB. Burrow, Maye, Caleb Williams territory. "
                  "Don't leave this round without at least 1 QB if you can help it.",
        "positions": ["QB", "RB", "WR"],
    },
    6: {
        "targets": ["WR4", "RB3/RB4", "TE1"],
        "advice": "Fill your flex spots. Target high-upside WR3/WR4 types. "
                  "If you skipped TE, McBride/Loveland/Warren could still be here.",
        "positions": ["RB", "WR", "TE"],
    },
    7: {
        "targets": ["QB2", "WR4", "TE1/TE2"],
        "advice": "Time for your second QB if you only have one. Herbert, Dak, Lawrence "
                  "are solid QB2 options. Also target a TE if you haven't gotten one.",
        "positions": ["QB", "WR", "TE"],
    },
    8: {
        "targets": ["WR5", "RB4", "QB2 (if not yet)"],
        "advice": "Round out your WR corps and RB depth. If you still need a QB2, "
                  "don't wait past this round. Purdy and Goff are undervalued here.",
        "positions": ["QB", "RB", "WR"],
    },
    9: {
        "targets": ["RB4", "WR5", "TE2"],
        "advice": "Fill remaining roster holes. Target upside RBs - Jaylen Warren, "
                  "Cam Skattebo types who could emerge as starters if injuries hit.",
        "positions": ["RB", "WR", "TE"],
    },
    10: {
        "targets": ["TE2", "RB depth", "WR depth"],
        "advice": "Secure your TE2 if you only have one. Look for high-floor TEs "
                  "like Kelce, Kittle, or Engram at a discount.",
        "positions": ["RB", "WR", "TE"],
    },
    11: {
        "targets": ["RB handcuff", "WR upside", "TE2"],
        "advice": "Fill your bench. Handcuff your elite RB if the backup is available. "
                  "Target WRs with week-winning upside (Watson, Xavier Worthy).",
        "positions": ["RB", "WR", "TE"],
    },
    12: {
        "targets": ["DEF", "K"],
        "advice": "Draft your defense. Rams, Seahawks, Eagles are the top tier. "
                  "Some leagues let you wait on DST to round 13-14 - your call.",
        "positions": ["DEF", "K"],
    },
    13: {
        "targets": ["K", "DEF (if not yet)"],
        "advice": "Draft your kicker. Brandon Aubrey is the only K worth reaching for. "
                  "Otherwise, any K in the top 5 is fine.",
        "positions": ["K", "DEF"],
    },
    14: {
        "targets": ["Best available"],
        "advice": "Fill any remaining roster spot with the best available player. "
                  "Prioritize upside over floor at this point.",
        "positions": ["QB", "RB", "WR", "TE"],
    },
    15: {
        "targets": ["Best available"],
        "advice": "Final pick. Take a dart-throw with upside - a backup RB on a "
                  "run-heavy team, or a deep WR sleeper.",
        "positions": ["RB", "WR"],
    },
}

# Draft priority targets by round
MUST_DRAFT_BY = {
    "QB": {"first_by": 5, "second_by": 8},
    "RB": {"first_by": 2, "all_by": 11},
    "WR": {"first_by": 3, "all_by": 11},
    "TE": {"first_by": 6, "second_by": 10},
    "DEF": {"first_by": 13},
    "K": {"first_by": 14},
}


def show_strategy_guide():
    """Display the round-by-round draft strategy guide."""
    thick_separator()
    print(f"{C.BOLD}  2026 DRAFT STRATEGY - ROUND-BY-ROUND GUIDE{C.RESET}")
    print(f"{C.DIM}  Roster: 2 QB, 4 RB, 5 WR, 2 TE, 1 DEF, 1 K (15 total){C.RESET}")
    thick_separator()

    for rnd in range(1, 16):
        info = ROUND_STRATEGY.get(rnd, {})
        targets = info.get("targets", ["Best available"])
        advice = info.get("advice", "")

        print(f"\n  {C.BOLD}{C.YELLOW}ROUND {rnd}{C.RESET}")
        print(f"  {C.DIM}Targets:{C.RESET} {', '.join(targets)}")
        print(f"  {advice}")

    # Must-draft-by deadlines
    print(f"\n\n  {C.BOLD}{C.RED}[!] MUST-DRAFT-BY DEADLINES{C.RESET}")
    separator()
    for pos, deadlines in MUST_DRAFT_BY.items():
        color = POS_COLORS.get(pos, C.WHITE)
        parts = []
        if "first_by" in deadlines:
            parts.append(f"1st by Round {deadlines['first_by']}")
        if "second_by" in deadlines:
            parts.append(f"2nd by Round {deadlines['second_by']}")
        if "all_by" in deadlines:
            parts.append(f"All {ROSTER_REQUIREMENTS[pos]} by Round {deadlines['all_by']}")
        print(f"  {color}{pos:<4}{C.RESET}  {' | '.join(parts)}")

    separator()
    print()


# ---------------------------------------------------------------------------
# VORP Analysis
# ---------------------------------------------------------------------------
def show_vorp_analysis():
    """Display VORP rankings to show where positional edges are biggest."""
    players = get_top_n(150)
    repl = get_replacement_level()

    thick_separator()
    print(f"{C.BOLD}  VORP ANALYSIS - VALUE OVER REPLACEMENT PLAYER{C.RESET}")
    thick_separator()

    print(f"\n  {C.DIM}Replacement Levels:{C.RESET}")
    for pos, pts in repl.items():
        color = POS_COLORS.get(pos, C.WHITE)
        print(f"    {color}{pos:<4}{C.RESET} = {pts:>6.1f} season pts")
    print()

    # Sort by VORP
    vorp_list = []
    for p in players:
        vorp = calculate_vorp(p, repl)
        vorp_list.append((p, vorp))
    vorp_list.sort(key=lambda x: x[1], reverse=True)

    print(f"  {C.BOLD}TOP 30 BY VORP (biggest edges over replacement):{C.RESET}")
    separator()
    print(f"{C.DIM}  {'Rank':<5} {'Pos':>5}  {'Player':<26} {'FPts':>7}  {'VORP':>7}  {'Edge'}{C.RESET}")
    separator()

    for i, (p, vorp) in enumerate(vorp_list[:30], 1):
        color = POS_COLORS.get(p["pos"], C.WHITE)
        bar = "#" * max(1, int(vorp / 10))
        print(f"  {i:<5} {color}{p['pos_label']:>5}{C.RESET}  "
              f"{p['name']:<26} "
              f"{p['fpts']:>7.1f}  "
              f"{C.GREEN}{vorp:>+7.1f}{C.RESET}  "
              f"{C.GREEN}{bar}{C.RESET}")

    separator()
    print()


# ---------------------------------------------------------------------------
# Sleeper Picks & Value Targets
# ---------------------------------------------------------------------------
def show_sleepers():
    """Show sleeper picks - players who could outperform their draft position."""
    thick_separator()
    print(f"{C.BOLD}  SLEEPER PICKS & VALUE TARGETS - 2026{C.RESET}")
    thick_separator()

    sleepers = [
        {
            "name": "Drake Maye", "pos": "QB", "team": "NE",
            "reason": "Second-year leap candidate. Strong arm, improved weapons with A.J. Brown. "
                      "Could finish as QB3-5 but drafted as QB5-7.",
        },
        {
            "name": "Ashton Jeanty", "pos": "RB", "team": "LV",
            "reason": "Rookie phenom from Boise State. College production was historic. "
                      "Las Vegas will lean heavily on him. Could be a top-5 RB.",
        },
        {
            "name": "Cam Skattebo", "pos": "RB", "team": "NYG",
            "reason": "Rookie with workhorse potential. NYG's OL improved and he'll get "
                      "3-down work. Elite pass-catching RB - valuable in Half PPR.",
        },
        {
            "name": "Jaxon Smith-Njigba", "pos": "WR", "team": "SEA",
            "reason": "Breakout WR1 in Seattle. Elite route runner with target hog potential. "
                      "Could finish as overall WR1 but drafted WR3-5.",
        },
        {
            "name": "Emeka Egbuka", "pos": "WR", "team": "TB",
            "reason": "Second-year WR in a pass-heavy Tampa offense. Low ADP relative to "
                      "his expected target share. WR2 ceiling at a WR3 price.",
        },
        {
            "name": "Luther Burden III", "pos": "WR", "team": "CHI",
            "reason": "Rookie with Caleb Williams throwing to him. Electric playmaker "
                      "who can line up everywhere. Late-round upside play.",
        },
        {
            "name": "Colston Loveland", "pos": "TE", "team": "SEA",
            "reason": "Rookie TE stepping into a big role. Athletic freak who can line up "
                      "as a WR. Could be a top-5 TE at a late-round price.",
        },
        {
            "name": "Brock Purdy", "pos": "QB", "team": "SF",
            "reason": "Elite offense, low INT rate. Always finishes better than his ADP. "
                      "Perfect QB2 who could give you QB1 weeks.",
        },
        {
            "name": "Xavier Worthy", "pos": "WR", "team": "KC",
            "reason": "Speed demon in the Chiefs offense. Boom-or-bust but the booms are "
                      "week-winners. Great late-round WR5 target.",
        },
        {
            "name": "TreVeyon Henderson", "pos": "RB", "team": "NE",
            "reason": "Explosive RB in an improving NE offense. Could emerge as lead back "
                      "if he stays healthy. Low cost, high ceiling.",
        },
    ]

    for s in sleepers:
        color = POS_COLORS.get(s["pos"], C.WHITE)
        print(f"\n  {color}{C.BOLD}{s['name']}{C.RESET} - {color}{s['pos']}{C.RESET}, {s['team']}")
        print(f"  {C.DIM}{s['reason']}{C.RESET}")

    separator()
    print()


# ---------------------------------------------------------------------------
# Interactive Draft Tracker
# ---------------------------------------------------------------------------
def run_draft_tracker():
    """Interactive draft tracker - mark picks and get live recommendations."""
    all_players = get_all_players()
    available = list(all_players)  # Copy
    my_roster = {"QB": [], "RB": [], "WR": [], "TE": [], "K": [], "DEF": []}
    picks_made = 0
    repl = get_replacement_level()

    thick_separator()
    print(f"{C.BOLD}  [FB] INTERACTIVE DRAFT TRACKER - 2026{C.RESET}")
    print(f"{C.DIM}  Roster: 2 QB, 4 RB, 5 WR, 2 TE, 1 DEF, 1 K{C.RESET}")
    thick_separator()
    print(f"\n  Commands:")
    print(f"    {C.BOLD}pick <name>{C.RESET}   - Draft a player to your roster")
    print(f"    {C.BOLD}taken <name>{C.RESET}  - Mark a player as taken by another team")
    print(f"    {C.BOLD}best{C.RESET}          - Show best available by position")
    print(f"    {C.BOLD}suggest{C.RESET}       - Get AI recommendation for your next pick")
    print(f"    {C.BOLD}roster{C.RESET}        - View your current roster")
    print(f"    {C.BOLD}needs{C.RESET}         - Show remaining roster needs")
    print(f"    {C.BOLD}quit{C.RESET}          - Exit tracker")
    separator()

    while True:
        try:
            cmd = input(f"\n  {C.CYAN}Round {picks_made + 1}>{C.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        action = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if action == "quit" or action == "exit":
            print(f"\n  {C.YELLOW}Draft tracker closed.{C.RESET}")
            break

        elif action == "pick":
            _handle_pick(arg, available, my_roster, repl)
            picks_made += 1
            _show_needs(my_roster)

        elif action == "taken":
            _handle_taken(arg, available)

        elif action == "best":
            _show_best_available(available, repl)

        elif action == "suggest":
            _suggest_pick(available, my_roster, picks_made, repl)

        elif action == "roster":
            _show_roster(my_roster)

        elif action == "needs":
            _show_needs(my_roster)

        else:
            print(f"  {C.RED}Unknown command. Try: pick, taken, best, suggest, roster, needs, quit{C.RESET}")


def _find_player(name: str, players: list):
    """Find a player by partial name match."""
    name_lower = name.lower()
    matches = [p for p in players if name_lower in p["name"].lower()]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"  {C.YELLOW}Multiple matches:{C.RESET}")
        for m in matches[:5]:
            print(f"    {m['name']} ({m['pos']}, {m['team']})")
        return None
    else:
        print(f"  {C.RED}Player not found: '{name}'{C.RESET}")
        return None


def _handle_pick(name: str, available: list, roster: dict, repl: dict):
    """Draft a player to your roster."""
    player = _find_player(name, available)
    if not player:
        return

    pos = player["pos"]
    needed = ROSTER_REQUIREMENTS[pos]
    have = len(roster[pos])

    if have >= needed:
        print(f"  {C.YELLOW}[!] You already have {have}/{needed} {pos}s. Pick anyway? (y/n){C.RESET}", end=" ")
        try:
            if input().strip().lower() != "y":
                return
        except (EOFError, KeyboardInterrupt):
            return

    roster[pos].append(player)
    available.remove(player)
    color = POS_COLORS.get(pos, C.WHITE)
    vorp = calculate_vorp(player, repl)
    print(f"  {C.GREEN}[OK] Drafted:{C.RESET} {color}{player['pos_label']}{C.RESET} "
          f"{C.BOLD}{player['name']}{C.RESET} ({player['team']}) - "
          f"{player['fpts']:.1f} pts, VORP: {vorp:+.1f}")


def _handle_taken(name: str, available: list):
    """Mark a player as taken by another team."""
    player = _find_player(name, available)
    if player:
        available.remove(player)
        print(f"  {C.DIM}[X] Removed: {player['name']} ({player['pos']}, {player['team']}){C.RESET}")


def _show_best_available(available: list, repl: dict):
    """Show best available players by position."""
    for pos in ["QB", "RB", "WR", "TE", "K", "DEF"]:
        color = POS_COLORS.get(pos, C.WHITE)
        pos_avail = [p for p in available if p["pos"] == pos]
        pos_avail.sort(key=lambda x: x["fpts"], reverse=True)
        top3 = pos_avail[:3]

        print(f"  {color}{C.BOLD}{pos}:{C.RESET}", end="  ")
        for p in top3:
            vorp = calculate_vorp(p, repl)
            print(f"{p['name']} ({p['fpts']:.0f}pts, VORP:{vorp:+.0f})", end="  ")
        print()


def _suggest_pick(available: list, roster: dict, picks_made: int, repl: dict):
    """Suggest the best pick based on roster needs and VORP."""
    needs = {}
    for pos, required in ROSTER_REQUIREMENTS.items():
        have = len(roster[pos])
        remaining = required - have
        if remaining > 0:
            needs[pos] = remaining

    # Calculate VORP for all available players
    suggestions = []
    for p in available:
        pos = p["pos"]
        if pos not in needs:
            continue  # Already filled

        vorp = calculate_vorp(p, repl)

        # Urgency multiplier: boost positions you need more urgently
        urgency = 1.0
        if pos in MUST_DRAFT_BY:
            deadline = MUST_DRAFT_BY[pos].get("first_by", 15)
            have = len(roster[pos])
            if have == 0 and picks_made + 1 >= deadline:
                urgency = 1.5  # Urgent!
            elif have == 0 and picks_made + 2 >= deadline:
                urgency = 1.2  # Getting urgent

        adjusted_vorp = vorp * urgency
        suggestions.append((p, vorp, adjusted_vorp, urgency))

    suggestions.sort(key=lambda x: x[2], reverse=True)

    print(f"\n  {C.BOLD}{C.YELLOW}[T] SUGGESTED PICKS:{C.RESET}")
    separator()

    for i, (p, vorp, adj_vorp, urgency) in enumerate(suggestions[:5], 1):
        color = POS_COLORS.get(p["pos"], C.WHITE)
        urgent_tag = f" {C.RED}!! URGENT{C.RESET}" if urgency > 1.0 else ""
        print(f"  {i}. {color}{p['pos_label']}{C.RESET} "
              f"{C.BOLD}{p['name']}{C.RESET} ({p['team']}) - "
              f"{p['fpts']:.1f} pts, VORP: {vorp:+.1f}{urgent_tag}")

    print()


def _show_roster(roster: dict):
    """Show current roster."""
    print(f"\n  {C.BOLD}YOUR ROSTER:{C.RESET}")
    separator()
    total_pts = 0
    for pos in ["QB", "RB", "WR", "TE", "K", "DEF"]:
        color = POS_COLORS.get(pos, C.WHITE)
        needed = ROSTER_REQUIREMENTS[pos]
        have = len(roster[pos])
        status = f"{C.GREEN}[OK]{C.RESET}" if have >= needed else f"{C.RED}[X]{C.RESET}"

        print(f"  {status} {color}{pos}{C.RESET} ({have}/{needed}):")
        for p in roster[pos]:
            total_pts += p["fpts"]
            print(f"      {p['pos_label']:>6} {p['name']:<24} {p['team']:<4} {p['fpts']:>6.1f} pts")
        if have == 0:
            print(f"      {C.DIM}(empty){C.RESET}")

    separator()
    print(f"  {C.BOLD}Total projected: {total_pts:.1f} pts{C.RESET}")
    print()


def _show_needs(roster: dict):
    """Show remaining roster needs."""
    total_picks = sum(len(v) for v in roster.values())
    remaining = TOTAL_ROSTER - total_picks

    print(f"\n  {C.BOLD}ROSTER NEEDS{C.RESET} ({remaining} picks remaining):")
    for pos in ["QB", "RB", "WR", "TE", "K", "DEF"]:
        needed = ROSTER_REQUIREMENTS[pos]
        have = len(roster[pos])
        left = max(0, needed - have)
        if left > 0:
            color = POS_COLORS.get(pos, C.WHITE)
            print(f"    {color}{pos}{C.RESET}: need {left} more ({have}/{needed})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]

    if "--draft" in args:
        run_draft_tracker()
    elif "--sleepers" in args:
        show_sleepers()
    elif "--vorp" in args:
        show_vorp_analysis()
    elif "--help" in args:
        print(__doc__)
    else:
        show_strategy_guide()


if __name__ == "__main__":
    main()
