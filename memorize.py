"""
Fantasy Football 2026-2027 - Memorization Helper
==================================================
ESPN League 756823 | Half PPR | 4pt Passing TDs

Helps you memorize the top 150 players for your in-person draft.

Modes:
  1. Flashcard quiz - "Who is the #27 overall pick?" / "What rank is Puka Nacua?"
  2. Position drills - Quiz on just QBs, RBs, WRs, or TEs
  3. Tier boundary drills - Test if you know where value drop-offs are
  4. Progress tracking - See which players you miss the most
  5. Condensed memory aids - Tier summaries and mnemonic groupings

Usage:
  python memorize.py                   # Main menu
  python memorize.py --flash           # Flashcard mode
  python memorize.py --position QB     # Position drill
  python memorize.py --tiers           # Tier boundary drill
  python memorize.py --summary         # Condensed memory aids
  python memorize.py --stats           # Show progress stats
"""

import sys
import random
import json
import os
from player_data import get_top_n, get_players_by_position

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

# Progress file location
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".memorize_progress.json")

TIER_LABELS = {
    1: "TIER 1 - CAN'T-MISS (Picks 1-12)",
    2: "TIER 2 - STRONG STARTERS (Picks 13-24)",
    3: "TIER 3 - CORE BUILDERS (Picks 25-36)",
    4: "TIER 4 - VALUE ZONE (Picks 37-60)",
    5: "TIER 5 - DEPTH & SLEEPERS (Picks 61-90)",
    6: "TIER 6 - LATE ROUND UPSIDE (Picks 91-120)",
    7: "TIER 7 - FINAL PICKS (Picks 121-150)",
}


def separator(char="-", width=72):
    print(f"{C.DIM}{char * width}{C.RESET}")


def thick_separator(width=72):
    print(f"{C.BOLD}{'=' * width}{C.RESET}")


def get_tier(rank: int) -> int:
    if rank <= 12: return 1
    elif rank <= 24: return 2
    elif rank <= 36: return 3
    elif rank <= 60: return 4
    elif rank <= 90: return 5
    elif rank <= 120: return 6
    else: return 7


# ---------------------------------------------------------------------------
# Progress Tracking
# ---------------------------------------------------------------------------
def load_progress() -> dict:
    """Load progress from file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"correct": {}, "wrong": {}, "total_questions": 0, "total_correct": 0}


def save_progress(progress: dict):
    """Save progress to file."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def record_answer(progress: dict, player_name: str, correct: bool):
    """Record a quiz answer."""
    progress["total_questions"] = progress.get("total_questions", 0) + 1
    if correct:
        progress["total_correct"] = progress.get("total_correct", 0) + 1
        progress["correct"][player_name] = progress.get("correct", {}).get(player_name, 0) + 1
    else:
        progress["wrong"][player_name] = progress.get("wrong", {}).get(player_name, 0) + 1
    save_progress(progress)


