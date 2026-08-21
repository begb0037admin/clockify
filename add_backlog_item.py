#!/usr/bin/env python3
"""
add_backlog_item.py -- append one item to data/backlog.json.

For any agent (Drew, Lauren, Adam, Markey, Matthew) who notices something
broken, missing, or worth improving while doing other work, and wants to add
it to the living cross-estate roadmap without hand-editing JSON. This only
writes the local file -- you still need to commit and push (or hand the
change to Drew) for it to reach the live dashboard.

Usage:
  python add_backlog_item.py \
    --title "needs_reply classifier drops X" \
    --area "Work Inbox" \
    --type bug \
    --severity medium \
    --found-by Lauren \
    --status open \
    --recommendation "Do Y to fix it." \
    --source "lauren/memory/some-file.md"

--area must be one of: Meetings, Work Inbox, Command Centre, Knowledge Base, HRIS, Cross-cutting
--type must be one of: bug, gap, improvement-idea, process-fix
--severity must be one of: low, medium, high
--status must be one of: open, in-progress, done
"""
import argparse
import json
import sys
from datetime import date

AREAS = ["Meetings", "Work Inbox", "Command Centre", "Knowledge Base", "HRIS", "Cross-cutting"]
TYPES = ["bug", "gap", "improvement-idea", "process-fix"]
SEVERITIES = ["low", "medium", "high"]
STATUSES = ["open", "in-progress", "done"]

AREA_PREFIX = {
    "Meetings": "meet", "Work Inbox": "wi", "Command Centre": "cc",
    "Knowledge Base": "kb", "HRIS": "hris", "Cross-cutting": "cross",
}


def next_id(items, area):
    prefix = AREA_PREFIX[area]
    existing = [i["id"] for i in items if i["id"].startswith(prefix + "-")]
    nums = [int(i.split("-")[-1]) for i in existing if i.split("-")[-1].isdigit()]
    n = max(nums, default=0) + 1
    return f"{prefix}-{n:02d}"


def main():
    p = argparse.ArgumentParser(description="Append one item to the kevin-work-hub backlog.")
    p.add_argument("--title", required=True)
    p.add_argument("--area", required=True, choices=AREAS)
    p.add_argument("--type", required=True, choices=TYPES)
    p.add_argument("--severity", required=True, choices=SEVERITIES)
    p.add_argument("--found-by", required=True)
    p.add_argument("--status", default="open", choices=STATUSES)
    p.add_argument("--recommendation", default="")
    p.add_argument("--source", required=True, help="Where this was found -- a commit, a memory file, a conversation.")
    p.add_argument("--found-date", default=str(date.today()))
    args = p.parse_args()

    with open("data/backlog.json", "rb") as f:
        data = json.load(f)

    item = {
        "id": next_id(data["items"], args.area),
        "title": args.title,
        "area": args.area,
        "type": args.type,
        "severity": args.severity,
        "found_by": args.found_by,
        "found_date": args.found_date,
        "status": args.status,
        "recommendation": args.recommendation,
        "source": args.source,
    }
    data["items"].append(item)

    with open("data/backlog.json", "wb") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    print(f"Added {item['id']}: {item['title']}")
    print("Now run: python build_roadmap.py   (then commit + push both files)")


if __name__ == "__main__":
    sys.exit(main())
