# ROADMAP — kevin-work-hub

## v1 (done, 21 Aug 2026)
Read-only consolidated dashboard, one pillar per source area, manually-run aggregator, GitHub Pages hosting.

## Not yet built
1. **Automation.** `build_roadmap.py` is hand-run. Once Kevin approves the v1 shape, wire it to a schedule (Task Scheduler, matching work-inbox/hris-dashboard's pattern) so `data/roadmap.json` refreshes without a session having to run it.
2. **Meetings/KB live refresh path.** These two pillars are currently point-in-time encodings of a single SendMessage sweep each. Needs a repeatable convention — e.g. Lauren/Adam drop a small structured JSON/YAML file into their own repos on a cadence, and `build_roadmap.py` reads that file instead of a one-off hand-transcription. Avoids re-encoding prose by hand every refresh.
3. **Drill-through links.** Overview cards currently jump to the in-page pillar section. Consider deep-linking specific items (e.g. a command-centre task ID) to that item's actual location in the source dashboard, the way work-inbox's calendar already deep-links to command-centre tasks.
4. **Staleness indicators per pillar**, not just a global "generated at" timestamp — some sources (meetings) are inherently sparser-refreshed than others (work-inbox, which updates ~6x/day). A single per-item "last touched" date, where the source provides one, would make the "last known, not current" caveat concrete rather than a blanket disclaimer.
5. **AI Chat Panel parity** — work-inbox and command-centre both have this on their own roadmaps as a post-migration Phase 1 item. Once built there, consider whether this dashboard wants the same entry point, or whether it should stay a pure aggregation view.

## Explicitly out of scope for Drew
- Curating what counts as "done" in any source pillar — that's each domain owner's call (Lauren for meetings, Adam for KB, Kevin for command-centre/work-inbox priorities).
- Writing back to any source repo from this dashboard. This is read-only by design.