# ---------------------------------------------------------------------------
# Flashcard Quiz Mode
# ---------------------------------------------------------------------------
def run_flashcard_quiz(num_questions: int = 20):
    """Run a flashcard-style quiz on the top 150 players."""
    players = get_top_n(150)
    progress = load_progress()

    thick_separator()
    print(f"{C.BOLD}  [Q] FLASHCARD QUIZ - TOP 150 PLAYERS{C.RESET}")
    thick_separator()
    print(f"  Answer questions about player ranks and names.")
    print(f"  Type your answer and press Enter. Type 'quit' to stop.")
    print(f"  Answers within ±5 ranks count as close (partial credit).\n")

    score = 0
    asked = 0
    quiz_types = ["name_to_rank", "rank_to_name", "pos_rank_to_name"]

    # Weight harder players more if they've been missed before
    wrong_players = set(progress.get("wrong", {}).keys())

    while asked < num_questions:
        quiz_type = random.choice(quiz_types)
        player = _pick_player(players, wrong_players)

        try:
            if quiz_type == "name_to_rank":
                correct = _quiz_name_to_rank(player)
            elif quiz_type == "rank_to_name":
                correct = _quiz_rank_to_name(player, players)
            else:
                correct = _quiz_pos_rank_to_name(player)
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break

        if correct is None:  # quit
            break

        if correct:
            score += 1
            print(f"  {C.GREEN}[OK] Correct!{C.RESET}")
        else:
            print(f"  {C.RED}[X] Wrong!{C.RESET}")

        record_answer(progress, player["name"], correct)
        asked += 1
        print(f"  {C.DIM}Score: {score}/{asked} ({score/asked*100:.0f}%){C.RESET}\n")

    print(f"\n  {C.BOLD}Final Score: {score}/{asked}")
    pct = (score / asked * 100) if asked > 0 else 0
    if pct >= 80:
        print(f"  {C.GREEN}[W] Excellent! You're draft-ready!{C.RESET}")
    elif pct >= 60:
        print(f"  {C.YELLOW}[B] Good, but keep studying the middle tiers.{C.RESET}")
    else:
        print(f"  {C.RED}[R] Keep practicing! Focus on tiers 3-5.{C.RESET}")
    separator()
    print()


def _pick_player(players: list, wrong_players: set):
    """Pick a player, weighting missed players more heavily."""
    # 30% chance to pick a previously missed player
    if wrong_players and random.random() < 0.3:
        missed = [p for p in players if p["name"] in wrong_players]
        if missed:
            return random.choice(missed)
    return random.choice(players)


def _quiz_name_to_rank(player: dict) -> bool:
    """Given a player name, guess their overall rank."""
    color = POS_COLORS.get(player["pos"], C.WHITE)
    answer = input(f"  {C.BOLD}What is the overall rank of "
                   f"{color}{player['name']}{C.RESET} ({player['pos']}, {player['team']})? > ").strip()

    if answer.lower() == "quit":
        return None

    try:
        guess = int(answer.replace("#", ""))
        actual = player["overall_rank"]
        diff = abs(guess - actual)

        if diff == 0:
            return True
        elif diff <= 5:
            print(f"  {C.YELLOW}~ Close! Actual rank: #{actual} (you said #{guess}, off by {diff}){C.RESET}")
            return True
        else:
            print(f"  {C.DIM}  Actual rank: #{actual}{C.RESET}")
            return False
    except ValueError:
        print(f"  {C.DIM}  Actual rank: #{player['overall_rank']}{C.RESET}")
        return False


def _quiz_rank_to_name(player: dict, all_players: list) -> bool:
    """Given an overall rank, name the player."""
    rank = player["overall_rank"]
    answer = input(f"  {C.BOLD}Who is ranked #{rank} overall? > {C.RESET}").strip()

    if answer.lower() == "quit":
        return None

    actual_name = player["name"].lower()
    # Check for partial match (last name match is fine)
    if answer.lower() in actual_name or actual_name.split()[-1].lower() in answer.lower():
        color = POS_COLORS.get(player["pos"], C.WHITE)
        print(f"  {C.DIM}  {color}{player['pos_label']}{C.RESET} {C.DIM}{player['name']} ({player['team']}){C.RESET}")
        return True
    else:
        color = POS_COLORS.get(player["pos"], C.WHITE)
        print(f"  {C.DIM}  Answer: {color}{player['pos_label']}{C.RESET} {C.DIM}{player['name']} ({player['team']}){C.RESET}")
        return False


def _quiz_pos_rank_to_name(player: dict) -> bool:
    """Given a positional rank, name the player."""
    color = POS_COLORS.get(player["pos"], C.WHITE)
    answer = input(f"  {C.BOLD}Who is {color}{player['pos_label']}{C.RESET}{C.BOLD} "
                   f"(#{player['pos_rank']} {player['pos']})? > {C.RESET}").strip()

    if answer.lower() == "quit":
        return None

    actual_name = player["name"].lower()
    if answer.lower() in actual_name or actual_name.split()[-1].lower() in answer.lower():
        print(f"  {C.DIM}  {player['name']} ({player['team']}) - Overall #{player['overall_rank']}{C.RESET}")
        return True
    else:
        print(f"  {C.DIM}  Answer: {player['name']} ({player['team']}) - Overall #{player['overall_rank']}{C.RESET}")
        return False


