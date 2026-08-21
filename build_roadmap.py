#!/usr/bin/env python3
"""
build_roadmap.py -- kevin-work-hub aggregator (v2, curated-backlog model).

v1 mirrored live counts/metrics from command-centre, work-inbox and
hris-dashboard. Kevin rejected that: those numbers are already visible in
each system's own dashboard ("that's of no use to me, I already have that").
What he actually wants is a living backlog of things AI agents have noticed
are broken, missing, or worth improving while doing other work -- bugs,
gaps, improvement ideas, process fixes -- not a snapshot of current-state
metrics.

This script no longer pulls live task/ticket counts. It reads the single
curated source of truth, data/backlog.json, groups items by area, and
writes data/roadmap.json for the dashboard to render (one tab per area).

data/backlog.json is meant to be appended to by ANY agent (Drew, Lauren,
Adam, Markey, Matthew) as they notice things during other work -- see
add_backlog_item.py for the convention, or just append an object matching
the same shape directly and push.
"""
import json
import sys
from datetime import datetime, timezone

AREAS = ["Meetings", "Work Inbox", "Command Centre", "Knowledge Base", "HRIS", "Cross-cutting"]
AREA_ID = {
    "Meetings": "meetings",
    "Work Inbox": "work-inbox",
    "Command Centre": "command-centre",
    "Knowledge Base": "knowledge-base",
    "HRIS": "hris",
    "Cross-cutting": "cross-cutting",
}
AREA_LINK = {
    "Work Inbox": "https://begb0037admin.github.io/work-inbox/",
    "Command Centre": "https://begb0037admin.github.io/command-centre/",
    "HRIS": "https://begb0037admin.github.io/hris-dashboard/",
    "Knowledge Base": "https://begb0037admin.github.io/hr-fa-knowledge-base/",
}


def load_backlog():
    with open("data/backlog.json", "rb") as f:
        data = json.load(f)
    return data["items"]


def pillar_status(items):
    """attention if any open item is high severity or there are open items
    at all past a small threshold; ok if everything is done; pending if the
    area has no items yet."""
    if not items:
        return "pending"
    open_items = [i for i in items if i.get("status") != "done"]
    if not open_items:
        return "ok"
    if any(i.get("severity") == "high" for i in open_items):
        return "attention"
    if len(open_items) >= 2:
        return "attention"
    return "ok"


def build_pillar(area, items):
    open_items = [i for i in items if i.get("status") != "done"]
    done_items = [i for i in items if i.get("status") == "done"]
    status = pillar_status(items)

    by_type = {}
    for i in open_items:
        by_type[i.get("type", "other")] = by_type.get(i.get("type", "other"), 0) + 1
    type_summary = ", ".join(f"{v} {k}" for k, v in sorted(by_type.items()))

    if items:
        summary = f"{len(open_items)} open backlog item(s) ({type_summary})." if open_items else "All known backlog items resolved."
        if done_items:
            summary += f" {len(done_items)} resolved."
    else:
        summary = "No backlog items logged yet for this area."

    return {
        "id": AREA_ID[area],
        "label": area,
        "status": status,
        "source": "Curated cross-agent backlog (data/backlog.json) -- not a live metrics mirror",
        "summary": summary,
        "backlog": sorted(items, key=lambda i: (i.get("status") == "done", {"high": 0, "medium": 1, "low": 2}.get(i.get("severity"), 3))),
        "link": AREA_LINK.get(area),
    }


def main():
    items = load_backlog()
    by_area = {a: [] for a in AREAS}
    unknown_area_items = []
    for i in items:
        a = i.get("area")
        if a in by_area:
            by_area[a].append(i)
        else:
            unknown_area_items.append(i)

    if unknown_area_items:
        print(f"WARNING: {len(unknown_area_items)} backlog item(s) have an area not in {AREAS}, skipped: "
              f"{[i.get('id') for i in unknown_area_items]}", file=sys.stderr)

    pillars = [build_pillar(a, by_area[a]) for a in AREAS]

    out = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "model": "curated-backlog-v2",
        "pillars": pillars,
    }
    with open("data/roadmap.json", "wb") as f:
        f.write(json.dumps(out, indent=2, ensure_ascii=False).encode("utf-8"))
    print(f"Wrote data/roadmap.json ({len(json.dumps(out))} bytes) from {len(items)} backlog items")


if __name__ == "__main__":
    sys.exit(main())
