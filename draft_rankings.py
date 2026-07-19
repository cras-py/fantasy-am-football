"""
Fantasy Football 2026-2027 - Draft Rankings & Cheat Sheet Generator
====================================================================
ESPN League 756823 | Half PPR | 4pt Passing TDs

Generates:
  1. Overall Top 150 rankings with tiers and VORP
  2. Positional rankings (QB, RB, WR, TE, K, DEF)
  3. Printable cheat sheet for draft day
  4. CSV export for spreadsheet use

Usage:
  python draft_rankings.py              # Full cheat sheet to terminal
  python draft_rankings.py --csv        # Export to CSV file
  python draft_rankings.py --position QB  # Show specific position
  python draft_rankings.py --tiers      # Show tier breakdowns
  python draft_rankings.py --compact    # Compact memorization view
"""

import sys
import csv
import os
from player_data import (
    get_all_players, get_players_by_position, get_top_n,
    get_replacement_level, calculate_vorp, ROSTER_REQUIREMENTS
)

# ---------------------------------------------------------------------------
# ANSI color codes for terminal output
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
    BG_DARK= "\033[48;5;235m"

POS_COLORS = {
    "QB": C.RED,
    "RB": C.GREEN,
    "WR": C.BLUE,
    "TE": C.MAGENTA,
    "K":  C.YELLOW,
    "DEF": C.CYAN,
}

TIER_LABELS = {
    1: "Elite / Locked In",
    2: "Strong Starter",
    3: "Solid Starter",
    4: "Flex / Upside",
    5: "Bench / Depth",
    6: "Late Round Value",
    7: "Dart Throw / Handcuff",
}


def pos_color(pos: str) -> str:
    return POS_COLORS.get(pos, C.WHITE)


def format_rank(rank: int) -> str:
    """Format rank with padding."""
    return f"#{rank:<3}"


def separator(char="-", width=80):
    print(f"{C.DIM}{char * width}{C.RESET}")


def thick_separator(width=80):
    print(f"{C.BOLD}{'=' * width}{C.RESET}")


# ---------------------------------------------------------------------------
# Display: Overall Top 150
# ---------------------------------------------------------------------------
def show_top_150():
    """Display the Top 150 overall rankings with tier breaks."""
    players = get_top_n(150)
    repl = get_replacement_level()

    thick_separator()
    print(f"{C.BOLD}{'':>4}  TOP 150 OVERALL RANKINGS - 2026 HALF PPR CHEAT SHEET{'':>4}{C.RESET}")
    thick_separator()
    print(f"{C.DIM}{'Rank':<6} {'Tier':>4}  {'Pos':>5}  {'Player':<26} {'Team':<5} {'Bye':>3}  "
          f"{'FPts':>7}  {'VORP':>7}{C.RESET}")
    separator()

    current_tier = None
    for p in players:
        # Determine the effective tier grouping for overall display
        # Use VORP tiers for positioning
        tier = p.get("tier", 7)
        vorp = calculate_vorp(p, repl)

        # Tier break visual separator
        overall_tier = _get_overall_tier(p["overall_rank"])
        if overall_tier != current_tier:
            if current_tier is not None:
                _print_tier_break(overall_tier)
            current_tier = overall_tier

        color = pos_color(p["pos"])
        vorp_color = C.GREEN if vorp > 0 else C.RED if vorp < 0 else C.DIM

        print(f"  {format_rank(p['overall_rank'])} "
              f" T{tier}   "
              f"{color}{p['pos_label']:>6}{C.RESET}  "
              f"{p['name']:<26} "
              f"{p['team']:<5}"
              f"{p['bye']:>3}  "
              f"{C.BOLD}{p['fpts']:>7.1f}{C.RESET}  "
              f"{vorp_color}{vorp:>+7.1f}{C.RESET}")

    separator()
    print(f"\n{C.DIM}  FPts = Projected Season Fantasy Points (Half PPR)")
    print(f"  VORP = Value Over Replacement Player{C.RESET}\n")


def _get_overall_tier(rank: int) -> int:
    """Group overall ranks into memorization-friendly tiers."""
    if rank <= 12:
        return 1   # Round 1 territory
    elif rank <= 24:
        return 2   # Round 2
    elif rank <= 36:
        return 3   # Round 3
    elif rank <= 60:
        return 4   # Rounds 4-5
    elif rank <= 90:
        return 5   # Rounds 6-8
    elif rank <= 120:
        return 6   # Rounds 9-10
    else:
        return 7   # Rounds 11+


def _print_tier_break(tier: int):
    """Print a visual tier break with label."""
    labels = {
        1: "TIER 1 - CAN'T-MISS (Picks 1-12)",
        2: "TIER 2 - STRONG STARTERS (Picks 13-24)",
        3: "TIER 3 - CORE BUILDERS (Picks 25-36)",
        4: "TIER 4 - VALUE ZONE (Picks 37-60)",
        5: "TIER 5 - DEPTH & SLEEPERS (Picks 61-90)",
        6: "TIER 6 - LATE ROUND UPSIDE (Picks 91-120)",
        7: "TIER 7 - FINAL PICKS (Picks 121-150)",
    }
    label = labels.get(tier, f"TIER {tier}")
    print(f"\n  {C.BOLD}{C.YELLOW}> {label}{C.RESET}")
    separator("-", 80)


