## Claude Quick Load

Paste any URL below directly into Claude chat to load project context:

| File | Raw URL |
|---|---|
| `CLAUDE.md` | https://raw.githubusercontent.com/begb0037admin/clockify/main/CLAUDE.md |
| `docs/reference/CLOCKIFY_KB.md` | https://raw.githubusercontent.com/begb0037admin/clockify/main/docs/reference/CLOCKIFY_KB.md |
| `docs/STATUS.md` | https://raw.githubusercontent.com/begb0037admin/clockify/main/docs/STATUS.md |
| `docs/HANDOVER.md` | https://raw.githubusercontent.com/begb0037admin/clockify/main/docs/HANDOVER.md |

---

# Clockify Morning Dashboard

AI-assisted Clockify timesheet logging for Kevin Lelitte, HR Systems, University of Oxford.

**Live site:** https://begb0037admin.github.io/clockify/

---

## What it does

Opens each morning as a browser dashboard. Fetches the latest KB from GitHub, builds today's timesheet plan automatically based on the day of the week, and generates a ready-to-paste prompt for Claude in Chrome to log the entries.

## Morning routine

1. Open https://begb0037admin.github.io/clockify/
2. Review the plan — add any ad-hoc meetings
3. Hit **Copy prompt**
4. Paste into Claude in Chrome
5. Claude logs the timesheet, confirms 07:15, done

## What's in the repo

| File | Purpose |
|------|---------|
| `index.html` | Morning dashboard — fetches KB, builds plan, generates Chrome prompt |
| `MORNING_PROMPT.md` | Manual fallback prompt if the dashboard isn't available |
| `CLAUDE.md` | AI bootstrap entry point — read first |
| `docs/STATUS.md` | Current project state |
| `docs/HANDOVER.md` | Latest session handover note |
| `docs/reference/CLOCKIFY_KB.md` | Living knowledge base — project/task mappings |

## Hard rules

- Timesheet UI only — no API writes (Oxford SSO blocker)
- Never log more or less than 07:15 per working day
- Always update HANDOVER.md and push after each session