# ---------------------------------------------------------------------------
# Position Drill
# ---------------------------------------------------------------------------
def run_position_drill(position: str, num_questions: int = 15):
    """Quiz focused on a single position."""
    players = get_players_by_position(position)
    if not players:
        print(f"  {C.RED}No players found for position: {position}{C.RESET}")
        return

    progress = load_progress()
    color = POS_COLORS.get(position, C.WHITE)

    thick_separator()
    print(f"{C.BOLD}  [T] POSITION DRILL - {color}{position}{C.RESET}")
    thick_separator()
    print(f"  How well do you know the {position} rankings?")
    print(f"  Type 'quit' to stop.\n")

    score = 0
    asked = 0

    while asked < num_questions and asked < len(players):
        # Mix up question types
        player = random.choice(players)

        if random.random() < 0.5:
            # Given name, guess positional rank
            answer = input(f"  {C.BOLD}What is {player['name']}'s {color}{position}{C.RESET}{C.BOLD} rank? > {C.RESET}").strip()
            if answer.lower() == "quit":
                break

            try:
                guess = int(answer.replace("#", "").replace(position, ""))
                actual = player["pos_rank"]
                diff = abs(guess - actual)

                if diff <= 2:
                    print(f"  {C.GREEN}[OK] Correct! {player['pos_label']}{C.RESET}")
                    score += 1
                    record_answer(progress, player["name"], True)
                else:
                    print(f"  {C.RED}[X] Answer: {player['pos_label']}{C.RESET}")
                    record_answer(progress, player["name"], False)
            except ValueError:
                print(f"  {C.RED}[X] Answer: {player['pos_label']}{C.RESET}")
                record_answer(progress, player["name"], False)
        else:
            # Given positional rank, name the player
            answer = input(f"  {C.BOLD}Who is {color}{player['pos_label']}{C.RESET}{C.BOLD}? > {C.RESET}").strip()
            if answer.lower() == "quit":
                break

            actual_name = player["name"].lower()
            if answer.lower() in actual_name or actual_name.split()[-1].lower() in answer.lower():
                print(f"  {C.GREEN}[OK] {player['name']} ({player['team']}){C.RESET}")
                score += 1
                record_answer(progress, player["name"], True)
            else:
                print(f"  {C.RED}[X] Answer: {player['name']} ({player['team']}){C.RESET}")
                record_answer(progress, player["name"], False)

        asked += 1
        print(f"  {C.DIM}Score: {score}/{asked}{C.RESET}\n")

    separator()
    print(f"  {C.BOLD}Position Drill Score: {score}/{asked}{C.RESET}\n")