# ---------------------------------------------------------------------------
# Display: Positional Rankings
# ---------------------------------------------------------------------------
def show_positional_rankings(position: str = None):
    """Show rankings for a specific position or all positions."""
    positions = [position.upper()] if position else ["QB", "RB", "WR", "TE", "K", "DEF"]

    for pos in positions:
        players = get_players_by_position(pos)
        color = pos_color(pos)

        thick_separator()
        print(f"{C.BOLD}  {color}{pos} RANKINGS - 2026 HALF PPR{C.RESET}")
        thick_separator()
        print(f"{C.DIM}  {'Rank':<6} {'Tier':>4}  {'Player':<26} {'Team':<5} {'Bye':>3}  {'FPts':>7}{C.RESET}")
        separator()

        current_tier = None
        for p in players:
            tier = p.get("tier", 7)
            if tier != current_tier:
                if current_tier is not None:
                    print(f"  {C.DIM}{'.' * 60}{C.RESET}")
                current_tier = tier

            print(f"  {color}{p['pos_label']:>6}{C.RESET}  "
                  f" T{tier}   "
                  f"{p['name']:<26} "
                  f"{p['team']:<5}"
                  f"{p['bye']:>3}  "
                  f"{C.BOLD}{p['fpts']:>7.1f}{C.RESET}")

        separator()
        print()


# ---------------------------------------------------------------------------
# Display: Tier Breakdown
# ---------------------------------------------------------------------------
def show_tier_breakdown():
    """Show players grouped by their positional tier assignments."""
    thick_separator()
    print(f"{C.BOLD}  TIER BREAKDOWN - ALL POSITIONS{C.RESET}")
    thick_separator()

    for pos in ["QB", "RB", "WR", "TE", "K", "DEF"]:
        players = get_players_by_position(pos)
        color = pos_color(pos)

        print(f"\n  {color}{C.BOLD}{pos}s:{C.RESET}")

        current_tier = None
        for p in players:
            tier = p.get("tier", 7)
            if tier != current_tier:
                tier_label = TIER_LABELS.get(tier, f"Tier {tier}")
                print(f"    {C.DIM}Tier {tier} - {tier_label}{C.RESET}")
                current_tier = tier

            print(f"      {color}{p['pos_label']:>6}{C.RESET} {p['name']:<24} "
                  f"{p['team']:<4} {p['fpts']:>6.1f}")

    separator()
    print()


# ---------------------------------------------------------------------------
# Display: Compact View (for memorization)
# ---------------------------------------------------------------------------
def show_compact():
    """Ultra-compact view optimized for memorizing the top 150."""
    players = get_top_n(150)

    thick_separator()
    print(f"{C.BOLD}  TOP 150 - COMPACT MEMORIZATION VIEW{C.RESET}")
    thick_separator()

    # Print in columns of 3 for easier scanning
    current_tier = None
    rows = []
    for p in players:
        overall_tier = _get_overall_tier(p["overall_rank"])
        if overall_tier != current_tier:
            if rows:
                _flush_compact_rows(rows)
                rows = []
            _print_tier_break(overall_tier)
            current_tier = overall_tier

        color = pos_color(p["pos"])
        entry = f"{format_rank(p['overall_rank'])} {color}{p['pos_label']:>5}{C.RESET} {p['name']:<20}"
        rows.append(entry)

    if rows:
        _flush_compact_rows(rows)

    separator()
    print()


def _flush_compact_rows(rows):
    """Print rows in 2-column format."""
    for i in range(0, len(rows), 2):
        left = rows[i]
        right = rows[i + 1] if i + 1 < len(rows) else ""
        print(f"  {left}  {right}")


# ---------------------------------------------------------------------------
# CSV Export
# ---------------------------------------------------------------------------
def export_csv():
    """Export the full cheat sheet to CSV."""
    players = get_top_n(150)
    repl = get_replacement_level()

    filename = "draft_cheat_sheet_2026.csv"
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Overall Rank", "Pos Rank", "Position", "Player", "Team",
            "Bye", "Tier", "Projected FPts", "VORP"
        ])
        for p in players:
            vorp = calculate_vorp(p, repl)
            writer.writerow([
                p["overall_rank"], p["pos_label"], p["pos"],
                p["name"], p["team"], p["bye"], p.get("tier", ""),
                round(p["fpts"], 1), round(vorp, 1)
            ])

    print(f"\n  {C.GREEN}[OK] Exported to: {filepath}{C.RESET}\n")
    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]

    if "--csv" in args:
        export_csv()
    elif "--position" in args:
        idx = args.index("--position")
        pos = args[idx + 1] if idx + 1 < len(args) else None
        show_positional_rankings(pos)
    elif "--tiers" in args:
        show_tier_breakdown()
    elif "--compact" in args:
        show_compact()
    elif "--help" in args:
        print(__doc__)
    else:
        show_top_150()
        print()
        show_positional_rankings()


if __name__ == "__main__":
    main()
