#!/usr/bin/env python3
"""
add_day.py -- Updates index.html to unlock a new day after you publish it.

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
        print("Day number must be between 1 and " + str(TOTAL_DAYS))
        sys.exit(1)

    day_str = pad(day_num)

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    locked_pattern = re.compile(
        r'<div class="day-box locked"><span class="lock-icon">\U0001F512</span>'
        r'<span class="day-num">' + day_str + r'</span><span class="day-date">([^<]+)</span></div>'
    )

    match = locked_pattern.search(html)
    if not match:
        if "day-" + day_str + ".html" in html:
            print("Day " + day_str + " is already unlocked in index.html. Nothing to do.")
            sys.exit(0)
        else:
            print("Could not find a locked box for Day " + day_str + ". Check index.html manually.")
            sys.exit(1)

    date_text = match.group(1)
    new_box = (
        '<a href="day-' + day_str + '.html" class="day-box done">'
        '<span class="day-check">✓</span>'
        '<span class="day-num">' + day_str + '</span>'
        '<span class="day-date">' + date_text + '</span></a>'
    )

    html = locked_pattern.sub(new_box, html, count=1)

    unlocked_days = re.findall(r'day-(\d{2})\.html', html)
    max_day = max(int(d) for d in unlocked_days) if unlocked_days else day_num
    completed = max(max_day, day_num)
    pct = round((completed / TOTAL_DAYS) * 100, 2)

    html = re.sub(
        r'(<span class="progress-pct" id="progressPct">)\d+ / 45 days(</span>)',
        r'\g<1>' + str(completed) + ' / ' + str(TOTAL_DAYS) + r' days\g<2>',
        html
    )
    html = re.sub(
        r'(id="progressBar" style="width: )[\d.]+%;',
        r'\g<1>' + str(pct) + '%;',
        html
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Day " + day_str + " unlocked in index.html")
    print("Progress updated: " + str(completed) + " / " + str(TOTAL_DAYS) + " days (" + str(pct) + "%)")
    print("Next steps:")
    print("   git add index.html day-" + day_str + ".html")
    print("   git commit -m Day-" + day_str + "-unlock-publish")
    print("   git push origin main")

if __name__ == "__main__":
    main()
