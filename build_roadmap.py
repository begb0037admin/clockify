#!/usr/bin/env python3
"""
build_roadmap.py -- kevin-work-hub aggregator.

Pulls live data from Kevin's work estate (command-centre, work-inbox,
hris-dashboard, hris-change-requests) via the GitHub Contents API and
combines it with structured input supplied directly by Lauren
(meeting-records) and Adam (knowledge base) -- this script does not scrape
either of their domains itself, it only encodes what they hand over.

Output: data/roadmap.json (consumed client-side by index.html/js/app.js).

Run manually for now (`python build_roadmap.py`). Not yet wired into Task
Scheduler -- see HANDOVER.md for that as a next step.
"""
import base64
import json
import subprocess
import sys
from datetime import datetime, timezone

GH_OWNER = "begb0037admin"


def gh_json(repo, path):
    """Fetch and decode a JSON file from a repo via `gh api`, using the
    Contents API + base64 decode (never raw.githubusercontent.com -- no
    cache-buster games needed when going through the API directly)."""
    result = subprocess.run(
        ["gh", "api", f"repos/{GH_OWNER}/{repo}/contents/{path}", "--jq", ".content"],
        capture_output=True, text=True, check=True,
    )
    raw = base64.b64decode(result.stdout.strip())
    return json.loads(raw)


def gh_text(repo, path):
    result = subprocess.run(
        ["gh", "api", f"repos/{GH_OWNER}/{repo}/contents/{path}", "--jq", ".content"],
        capture_output=True, text=True, check=True,
    )
    raw = base64.b64decode(result.stdout.strip())
    return raw.decode("utf-8", errors="replace")


def build_command_centre():
    tasks = gh_json("command-centre", "data/tasks.json")
    tiers = {"today": [], "tomorrow": [], "week": [], "parked": []}
    for t in tasks:
        tier = t.get("tier")
        if tier in tiers:
            tiers[tier].append(t)
    open_counts = {k: sum(1 for t in v if not t.get("done")) for k, v in tiers.items()}
    done_counts = {k: sum(1 for t in v if t.get("done")) for k, v in tiers.items()}
    total_open = sum(open_counts.values())
    total_done = sum(done_counts.values())

    # Surface the "Today" open items by name -- the sharpest-edge tier.
    today_open = [
        {"id": t["id"], "title": t.get("title", ""), "source": t.get("source", "")}
        for t in tiers["today"] if not t.get("done")
    ]

    return {
        "id": "command-centre",
        "label": "Command Centre",
        "status": "ok" if total_open else "attention",
        "source": "begb0037admin/command-centre data/tasks.json (live)",
        "summary": f"{total_open} open tasks across Today/Tomorrow/This Week/Parked ({total_done} done, {len(tasks)} total).",
        "counts": {
            "today_open": open_counts["today"], "today_done": done_counts["today"],
            "tomorrow_open": open_counts["tomorrow"], "tomorrow_done": done_counts["tomorrow"],
            "week_open": open_counts["week"], "week_done": done_counts["week"],
            "parked_open": open_counts["parked"], "parked_done": done_counts["parked"],
        },
        "today_open_items": today_open,
        "link": "https://begb0037admin.github.io/command-centre/",
    }


