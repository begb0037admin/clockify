# STATUS.md — Clockify

Last updated: 2026-06-26
Current phase: Daily process live — briefing.json → KB → Clockify UI

## Active Process
Daily routine: Claude reads `work-inbox/data/briefing.json → calToday`, maps to Clockify KB, reports table. Kevin logs in UI. See `docs/DAILY_PROCESS.md`.

## Current Rules
- Daily target: **4:00** (phased return, 9am–1pm)
- Gap fill: Focussed time: Email and Teams messages — BAU
- Revert to 7:15 when phased return ends

## Completed
- Clockify API auth investigated — SSO blocker confirmed, closed permanently
- Timesheet UI approach adopted as only method
- Weekly Standard template created in Clockify
- KB populated with all confirmed project/task mappings
- Phased return rule added to KB (2026-06-26)
- HR Systems Roadmap meeting added to KB (Fri 1:00, 2026-06-26)
- Gap period 4 Jun – 25 Jun back-filled (4:00 BAU per day)
- Daily process documented and committed
- Previous dashboard/Chrome approach retired

## Open
- OQ-01: Busy blocks Tue 2 Jun unresolved (low priority)
- HR Systems Roadmap exact Clockify task name to be confirmed by Kevin

## Risks
- briefing.json staleness: always check refreshed_at before using
- Phased return target changes weekly — must update KB when hours step up
