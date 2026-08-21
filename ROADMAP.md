# ROADMAP — kevin-work-hub

## v2 (done, 21 Aug 2026)
Curated cross-agent backlog, correct data model, one tab per area, strict BRANDING.md compliance. See CLAUDE.md "Data model" section before touching this repo again — the v1 mistake (live-metrics mirror) is an easy one to repeat if this isn't read first.

## Not yet built
1. **Backlog growth.** Only 28 seed items exist as of 21 Aug. This should grow continuously as any agent notices something during other work — Command Centre and HRIS in particular are likely under-populated relative to what Drew's own memory already documents. Not a one-time job; revisit periodically.
2. **A lighter-weight add path.** `add_backlog_item.py` is a CLI script requiring repo access. Consider whether a simpler convention (e.g. any agent's own memory file gets picked up automatically, or a shared `agent-commons` inbox) would lower the friction to actually logging something in the moment, per Kevin's stated mechanism ("as we're working along... that goes on this roadmap").
3. **Resolution tracking.** `status: done` items currently stay in the backlog forever (shown, just deprioritised in sort order). Worth deciding whether done items should eventually archive out, or whether keeping a visible resolved history is itself useful (arguably yes, given Kevin's own "what's been fixed" question is adjacent to "what's still broken").
4. **Duplicate/overlap detection.** Nothing currently stops the same finding being logged twice by two different agents. Not urgent at 28 items; will matter more as the backlog grows.
5. **AI Chat Panel parity** — noted on work-inbox/command-centre's own roadmaps as a post-migration Phase 1 item. Given this dashboard is now explicitly a curated backlog rather than a live view, it's not obviously the right fit here — revisit only if Kevin asks.

## Explicitly out of scope for Drew
- Deciding what counts as "worth fixing" in another domain — Lauren/Adam/etc. can add and prioritise their own area's items; Drew's role is the schema/pipeline/display, not editorial judgement over other agents' domains.
- Writing back to any source repo from this dashboard. This is read-only by design.
- Auto-generating backlog items from live data. The whole point of v2 is that entries are judgement calls made by an agent noticing something, not a mechanical query.