def build_work_inbox():
    briefing = gh_json("work-inbox", "data/briefing.json")
    suggestions = gh_json("work-inbox", "data/inbox_suggestions.json")

    urgent = briefing.get("urgent", [])
    needs = briefing.get("needs", [])
    fyi_raw = briefing.get("fyiRawCount", len(briefing.get("fyi", [])))
    new_tasks = suggestions.get("new_tasks", [])
    applied = suggestions.get("applied_updates", [])

    status = "attention" if urgent or needs else "ok"

    return {
        "id": "work-inbox",
        "label": "Work Inbox",
        "status": status,
        "source": "begb0037admin/work-inbox data/briefing.json + data/inbox_suggestions.json (live)",
        "summary": (
            f"{len(urgent)} urgent, {len(needs)} needs-reply, {fyi_raw} FYI. "
            f"{len(new_tasks)} new task suggestion(s) not yet actioned in Command Centre."
        ),
        "counts": {
            "urgent": len(urgent), "needs": len(needs), "fyi": fyi_raw,
            "low": len(briefing.get("low", [])),
            "priorities_today": len(briefing.get("prioritiesToday", [])),
            "priorities_week": len(briefing.get("prioritiesWeek", [])),
            "new_suggestions": len(new_tasks),
            "applied_updates": len(applied),
        },
        "urgent_items": [
            {"title": u.get("subject") or u.get("title", ""), "from": u.get("from", "")}
            for u in urgent[:10]
        ],
        "needs_items": [
            {"title": n.get("subject") or n.get("title", ""), "from": n.get("from", "")}
            for n in needs[:10]
        ],
        "new_suggestion_items": [
            {"title": n.get("title", ""), "tier": n.get("tier", "")}
            for n in new_tasks[:10]
        ],
        "briefing_date": briefing.get("date", ""),
        "refreshed_at": briefing.get("refreshed_at", ""),
        "link": "https://begb0037admin.github.io/work-inbox/",
    }


def build_hris():
    tickets = gh_json("hris-dashboard", "data/tickets.json")
    summary = tickets.get("summary", {})

    crs = []
    try:
        cr_files = subprocess.run(
            ["gh", "api", f"repos/{GH_OWNER}/hris-change-requests/contents/CRs", "--jq", ".[].name"],
            capture_output=True, text=True, check=True,
        ).stdout.strip().splitlines()
    except subprocess.CalledProcessError:
        cr_files = []

    for fname in cr_files:
        if not fname.endswith(".md"):
            continue
        text = gh_text("hris-change-requests", f"CRs/{fname}")
        title = ""
        status = "Unknown"
        for line in text.splitlines():
            if line.startswith("# Change Request"):
                title = line.replace("# Change Request —", "").replace("# Change Request -", "").strip(" -—")
            if line.strip().startswith("**Status:**"):
                status = line.split("**Status:**", 1)[1].strip()
        crs.append({"file": fname, "title": title, "status": status})

    open_crs = [c for c in crs if c["status"].lower() not in ("closed", "complete", "completed", "done")]

    status = "attention" if summary.get("stale", 0) or open_crs else "ok"

    return {
        "id": "hris",
        "label": "HRIS (Tickets + Change Requests)",
        "status": status,
        "source": "begb0037admin/hris-dashboard data/tickets.json + begb0037admin/hris-change-requests/CRs (live)",
        "summary": (
            f"{summary.get('total', '?')} open SAASIT tickets ({summary.get('stale', 0)} stale, "
            f"oldest {summary.get('oldest_days', '?')} days). "
            f"{len(open_crs)} change request(s) still in Draft, none finalised."
        ),
        "counts": {
            "tickets_total": summary.get("total"),
            "tickets_unassigned": summary.get("unassigned"),
            "tickets_stale": summary.get("stale"),
            "tickets_oldest_days": summary.get("oldest_days"),
            "change_requests_open": len(open_crs),
            "change_requests_total": len(crs),
        },
        "change_requests": crs,
        "tickets_updated_display": tickets.get("updated_display", ""),
        "link": "https://begb0037admin.github.io/hris-dashboard/",
    }


