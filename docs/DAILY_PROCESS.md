# DAILY_PROCESS.md — Clockify Daily Timesheet Routine
> Established: 2026-06-26
> Owner: Kevin Lelitte

---

## The One-Line Summary
Each morning, Claude reads Kevin's calendar, maps meetings to Clockify, and reports back a ready-to-log timesheet. Kevin logs it in the Clockify UI. Done in under 60 seconds.

---

## Trigger
Kevin says: "clockify" (or any variation — "do my clockify", "timesheet", etc.)

---

## What Claude Does (in order)

### 1. Check briefing.json freshness
Fetch `begb0037admin/work-inbox/data/briefing.json` → check `refreshed_at`.

**If stale (over 24 hours old):**
> "Your inbox briefing is stale (last refreshed [date/time]). Run `fetch_inbox.py` on your admin machine first, then come back and say 'clockify' again."

**Stop here. Do not proceed until Kevin confirms it has been refreshed.**

### 2. Read today's calendar
Read `calToday` from briefing.json for today's meetings.

**If briefing.json is fresh but calToday is empty or sparse:** fall back to Granola — list today's meetings and use those instead. Flag to Kevin that the calendar fell back to Granola.

### 3. Cross-reference with Granola
Pull today's meetings from Granola. Use this to:
- Confirm meeting durations
- Catch any meetings not showing in calToday
- Resolve any ambiguity (e.g. notes saved today from a previous day's meeting)

### 4. Check Command Centre tasks
Read `begb0037admin/command-centre/data/tasks.json` → Today tier.

If any task maps to a specific funded Clockify project (not BAU), include it in the timesheet. Otherwise tasks stay in gap fill.

### 5. Check phased return target
Current daily target: **4:00** (phased return, 9am–1pm).

Check `calFull` in briefing.json for block-out events — these indicate when phased return hours change week by week. If a change is detected, confirm with Kevin and update KB.

### 6. Calculate BAU
`BAU = daily target minus total meeting duration`

| Situation | Action |
|-----------|--------|
| Meetings total < target | BAU = target minus meetings |
| Meetings total = target | BAU = 0 |
| Meetings total > target | BAU = 0, log meetings only |

### 7. Report back

Present the table and wait. Do not proceed further.

> **Clockify — [Day Date]**
>
> | Project | Task | Duration |
> |---------|------|----------|
> | [meetings...] | | |
> | Focussed time: Email and Teams messages | BAU | X:XX |
> | **Total** | | **4:00** |
>
> ⚠️ *Check what's already logged in Clockify today before entering — adjust BAU accordingly.*

### 8. Handle unknowns
If any meeting in calToday or Granola has no KB mapping:
> "Unknown meeting — [title]. What Clockify project/task?"
Kevin confirms once → add to KB → all future occurrences mapped automatically.

---

## What Kevin Does

1. Open https://app.clockify.me/timesheet
2. Check what's already logged for today
3. Enter/adjust entries to match Claude's table
4. Done

---

## Data Sources

| Source | What it provides | Fallback |
|--------|-----------------|---------|
| `work-inbox/data/briefing.json → calToday` | Today's calendar (Outlook-synced, 6x daily Mon–Fri) | Granola if stale or empty |
| Granola | Meeting detail, duration confirmation | — |
| `command-centre/data/tasks.json` | Today tier tasks — any funded project work | — |
| `clockify/docs/reference/CLOCKIFY_KB.md` | Project/task mappings, daily target | — |

---

## Known Gaps in the Process

| Gap | Impact | Mitigation |
|----|--------|-----------|
| briefing.json not refreshed (machine off) | calToday is stale | Stale check at step 1 — stop and prompt Kevin to run fetch_inbox.py |
| HR Systems Roadmap not always in Granola (no notes taken) | Meeting missed | KB rule: every Friday 1:00 — included by default |
| Clockify pre-existing entries not visible to Claude | BAU may be wrong | Always remind Kevin to check before logging |

---

## Phased Return — Tracking Hours

Daily target changes as Kevin's phased return steps up. Claude tracks via block-out events in `calFull`. Kevin confirms → KB updated immediately.

Current target: **4:00/day**. Full day: **7:15**.

---

## What This Process Replaced

The previous approach (Clockify dashboard + Chrome extension + Approve & Commit button) was abandoned — the Clockify calendar view did not reliably sync Outlook events, and the Chrome extension workflow was not sustainable as a daily habit.
