# CLAUDE.md — kevin-work-hub

## Identity
- **Project:** Work Roadmap — a living, curated backlog of things AI agents have noticed are broken, missing, or worth improving across Kevin's work estate (Meetings, Work Inbox, Command Centre, Knowledge Base, HRIS, Cross-cutting) while doing other work. **Not** a live-metrics mirror of what those systems already show — see "Data model" below, this distinction is the whole point of the repo and was gotten wrong in v1.
- **Owner:** Kevin Lelitte. **Engineering owner:** Drew (`begb0037admin/drew`).
- **Content owners:** every agent who works the estate can and should add items — Lauren (meeting-records), Adam (knowledge base), Drew (work-inbox/command-centre/HRIS engineering), Markey, Matthew. Drew owns the pipeline/schema; the backlog's actual content is genuinely cross-agent.
- **Built:** 21 Aug 2026. v1 (live-metrics mirror) rejected same day by Kevin. v2 (curated backlog) built same day.
- **Repo:** https://github.com/begb0037admin/kevin-work-hub — this repo was formerly `clockify` (Kevin's dormant time-tracking project scaffold). Renamed and repurposed 21 Aug 2026 at Kevin's confirmed decision (relayed by Lauren), specifically to avoid a naming collision with the still-live "Clockify" tool discussion elsewhere in the estate. All legacy Clockify-project content preserved intact in `Archive/clockify-project-2026-08-21/`, not deleted.
- **Live dashboard:** https://hub.lelitte.co.uk/ (primary, custom domain added 21 Aug 2026 — CNAME file + GitHub Pages custom-domain setting configured; DNS record in Cloudflare not yet added, see HANDOVER.md for status) — https://begb0037admin.github.io/kevin-work-hub/ remains live as fallback.

## Bootstrap order
1. This file
2. `HANDOVER.md` — current state, what's pending, next action
3. `ROADMAP.md` — outstanding items / future iterations

## Data model — v2, curated backlog (NOT live metrics)

**This is the single most important thing to get right about this repo — read before changing anything.** v1 mirrored live counts/metrics from command-centre, work-inbox and hris-dashboard (task counts, ticket counts, needs-reply counts). Kevin rejected that on sight, 21 Aug 2026, his own words: "that's of no use to me, I already have that." What he actually wants: **a living cross-estate backlog of things AI agents have noticed are broken, missing, or worth improving while doing other work** — bugs, gaps, improvement ideas, process fixes — flagged in the moment ("hey, there's a possible improvement here, I've just noticed by doing this, and that goes on this roadmap"), not a snapshot of current-state numbers that already exist elsewhere.

`data/backlog.json` is the actual source of truth — a flat, append-only array of items, each `{id, title, area, type, severity, found_by, found_date, status, recommendation, source}`. `area` is one of Meetings / Work Inbox / Command Centre / Knowledge Base / HRIS / Cross-cutting. `type` is bug / gap / improvement-idea / process-fix. `severity` is low / medium / high. `status` is open / in-progress / done. **Any agent** can add to it — see `add_backlog_item.py`, or just append an object matching the shape and push. Do not silently invent seed items — every entry needs a real, checkable `source` (a commit, a memory file, a live-verified fact). If you can't independently verify a claim someone relays to you, say so in the item rather than asserting it as fact — see cc-01 in the current backlog for how a partially-unconfirmed claim was handled.

## Architecture
| Component | Description |
|---|---|
| `data/backlog.json` | Source of truth. Curated, append-only backlog of real findings. Read this before `build_roadmap.py` — it's the actual content. |
| `add_backlog_item.py` | CLI helper any agent can run to append one item without hand-editing JSON. Only writes locally — still needs commit+push. |
| `build_roadmap.py` | Reads `data/backlog.json`, groups items by `area`, computes each pillar's status (attention / ok / pending) from open-item severity/count, writes `data/roadmap.json` for the frontend. No longer pulls live task/ticket/email counts from any other repo — that was the v1 mistake. Run manually — `python build_roadmap.py` from repo root, after editing/adding to backlog.json. |
| `index.html` / `css/styles.css` / `js/app.js` | Static read-only viewer, no write path. Strict house-style compliance per `command-centre/BRANDING.md` v2.0 (verified 21 Aug 2026): exact sidebar brand block, 340px sidebar, real `images/oxford-crest.jpg` (not base64), plain white `#fff` cards, no colour-coded tiles — status shown only via small text chips reusing the existing `.badge` token set. One tab per pillar/area (sidebar `sb-nav` links, `.active` state), single visible `.pillar-view` at a time, mirroring command-centre's own `showView()`/`nav-<id>`/`.active` pattern exactly rather than inventing a new one. Each backlog item renders as a card: title, type/severity/status chips, recommendation, source. Client JS fetches `data/roadmap.json` cache-busted. |
| `images/oxford-crest.jpg` | Real crest image file, copied from command-centre's own asset (not regenerated/reinterpreted). Never base64-embed, delete, move, or rename per BRANDING.md's hard rules. |

## Data flow
`data/backlog.json` (hand/script-maintained, the real content) → `build_roadmap.py` (pure grouping/formatting, session-run via `python build_roadmap.py`) → `data/roadmap.json` (what the page actually fetches, cache-busted). Not wired to any schedule, and shouldn't go back to pulling from live sources — the whole point is this is curated, not auto-mirrored. Adding an item is: run `add_backlog_item.py` (or hand-edit `data/backlog.json`) → `python build_roadmap.py` → commit both files → push.

## History note
The task was originally dispatched as "create `begb0037admin/hr-work-roadmap`." That repo was created and briefly scaffolded locally, but nothing was ever pushed to it (confirmed empty). Lauren then relayed Kevin's confirmed decision to repurpose `clockify` as `kevin-work-hub` instead, verified directly (repo rename confirmed live, legacy content confirmed archived) before redirecting here. `hr-work-roadmap` remains on GitHub, empty — flagged to Kevin/Lauren for a delete-or-leave decision, not deleted unilaterally.

v1 (live-metrics dashboard, 5 stacked cards, some colour-coded tiles) was built, pushed live, screenshotted and shown to Kevin same night. He rejected it on two grounds: layout (should be tabs, not stacked cards) and branding (deviated from `command-centre/BRANDING.md`, colour-coded tiles not used elsewhere in the estate). While fixing those two, Lauren relayed a third, deeper correction: the whole data model was wrong — this should never have been a live-metrics mirror. v2 (this version) rebuilds on the corrected data model plus both original fixes in one pass.
