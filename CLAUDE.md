# CLAUDE.md — kevin-work-hub

## Identity
- **Project:** Work Roadmap — a single consolidated dashboard collating everything live across Kevin's work estate (meetings, Work Inbox, Command Centre, Knowledge Base, HRIS) so he can see what's discussed, pending, and needs addressing in one place.
- **Owner:** Kevin Lelitte. **Engineering owner:** Drew (`begb0037admin/drew`).
- **Content owners:** Lauren (meeting-records section), Adam (knowledge-base section) — Drew structures and displays what they hand over, does not invent or curate their domain content itself.
- **Built:** 21 Aug 2026, v1.
- **Repo:** https://github.com/begb0037admin/kevin-work-hub — this repo was formerly `clockify` (Kevin's dormant time-tracking project scaffold). Renamed and repurposed 21 Aug 2026 at Kevin's confirmed decision (relayed by Lauren), specifically to avoid a naming collision with the still-live "Clockify" tool discussion elsewhere in the estate. All legacy Clockify-project content preserved intact in `Archive/clockify-project-2026-08-21/`, not deleted.
- **Live dashboard:** https://begb0037admin.github.io/kevin-work-hub/ (once Pages is enabled — check HANDOVER.md for current status)

## Bootstrap order
1. This file
2. `HANDOVER.md` — current state, what's pending, next action
3. `ROADMAP.md` — outstanding items / future iterations

## Architecture
| Component | Description |
|---|---|
| `build_roadmap.py` | Aggregator. Pulls live JSON from command-centre, work-inbox, hris-dashboard, hris-change-requests via the GitHub Contents API; encodes Lauren's and Adam's structured SendMessage sweeps for meetings/knowledge-base (their content, not scraped). Writes `data/roadmap.json`. Run manually for now — `python build_roadmap.py` from repo root. |
| `data/roadmap.json` | The single data file the dashboard reads. One `pillars[]` array — one entry per source area (meetings / work-inbox / command-centre / knowledge-base / hris), each with a `status` (ok / attention / pending), a `summary`, and whichever detail arrays apply (`areas`, `overdue`, `items`, `urgent_items`, `needs_items`, `today_open_items`, `change_requests`). |
| `index.html` / `css/styles.css` / `js/app.js` | Static read-only viewer, no write path — this dashboard doesn't need one, unlike command-centre's task board. Oxford navy sidebar house style, matching command-centre/work-inbox. Client JS fetches `data/roadmap.json` cache-busted and renders an overview strip + one detail card per pillar. |

## Data flow
This is a **snapshot pipeline, not live cross-repo fetching in the browser** — `build_roadmap.py` pulls everything server-side (well, session-side) via `gh api`, writes one combined `data/roadmap.json`, and that's what the page actually loads. Re-run the aggregator and push to refresh. Not yet wired to any schedule — see ROADMAP.md.

## History note
The task was originally dispatched as "create `begb0037admin/hr-work-roadmap`." That repo was created and briefly scaffolded locally, but nothing was ever pushed to it (confirmed empty). Lauren then relayed Kevin's confirmed decision to repurpose `clockify` as `kevin-work-hub` instead, verified directly (repo rename confirmed live, legacy content confirmed archived) before redirecting here. `hr-work-roadmap` remains on GitHub, empty — flagged to Kevin/Lauren for a delete-or-leave decision, not deleted unilaterally.
