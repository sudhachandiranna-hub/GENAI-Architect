#!/usr/bin/env python3
"""
add_day.py — Updates index.html to unlock a new day after you publish it.

USAGE:
    python3 add_day.py 4

This will:
1. Find day 4's box in index.html (currently locked)
2. Convert it to a "done" box linking to day-04.html
3. Update the overall progress bar and "X / 45 days" counter
4. Save index.html in place

Run this from the same folder as index.html and your day-XX.html files,
right after you create/publish a new day's page.
"""

import sys
import re

TOTAL_DAYS = 45

def pad(n):
    return str(n).zfill(2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 add_day.py <day_number>")
        sys.exit(1)

    day_num = int(sys.argv[1])
    if day_num < 1 or day_num > TOTAL_DAYS:
        print(f"Day number must be between 1 and {TOTAL_DAYS}")
        sys.exit(1)

    day_str = pad(day_num)

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Pattern for the locked box of this day
    locked_pattern = re.compile(
        r'<div class="day-box locked"><span class="lock-icon">🔒</span>'
        rf'<span class="day-num">{day_str}</span><span class="day-status">Soon</span></div>'
    )

    if not locked_pattern.search(html):
        # Check if it's already unlocked
        if f'day-{day_str}.html' in html:
            print(f"Day {day_str} is already unlocked in index.html. Nothing to do.")
            sys.exit(0)
        else:
            print(f"Could not find a locked box for Day {day_str}. Check index.html manually.")
            sys.exit(1)

    new_box = (
        f'<a href="day-{day_str}.html" class="day-box done">'
        f'<span class="day-check">✓</span>'
        f'<span class="day-num">{day_str}</span>'
        f'<span class="day-status">View</span></a>'
    )

    html = locked_pattern.sub(new_box, html, count=1)

    # Update progress bar + counter
    # Find the highest unlocked day number to compute new progress
    unlocked_days = re.findall(r'day-(\d{2})\.html', html)
    max_day = max(int(d) for d in unlocked_days) if unlocked_days else day_num
    completed = max(max_day, day_num)
    pct = round((completed / TOTAL_DAYS) * 100, 2)

    html = re.sub(
        r'(<span class="progress-pct" id="progressPct">)\d+ / 45 days(</span>)',
        rf'\g<1>{completed} / {TOTAL_DAYS} days\g<2>',
        html
    )
    html = re.sub(
        r'(id="progressBar" style="width: )[\d.]+%;',
        rf'\g<1>{pct}%;',
        html
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Day {day_str} unlocked in index.html")
    print(f"✅ Progress updated: {completed} / {TOTAL_DAYS} days ({pct}%)")
    print(f"\nNext steps:")
    print(f"   git add index.html day-{day_str}.html")
    print(f"   git commit -m \"Day {day_str}: unlock + publish\"")
    print(f"   git push origin main")

if __name__ == "__main__":
    main()
