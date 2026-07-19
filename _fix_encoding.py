import os

for fname in ['draft_rankings.py', 'draft_strategy.py', 'memorize.py', 'player_data.py']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    replacements = {
        '\u2550': '=',
        '\u2500': '-',
        '\u25b8': '>',
        '\u00b7': '.',
        '\u2713': '[OK]',
        '\u2717': '[X]',
        '\u2014': '-',
        '\u26a0': '[!]',
        '\u26a1': '!!',
        '\u2588': '#',
        '\U0001f3c8': '[FB]',
        '\U0001f9e0': '[Q]',
        '\U0001f4ca': '[S]',
        '\U0001f3af': '[T]',
        '\U0001f4dd': '[N]',
        '\U0001f4c8': '[P]',
        '\U0001f3c6': '[W]',
        '\U0001f4da': '[B]',
        '\U0001f4d6': '[R]',
        '\U0001f522': '[#]',
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    bad = [hex(ord(c)) for c in set(content) if ord(c) > 255]
    status = "clean" if not bad else str(bad)
    print(fname + ": " + status)