def build_meetings():
    """Encodes Lauren's 21 Aug 2026 structured meeting-records sweep,
    delivered via SendMessage. This is her curated content, not scraped --
    Drew only structures it for display. Update this block from her next
    sweep rather than re-deriving it from meeting-records directly."""
    return {
        "id": "meetings",
        "label": "Meetings",
        "status": "attention",
        "source": "Lauren sweep, begb0037admin/meeting-records, 21 Aug 2026 (relayed via SendMessage, not live-pulled)",
        "summary": (
            "2 handover areas need attention (HR Systems Roadmap has silently-dropped items; "
            "SK 1-1 has 2 unpushed pending prep items); 7 Roadmap Master items overdue. "
            "Status here is last-known, not live -- see caveat."
        ),
        "caveat": (
            "Much of this is itself stale (some items last touched 1-2 Aug) -- this is the whole "
            "reason the dashboard exists. Treat every line below as “last known status, as of the "
            "date shown,” not current fact."
        ),
        "areas": [
            {
                "name": "HR Systems Roadmap - Handover",
                "status": "open-gaps",
                "note": (
                    "‘Organisational Structure Update — Aug 2026’ (Simon Burford's 3-unit reorg "
                    "proposal) drafted 18 Aug, verified live, never propagated to any brief. "
                    "ORCID-onboarding thread (DTP1092, open since Oct 2024, last touched 27 Feb 2026) "
                    "also silently dropped, untracked in command-centre/work-inbox."
                ),
            },
            {
                "name": "Health and Safety Roadmap - Handover",
                "status": "not-refreshed",
                "note": "Area exists, no content refresh done in this sweep, not cross-referenced tonight.",
            },
            {
                "name": "HR Systems Managers Meeting - Handover",
                "status": "not-refreshed",
                "note": "Area exists, no content refresh done in this sweep.",
            },
            {
                "name": "SK 1-1 - Handover",
                "status": "open-gaps",
                "note": (
                    "Two pending prep items never pushed to the actual brief: P1 org-structure reorg, "
                    "P2 Cority Applicant Data Import file (DOB format fix; ‘who built RECSUP20’ "
                    "question resolved 20 Aug -- Grace, not Lee)."
                ),
            },
            {
                "name": "Team 1-1's (Asta / James / Michael)",
                "status": "unknown",
                "note": "Existing areas, not reviewed in this sweep, status unknown.",
            },
            {
                "name": "KPI Presentation - Handover",
                "status": "unknown",
                "note": (
                    "Last confirmed KPI run: May 2026 (sent 9 Jun, presented 10 Jun). Unconfirmed "
                    "whether June/July runs happened during Kevin's absence. kpi-definitions.md still a stub."
                ),
            },
            {
                "name": "Standing Agenda - Handover",
                "status": "in-progress",
                "note": (
                    "August 2026 deck real/live/approved, 6 slides, actively iterated 2–18 Aug. "
                    "Two newly appended slides (positions 5–6) still awaiting Kevin's confirm on "
                    "final placement."
                ),
            },
            {
                "name": "Meeting Pipeline Review - Handover",
                "status": "meta",
                "note": (
                    "The meta-item this whole dashboard traces back to. Root cause doc: "
                    "tools/speaking-briefs/PIPELINE_RELIABILITY_REVIEW.md (commit a28ac0d) -- every "
                    "brief is a hand-authored snapshot, no persistent registry, no staleness mechanism. "
                    "3 fix options sketched, none built yet."
                ),
            },
        ],
        "overdue": [
            {"id": "136", "title": "PeopleXD DPIA", "note": "Stage 7 sign-off stuck with Marie Cooksey since 3 Jul."},
            {"id": "DTP1334", "title": "H&S Management System", "note": "31 Jul deadline passed, revised date never confirmed."},
            {"id": "DTP1092", "title": "Research management data for REF & research quality", "note": "Refreshed 21 Aug (commit c737180) -- College/PXD workstream now in integration testing; REF-via-ESS sub-thread possibly stale-overdue (UDF actually went live 7 Jul); ORCID sub-thread open since 2024, untracked."},
            {"id": "ITS1004", "title": "WFM Rollout", "note": "GLAM resolution call status unconfirmed."},
            {"id": "179", "title": "SSO Migration", "note": "3 Jul decision-day outcome never recorded."},
            {"id": "174_b", "title": "H&S Dashboards", "note": "Brian's stakeholder comms still not sent as of last check."},
            {"id": "22_c/22_d", "title": "Security Model Review (phase 1 / university-wide)", "note": "On hold, no movement in over a year on 22_d."},
        ],
        "link": None,
    }


