# CLAUDE.md — Clockify
> AI bootstrap entry point. Read this first.
> Keep this file under 200 lines. Push details to linked docs.

## Identity
- **Project:** Clockify
- **Purpose:** AI-assisted Clockify Timesheet logging for Kevin Lelitte, HR Systems, University of Oxford.
- **Owner:** Kevin Lelitte, Manager/Director HR Systems
- **Status:** Active
- **Path:** https://github.com/begb0037admin/clockify

## Bootstrap Order
1. This file (orientation)
2. `docs/STATUS.md` (current state)
3. `docs/HANDOVER.md` (latest session note)
4. `docs/reference/CLOCKIFY_KB.md` (knowledge base — read for ANY Clockify task)
5. Read other docs on demand only.

Do NOT ask Kevin for a recap. The docs above are the recap.

Do NOT attempt Clockify API writes. Kevin's Oxford SSO account cannot authenticate for POST requests. Timesheet UI is the only method.

## Where Things Live
| What | Where |
|---|---|
| Current state | `docs/STATUS.md` |
| Latest handover | `docs/HANDOVER.md` |
| Clockify knowledge base | `docs/reference/CLOCKIFY_KB.md` |
| Open questions | `docs/OPEN_QUESTIONS.md` |
| Roadmap | `docs/ROADMAP.md` |
| Framework reference | `PROJECT_OS.md` |
| Agent roles and handoffs | `AGENT_MODEL.md` |
| Rollover procedure | `ROLLOVER_SOP.md` |

## Conventions
- Timesheet UI only — no API writes (SSO blocker, confirmed 1 Jun 2026)
- Duration format: HH:MM (e.g. 01:00, 00:15)
- Working day = 7:15 total. Gap fill always = Focussed time: Email and Teams messages (BAU)
- Calendar sync: Outlook to Clockify auto-populates Calendar view. Timesheet is the manual logging layer on top.
- Chrome extension (BEGB0037) is available for browser automation.

## Hard Rules
- Never attempt Clockify API writes
- Never log more or less than 7:15 per working day without Kevin's explicit instruction
- Always read CLOCKIFY_KB.md before touching the Timesheet
- Always update CLOCKIFY_KB.md when a new project/task mapping is confirmed
- Always update HANDOVER.md at end of session

## Out of Scope
- Clockify API automation (SSO blocker — do not re-investigate)
- Mobile or non-Chrome browser automation
- Modifying Clockify project/task structure (read only)

## Glossary
- **Gap fill** — Remaining hours after meetings logged, assigned to Focussed time: Email and Teams messages (BAU)
- **Weekly Standard** — Saved Clockify template with 4 standard rows. Apply on Mondays only.
- **Busy block** — Outlook calendar event synced as "Busy" with no title. Mapping must be confirmed with Kevin.
- **KB** — CLOCKIFY_KB.md, the living knowledge base for this project.

## AI Collaboration Notes
- Preferred style: direct, concise. Kevin is tech-savvy — no hand-holding.
- Chrome extension BEGB0037 is available for browser automation.
- Seat model: follow AGENT_MODEL.md. Seat A reasons. Cowork writes to disk.
- Update CLOCKIFY_KB.md whenever a new mapping is confirmed mid-session.

## Branch and Merge Protocol
Always push directly to main. If a branch must be used, merge it to main immediately upon completion — never leave files on a branch.