# ---------------------------------------------------------------------------
# Tier Boundary Drill
# ---------------------------------------------------------------------------
def run_tier_drill():
    """Test knowledge of tier boundaries - where the value cliffs are."""
    players = get_top_n(150)
    progress = load_progress()

    thick_separator()
    print(f"{C.BOLD}  [S] TIER BOUNDARY DRILL{C.RESET}")
    thick_separator()
    print(f"  Can you identify which tier/round each player belongs in?")
    print(f"  Type the tier number (1-7) or 'quit' to stop.\n")

    for label, desc in TIER_LABELS.items():
        print(f"  {C.DIM}{desc}{C.RESET}")
    print()

    score = 0
    asked = 0
    num_questions = 20

    while asked < num_questions:
        player = random.choice(players)
        color = POS_COLORS.get(player["pos"], C.WHITE)

        answer = input(f"  {C.BOLD}What tier is {color}{player['name']}{C.RESET} "
                       f"({player['pos']}, {player['team']})? [1-7] > ").strip()

        if answer.lower() == "quit":
            break

        try:
            guess = int(answer)
            actual_tier = get_tier(player["overall_rank"])

            if guess == actual_tier:
                print(f"  {C.GREEN}[OK] Correct! Tier {actual_tier} (Overall #{player['overall_rank']}){C.RESET}")
                score += 1
                record_answer(progress, player["name"], True)
            elif abs(guess - actual_tier) == 1:
                print(f"  {C.YELLOW}~ Close! Tier {actual_tier} (Overall #{player['overall_rank']}){C.RESET}")
                score += 0.5
                record_answer(progress, player["name"], True)
            else:
                print(f"  {C.RED}[X] Tier {actual_tier} (Overall #{player['overall_rank']}){C.RESET}")
                record_answer(progress, player["name"], False)
        except ValueError:
            print(f"  {C.RED}[X] Tier {get_tier(player['overall_rank'])} (Overall #{player['overall_rank']}){C.RESET}")
            record_answer(progress, player["name"], False)

        asked += 1
        print(f"  {C.DIM}Score: {score}/{asked}{C.RESET}\n")

    separator()
    print(f"  {C.BOLD}Tier Drill Score: {score}/{asked}{C.RESET}\n")


# ---------------------------------------------------------------------------
# Condensed Memory Aids
# ---------------------------------------------------------------------------
def show_memory_aids():
    """Generate condensed memorization aids grouped by tier."""
    players = get_top_n(150)

    thick_separator()
    print(f"{C.BOLD}  [N] CONDENSED MEMORY AIDS - TOP 150{C.RESET}")
    thick_separator()

    # Group by tier
    tiers = {}
    for p in players:
        tier = get_tier(p["overall_rank"])
        if tier not in tiers:
            tiers[tier] = {"QB": [], "RB": [], "WR": [], "TE": [], "K": [], "DEF": []}
        tiers[tier][p["pos"]].append(p)

    for tier_num in sorted(tiers.keys()):
        tier_data = tiers[tier_num]
        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
        print(f"\n  {C.BOLD}{C.YELLOW}> {label}{C.RESET}")
        separator("-", 72)

        for pos in ["QB", "RB", "WR", "TE", "K", "DEF"]:
            if not tier_data[pos]:
                continue
            color = POS_COLORS.get(pos, C.WHITE)
            names = [f"{p['name']}" for p in tier_data[pos]]
            print(f"  {color}{pos:>3}{C.RESET}: {', '.join(names)}")

        # Mnemonic: First letters of player names
        all_names = []
        for pos in ["RB", "WR", "QB", "TE", "K", "DEF"]:
            all_names.extend([p["name"].split()[-1][0] for p in tier_data[pos]])
        if all_names:
            mnemonic = "".join(all_names[:12])
            print(f"  {C.DIM}Mnemonic (last-name initials): {mnemonic}{C.RESET}")

    # Position-specific quick reference
    print(f"\n\n  {C.BOLD}QUICK REFERENCE - TOP AT EACH POSITION{C.RESET}")
    separator()

    for pos in ["QB", "RB", "WR", "TE"]:
        color = POS_COLORS.get(pos, C.WHITE)
        pos_players = get_players_by_position(pos)[:10]
        names = [p["name"].split()[-1] for p in pos_players]
        print(f"  {color}{pos} Top 10 (surnames):{C.RESET}")
        print(f"    {' -> '.join(names)}")
        print()

    # Key numbers to memorize
    print(f"\n  {C.BOLD}[#] KEY NUMBERS TO MEMORIZE{C.RESET}")
    separator()
    top_players = get_top_n(12)
    print(f"  Top 12 (Round 1 territory):")
    for p in top_players:
        color = POS_COLORS.get(p["pos"], C.WHITE)
        print(f"    #{p['overall_rank']:<3} {color}{p['pos_label']:>5}{C.RESET} {p['name']}")

    separator()
    print()