def build_knowledge_base():
    """Encodes Adam's 21 Aug 2026 structured knowledge-base sweep, relayed
    via Lauren (his direct SendMessage to Drew failed the same way Lauren's
    initially did). This is his curated content, not scraped -- Drew only
    structures it for display. Update this block from his next sweep."""
    items = [
        {"id": 1, "title": "Cority Salesforce Community scrape (Source 2)", "status": "open", "owner": "Adam",
         "note": "Second Cority H&S source (uc.cority.com); ClickHelp side fully built/indexed, this one still needs authenticated login flow, Coveo article enumeration, Salesforce image-placeholder safety check. Source: CORITY-FEASIBILITY.md §3-5."},
        {"id": 2, "title": "SQL Training Guide (Oracle SQL Developer for HR Systems)", "status": "open/parked", "owner": "Kevin/Adam",
         "note": "Full draft written June 2026, needs Word doc + screenshots + library commit."},
        {"id": 3, "title": "HOW TO: Add a Pay Code to HR Report Suite SQL", "status": "open/parked", "owner": "Kevin/Adam",
         "note": "Draft exists, needs Word doc + screenshots + commit; linked to pay code 121 work."},
        {"id": 4, "title": "HOW TO: Raise an OSM Change Request for HR Reporting", "status": "open/parked", "owner": "Kevin/Adam",
         "note": "Draft exists, needs Word doc + commit."},
        {"id": 5, "title": "Linda cross-session memory + self-learning", "status": "blocked", "owner": "Kevin (decision needed)",
         "note": "Two distinct pieces of work, neither designed; needs scope decision before sizing."},
        {"id": 6, "title": "Access Group/PeopleXD articles missing screenshots", "status": "open (tech debt)", "owner": "Adam",
         "note": "~1,948 web articles text-only, images never captured; fix steps already documented."},
        {"id": 7, "title": "Linda's live Cority Q&A not confirmed end-to-end", "status": "open", "owner": "Kevin (action needed)",
         "note": "Mechanism verified by code read only; needs Kevin's own AI worker credentials for a real test."},
        {"id": 8, "title": "TTS read-aloud cuts off past 2,000 chars", "status": "open", "owner": "Adam",
         "note": "Worker's /tts route truncates; client-side chunking fix scoped but not built."},
        {"id": 9, "title": "Data protection gaps on data/kb.json", "status": "blocked", "owner": "Kevin (action needed)",
         "note": "No branch protection on main, single custodian, no off-GitHub backup."},
        {"id": 10, "title": "pxd.lelitte.co.uk SERVICES section visual approval", "status": "open", "owner": "Kevin (action needed)",
         "note": "Live sidebar change verified byte-for-byte, not yet visually reviewed by Kevin."},
        {"id": 11, "title": "Colleges & Halls Guide -- commit real Word doc", "status": "in-progress", "owner": "Adam",
         "note": "Placeholder .md needs replacing with Kevin's actual .docx."},
        {"id": 12, "title": "Kevin's Guides cleanup", "status": "in-progress", "owner": "Adam",
         "note": "Remove broken JSON-blob pipeline, superseded by library-file approach."},
    ]
    blocked = [i for i in items if i["status"] == "blocked"]
    return {
        "id": "knowledge-base",
        "label": "Knowledge Base",
        "status": "attention" if blocked else "ok",
        "source": "Adam sweep, hr-fa-knowledge-base + knowledge-base-playbook + CORITY-FEASIBILITY.md, 21 Aug 2026 (relayed via Lauren/SendMessage, not live-pulled)",
        "summary": (
            f"{len(items)} open/pending items across the knowledge base. {len(blocked)} blocked on "
            f"Kevin's own decision or action ({', '.join(str(i['id']) for i in blocked)})."
        ),
        "items": items,
        "link": None,
    }


def main():
    pillars = [
        build_meetings(),
        build_work_inbox(),
        build_command_centre(),
        build_knowledge_base(),
        build_hris(),
    ]
    out = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "pillars": pillars,
    }
    with open("data/roadmap.json", "wb") as f:
        f.write(json.dumps(out, indent=2, ensure_ascii=False).encode("utf-8"))
    print(f"Wrote data/roadmap.json ({len(json.dumps(out))} bytes)")


if __name__ == "__main__":
    sys.exit(main())
