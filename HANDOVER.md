# HANDOVER — kevin-work-hub

## 21 Aug 2026 (later same day) — backlog reconciled with the work-inbox/command-centre stability sprint, 32 -> 44 items

Kevin's own work-inbox/command-centre stability sprint (Phases 1-3: scroll-out persistence, drag-and-drop rework, silent-failure toasts, ticks.json race-fix, staleness-clock fix, cross-system done-sync, wrangler-deploy confirmation, duplicate-task-pair merge) finished the same day this backlog was built — reconciled here rather than left stale.

- `wi-03` (scroll-out persistence) updated `open` -> `done` (was already in the backlog from the original sweep; not duplicated).
- 12 new items added: 9 `done` (`wi-05` drag-and-drop rework, `wi-06` silent-failure toasts, `wi-07` newest-first insertion, `cross-04` ticks.json race-fix, `cross-05` staleness-clock shared fix, `cross-06` cross-system done-sync, `cc-03` wrangler-deploy confirmation, `cc-04` duplicate-pair merge) and 3 `open` (`wi-08` header-count cosmetic bug, `wi-09` second-machine Task Scheduler overlap risk, `cc-05` abandoned branches, `cross-07` stale CLAUDE.md files).
- Every commit sha cited was live-checked via `gh api .../commits?path=...` rather than trusted from prior memory at face value — one correction found doing this: `cc`'s staleness-clock fix (`1a79b259`) had actually already been fast-forward-merged to `command-centre` main, not still "staged on branch pending approval" as an earlier same-day memory file said.
- One relayed estimate corrected rather than repeated: "~15 abandoned branches on command-centre" checked live against the branches API — real count is 19 total / 18 non-main.
- `wi-05` (drag-and-drop rework) flagged as work-inbox-only in its own entry: the original finding was framed as spanning both work-inbox and command-centre, but checking command-centre's own `js/app.js` commit history directly found no matching drag-and-drop change there — not asserted as fixed on the command-centre side without evidence.
- `build_roadmap.py` run unmodified against the updated `data/backlog.json` (44 items in, clean run, no unknown-area warnings). Both `data/backlog.json` and `data/roadmap.json` pushed via the Contents API with a race-guard SHA re-check immediately before each push, then byte-diffed against the live files afterward to confirm the push landed exactly as intended.
- Commits: `5663f576` (`data/backlog.json`), `f9476504` (`data/roadmap.json`), both on `main`.
- Full detail in `begb0037admin/drew`'s own memory: `memory/kevin-work-hub-21aug-stability-sprint-reconcile.md`.

**Not done this pass:** no `index.html`/`css`/`js` changes (none needed — the existing chip/card rendering already handles new items without a schema change). Did not delete any of command-centre's stale branches (logged as `cc-05`, a hygiene finding, not swept unprompted).

## 21 Aug 2026 — v2 built (correct data model + tabs + branding), awaiting Kevin's re-review

**Repo history:** originally dispatched as a new `begb0037admin/hr-work-roadmap` repo; nothing was ever pushed there. Redirected mid-build to `kevin-work-hub` (renamed from `clockify`) per Kevin's confirmed decision, relayed by Lauren and verified directly before acting. `hr-work-roadmap` is left empty on GitHub, unresolved, pending a delete-or-leave call.

**v1 (rejected same night):** stacked 5 cards on one page, live-mirrored counts/metrics from command-centre/work-inbox/hris-dashboard, used colour-coded tiles not present elsewhere in the estate. Kevin rejected on sight: layout wrong (should be tabs) and branding deviated from `command-centre/BRANDING.md`. Mid-fix, Lauren relayed a third, deeper correction: the data model itself was wrong — this was never meant to be a live-metrics mirror ("that's of no use to me, I already have that"). It's meant to be a **living cross-estate backlog of things AI agents notice are broken/missing/worth improving while doing other work**, addable by any agent, not a snapshot dashboard.

**v2 (this build) — what's done:**
- **Data model rebuilt.** `data/backlog.json` is now the source of truth — a flat array of curated items (`{id, title, area, type, severity, found_by, found_date, status, recommendation, source}`). `build_roadmap.py` no longer pulls any live JSON from other repos; it only groups `backlog.json` by area and computes pillar status. `add_backlog_item.py` added as a CLI convention any agent can use to append an item.
- **28 real seed items populated**, none invented — every one traces to a genuine finding with a checkable source:
  - Meetings (6): from Lauren's 21 Aug sweep + `PIPELINE_RELIABILITY_REVIEW.md`'s own root-cause finding.
  - Work Inbox (4): the 4 distinct `needs_reply` classifier/scroll-out gaps found across multiple sessions (12/17/18/19 Aug) — **corrected one claim mid-build**: Lauren's relay said the "Kevin isn't the addressee" gap was "not fixed yet"; checked Drew's own memory directly and found it was actually fixed and deployed 20 Aug (commit `c8ab371`) — logged as `status: done` with the real commit, not left wrong.
  - Command Centre (2): tasks marked done without a recorded resolution (live-verified against task `t027`; a second cited example, `t020`, was **not found under that id in live data** — flagged as unconfirmed rather than asserted) + the no-owner-field gap.
  - Knowledge Base (12): Adam's sweep, kept as-is per Lauren's note that this pillar's shape was already right.
  - HRIS (3): 3 CRs stuck permanently in Draft, 6 stale SAASIT tickets with no escalation mechanism, the `SCRIPT_SHA` pinning obligation's silent-lapse risk.
  - Cross-cutting (1): tonight's own `git reset --hard` mid-build incident (recovered, logged as a process-improvement flag on itself).
- **Tabs + branding**, both from the first correction, done in the same pass: sidebar `sb-nav` links copied from command-centre's exact house pattern (`showView()`/`nav-<id>`/`.active`), single visible pillar view at a time, real `images/oxford-crest.jpg` (copied from command-centre's own asset), exact `BRANDING.md` v2.0 sidebar brand block/tokens (340px sidebar, `#002147` navy, `#fff` cards, no colour-coded tiles — status now shown only via small text chips reusing the existing `.badge`/chip token pattern).
- Local Playwright render test across all 6 tabs (Meetings, Command Centre, Cross-cutting screenshotted explicitly; Work Inbox/Knowledge Base/HRIS use the same render path, verified via the JSON output directly) — correct active-tab highlighting, plain white cards, no colour tiles, all confirmed.

**Not yet done:**
- Not yet pushed to `main`/redeployed live — that's the next step in this same session.
- Kevin has not yet seen v2. Same UI approval gate as before applies.
- Only 28 seed items exist. This is meant to grow continuously as any agent notices things — not meant to be exhaustive on day one. Command Centre and HRIS in particular likely have more real findings in Drew's own memory that weren't pulled in this pass (kept tight for time; more can be added any time via `add_backlog_item.py`).
- No automation — everything here is agent-run by design, since curation requires judgement a script can't supply.

**Next action:** push v2 to `main`, redeploy, re-screenshot the live URL, report to Lauren for Kevin's re-review.