# ---------------------------------------------------------------------------
# Progress Stats
# ---------------------------------------------------------------------------
def show_progress_stats():
    """Show memorization progress and weak spots."""
    progress = load_progress()

    thick_separator()
    print(f"{C.BOLD}  [P] MEMORIZATION PROGRESS{C.RESET}")
    thick_separator()

    total_q = progress.get("total_questions", 0)
    total_c = progress.get("total_correct", 0)

    if total_q == 0:
        print(f"\n  {C.DIM}No quiz data yet. Run some drills first!{C.RESET}\n")
        return

    pct = total_c / total_q * 100
    print(f"\n  Total questions: {total_q}")
    print(f"  Total correct:  {total_c} ({pct:.1f}%)")

    # Most missed players
    wrong = progress.get("wrong", {})
    if wrong:
        print(f"\n  {C.RED}{C.BOLD}MOST MISSED PLAYERS (study these!){C.RESET}")
        sorted_wrong = sorted(wrong.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_wrong[:10]:
            bar = "#" * count
            print(f"    {name:<26} missed {count}x  {C.RED}{bar}{C.RESET}")

    # Most correct players
    correct = progress.get("correct", {})
    if correct:
        print(f"\n  {C.GREEN}{C.BOLD}MOST CONFIDENT PLAYERS{C.RESET}")
        sorted_correct = sorted(correct.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_correct[:10]:
            bar = "#" * count
            print(f"    {name:<26} correct {count}x  {C.GREEN}{bar}{C.RESET}")

    separator()
    print()


# ---------------------------------------------------------------------------
# Main Menu
# ---------------------------------------------------------------------------
def main_menu():
    """Interactive main menu."""
    thick_separator()
    print(f"{C.BOLD}  [Q] FANTASY FOOTBALL 2026 - MEMORIZATION HELPER{C.RESET}")
    thick_separator()
    print(f"""
  {C.BOLD}1{C.RESET}. Flashcard Quiz (top 150 overall)
  {C.BOLD}2{C.RESET}. Position Drill (pick a position)
  {C.BOLD}3{C.RESET}. Tier Boundary Drill
  {C.BOLD}4{C.RESET}. Memory Aids & Summary
  {C.BOLD}5{C.RESET}. Progress Stats
  {C.BOLD}6{C.RESET}. Quit
    """)

    while True:
        try:
            choice = input(f"  {C.CYAN}Choose [1-6]>{C.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break

        if choice == "1":
            run_flashcard_quiz()
        elif choice == "2":
            pos = input(f"  {C.DIM}Which position? (QB/RB/WR/TE)>{C.RESET} ").strip().upper()
            if pos in ["QB", "RB", "WR", "TE", "K", "DEF"]:
                run_position_drill(pos)
            else:
                print(f"  {C.RED}Invalid position. Choose from: QB, RB, WR, TE, K, DEF{C.RESET}")
        elif choice == "3":
            run_tier_drill()
        elif choice == "4":
            show_memory_aids()
        elif choice == "5":
            show_progress_stats()
        elif choice == "6" or choice.lower() == "quit":
            print(f"\n  {C.YELLOW}Good luck at the draft! [FB]{C.RESET}\n")
            break
        else:
            print(f"  {C.RED}Choose 1-6{C.RESET}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]

    if "--flash" in args:
        run_flashcard_quiz()
    elif "--position" in args:
        idx = args.index("--position")
        pos = args[idx + 1].upper() if idx + 1 < len(args) else "QB"
        run_position_drill(pos)
    elif "--tiers" in args:
        run_tier_drill()
    elif "--summary" in args:
        show_memory_aids()
    elif "--stats" in args:
        show_progress_stats()
    elif "--help" in args:
        print(__doc__)
    else:
        main_menu()


if __name__ == "__main__":
    main()
