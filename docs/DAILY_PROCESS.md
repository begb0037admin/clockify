# DAILY_PROCESS.md — Clockify Daily Timesheet Routine
> Established: 2026-06-26
> Owner: Kevin Lelitte

---

## The One-Line Summary
Each morning, Claude reads Kevin's calendar from `work-inbox/data/briefing.json`, maps meetings to Clockify, and reports back a ready-to-log timesheet. Kevin logs it in the Clockify UI. Done in under 60 seconds.

---

## Trigger
Kevin says: "clockify" (or any variation — "do my clockify", "timesheet", etc.)

---

## What Claude Does (in order)

1. **Read calendar** — fetch `begb0037admin/work-inbox/data/briefing.json` → read `calToday`
2. **Check phased return target** — read current daily hour target from `CLOCKIFY_KB.md` (currently 4:00)
3. **Map meetings** — cross-reference each calendar event against the mapping table in `CLOCKIFY_KB.md`
4. **Calculate BAU** — target minus sum of mapped meeting durations
5. **Report back** — present a clean table: Project | Task | Duration. Show daily total = target.
6. **Wait for Kevin to confirm** — do not log anything; Kevin logs via Clockify UI
7. **Update KB** — if any new meeting type appears, ask Kevin for the Clockify mapping and add it to `CLOCKIFY_KB.md`

---

## What Kevin Does

1. Open https://app.clockify.me/timesheet
2. Check the table Claude provided
3. Enter/adjust the "Focussed time: Email and Teams messages — BAU" row to match the gap fill number
4. Done

---

## Data Sources

| Source | What it provides |
|--------|-----------------|
| `begb0037admin/work-inbox/data/briefing.json` → `calToday` | Today's calendar events (Outlook-synced, updated 6x daily Mon–Fri) |
| `begb0037admin/clockify/docs/reference/CLOCKIFY_KB.md` | Project/task mappings, current daily target |
| Granola | Meeting detail and duration if needed for context |

---

## Current Daily Target

**4:00** — phased return (9am–1pm). Confirmed 2026-06-26.

When phased return ends, revert to **7:15**. Update `CLOCKIFY_KB.md` Working Day Rule when this changes.

Kevin's calendar shows block-out events at end of day indicating phased return hours each week. Claude reads these from `calFull` in `briefing.json` to track when the target steps up.

---

## Gap Fill Rule

| Situation | Action |
|-----------|--------|
| Meetings total < target | BAU = target minus meetings total |
| Meetings total = target | BAU = 0 |
| Meetings total > target | BAU = 0, log meetings only |

---

## When a New Meeting Type Appears

1. Claude flags it: "Unknown meeting — [title]. What Clockify project/task?"
2. Kevin confirms once
3. Claude adds to `CLOCKIFY_KB.md` Calendar Event Mapping table
4. All future occurrences mapped automatically

---

## Phased Return — Tracking Hours

The daily target changes as Kevin's phased return steps up week by week. Claude tracks this by:
- Reading block-out events in `briefing.json → calFull`
- Kevin confirming when the target changes
- Claude updating `CLOCKIFY_KB.md` Working Day Rule immediately

---

## What This Process Replaced

The previous approach (Clockify dashboard + Chrome extension + Approve & Commit button) was abandoned — the Clockify calendar view did not reliably sync Outlook events, and the Chrome extension workflow was not sustainable as a daily habit.
