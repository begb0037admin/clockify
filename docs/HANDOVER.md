# HANDOVER.md
> Last updated: 2026-06-26

## TL;DR
Daily Clockify process established. Claude reads `work-inbox/data/briefing.json → calToday` each morning, maps meetings to Clockify via KB, reports a ready-to-log table. Kevin enters it in the Clockify UI. 60 seconds per day.

## State of Play
- Daily process documented in `docs/DAILY_PROCESS.md`
- `CLOCKIFY_KB.md` updated 2026-06-26: phased return 4:00/day cap, HR Systems Roadmap (Fri 1:00) added
- Phased return active: 9am–1pm = 4:00/day target
- Gap period 4 Jun – 25 Jun: logged as 4:00 BAU per day (phased return, back-filled)
- Previous dashboard/Chrome extension approach abandoned — not sustainable

## Next Concrete Action
Each morning Kevin says "clockify" → Claude reads briefing.json calToday → reports table → Kevin logs in UI.

## Data Sources
- Calendar: `begb0037admin/work-inbox/data/briefing.json` → `calToday`
- Mapping: `docs/reference/CLOCKIFY_KB.md`
- Process: `docs/DAILY_PROCESS.md`

## Watch Out For
- `briefing.json` refreshes 6x daily Mon–Fri (7am/9am/11am/1pm/3pm/5pm). If stale (>24hrs), warn Kevin before using.
- Phased return target changes week by week — track via block-out events in `calFull`. Update KB when it changes.
- Pre-existing entries may already be in Clockify for the current day — always check before logging; adjust BAU accordingly.
- HR Systems Roadmap task name in Clockify not yet confirmed in KB — flagged for Kevin to verify next Friday.

## Open Questions
- OQ-01: Busy blocks Tue 2 Jun still unresolved (low priority — back period already filled)
