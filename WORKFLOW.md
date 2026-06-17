# GENAI Architect — Daily Notes Publishing Workflow

Repo: https://github.com/sudhachandiranna-hub/GENAI-Architect
Live hub: https://sudhachandiranna-hub.github.io/GENAI-Architect/

## Structure (flat — no subfolders)
- `index.html` — hub page, 45-day grid, links to each day, overall progress bar
- `day-01.html` … `day-45.html` — individual day notes, same folder as index.html
- `add_day.py` — unlocks a day in index.html + updates progress bar

## Every time a new day's HTML is ready:

1. **Run `add_day.py` FIRST, before anything else:**
   ```
   python3 add_day.py <day_number>
   ```
   This flips that day's box from 🔒 locked → ✓ done in `index.html` and recalculates
   the overall progress % (day / 45).

2. Place the new `day-XX.html` in the same folder as `index.html` (repo root — not a subfolder).

3. Commit and push all three: `index.html`, `day-XX.html`, and `add_day.py` (if changed).

4. Verify live:
   - `https://sudhachandiranna-hub.github.io/GENAI-Architect/`
   - `https://sudhachandiranna-hub.github.io/GENAI-Architect/day-XX.html`

## Known recurring fixes to check on each new day file
- Footer year should be **2026**, not 2024.
- Progress % span should show an actual percentage (`day/45`), not placeholder text like "Week 1 · Day X of 6W".
- Course length is **6 weeks / 45 days** — never "60 days".

## Note
`add_day.py` is idempotent — running it on an already-unlocked day just prints
"already unlocked, nothing to do" and exits cleanly. Safe to re-run.
