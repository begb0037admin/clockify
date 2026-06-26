# CLOCKIFY_KB.md — Clockify Knowledge Base
> Living reference. Read this before every Timesheet task.
> Update this whenever a new mapping is confirmed.
> Last updated: 2026-06-26 (phased return rule added)

---

## Workspace and Auth
| Item | Value |
|------|-------|
| Workspace | HR Systems workspace |
| Workspace ID | 64be71d996d0922209171f18 |
| User ID | 6728e441b3c33e77581a9892 |
| Email | kevin.lelitte@admin.ox.ac.uk |
| Auth method | Microsoft SSO to CAKE.com to Clockify |
| API writes | NOT POSSIBLE — SSO account. Do not re-investigate. |
| Timesheet URL | https://app.clockify.me/timesheet |
| Calendar URL | https://app.clockify.me/calendar |

---

## The Timesheet Process
1. Navigate to https://app.clockify.me/timesheet
2. Confirm correct week is showing
3. If Monday: click Apply on Weekly Standard template
4. Each morning: check yesterday's daily total — adjust "Focussed time" BAU row so the day total = **4:00**
5. If meetings on a day already total 4:00 or more, set Focussed time to 0

Task selection gotcha: Click the arrow next to N Tasks to expand task list inline. Do NOT click the task count badge — that selects project only with no task. Scroll within dropdown to find task, then click task name.

---

## Working Day Rule
| Rule | Value |
|------|-------|
| Target daily total | **4:00** (phased return — 9am–1pm. Confirmed 2026-06-26.) |
| Standard full day | 7:15 (when phased return ends, revert to this) |
| Gap fill project | Focussed time: Email and Teams messages — BAU |
| Gap fill calculation | 4:00 minus sum of all meeting durations |
| If meetings exceed 4:00 | Set BAU to 0, log meetings only |

---

## Weekly Standard Template
Template name in Clockify: Weekly Standard
Apply on Mondays only.

| Row | Project | Task | Typical duration |
|-----|---------|------|-----------------|
| 1 | Focussed time: Email and Teams messages | BAU | Gap fill to 4:00 |
| 2 | Meetings - HR Systems team | Functional Analysts: regular catch-up | 0:15 Mon to Fri |
| 3 | Meetings - HR Systems team | Weekly H&S Roadmap update meeting | 1:00 Mon only |
| 4 | Meetings - HR Systems team | Functional Analysts: one-to-ones | 1:00 when 1-1 occurs |

---

## Confirmed Project and Task Reference

### BAU
| Project | Task | Project ID | Notes |
|---------|------|------------|-------|
| Focussed time: Email and Teams messages | BAU | 64c0e2483c2c4542c2edeb66 | Gap fill. Always last row. |

### Meetings — HR Systems team (Project ID: 699d6c7c667a5341a63a04e1)
| Task | Task ID | Notes |
|------|---------|-------|
| Functional Analysts: regular catch-up | 699d70ea667a5341a63aaffa | Daily 0:15 |
| Weekly H&S Roadmap update meeting | 699f08eca11ae720eecb7c97 | Mon 1:00 |
| Functional Analysts: one-to-ones | 699d71e2afa57c90cad91bbc | When 1-1 occurs |
| HR Systems Management Team meeting | confirmed (verified 2026-06-03) | Fortnightly Wed 1:00 |
| HR Systems Management Team: one-to-ones | confirmed (verified 2026-06-03) | Fortnightly — Simon/Kevin 121 |

### HR Systems Roadmap Updates
| Project | Task | Notes |
|---------|------|-------|
| HR Systems Roadmap updates | (see Clockify row) | Every Friday 1:00. Confirmed 2026-06-26. |

### Funded Projects
| Project | Task | Project ID | Notes |
|---------|------|------------|-------|
| Research management data for REF and research quality [DTP1092] | Meetings and calls | 65bba5b51e975825d3c5539a | College staff in PXD meetings |
| Research management data for REF and research quality [DTP1092] | Multi-Company Set up | 65bba5b51e975825d3c5539a | — |
| Research management data for REF and research quality [DTP1092] | Training - multi company set up | 65bba5b51e975825d3c5539a | — |
| Data Platform Project | Meetings and calls | 699c4163d73ba8168f02d442 | Azure Integration Platform Sprint Review |
| Data Platform Project | Board Prep | 699c4163d73ba8168f02d442 | — |
| Data Platform Project | Project Board | 699c4163d73ba8168f02d442 | — |

### Functional Analyst Team Activities
| Project | Task | Description field | Notes |
|---------|------|-------------------|-------|
| Functional Analyst Team activities | BAU | H&S BAU | H&S-related BAU work. Confirmed 2026-06-03. |
| Functional Analyst Team activities | BAU | PXD - BAU | PXD-related BAU work. Confirmed 2026-06-03. |

### BAU Initiatives
| Project | Task | Project ID | Notes |
|---------|------|------------|-------|
| TSS ePloy integration [119] | No tasks | TBC | Eploy Hold and project run-through meetings |

---

## Calendar Event to Project/Task Mapping
| Calendar event | Project | Task | Duration | Notes |
|---------------|---------|------|----------|-------|
| FA Team Daily Catchup | Meetings - HR Systems team | Functional Analysts: regular catch-up | 0:15 | Every weekday |
| H&S Roadmap | Meetings - HR Systems team | Weekly H&S Roadmap update meeting | 1:00 | Mondays |
| HR Systems Roadmap | HR Systems Roadmap updates | (see Clockify row) | 1:00 | Every Friday 10:00. Confirmed 2026-06-26. |
| 1-1 Session / [Name] 1-1 / James Salas Guillen 1-1 | Meetings - HR Systems team | Functional Analysts: one-to-ones | 0:30 or 1:00 | Check calendar for duration |
| Simon / Kevin 121s / SK 1-1 | Meetings - HR Systems team | HR Systems Management Team: one-to-ones | 1:00 | Fortnightly |
| HR Systems team meeting | Meetings - HR Systems team | HR Systems Management Team meeting | 1:00 | Fortnightly Wed |
| Weekly HR Systems Team meeting (14:00-14:30) | Meetings - HR Systems team | Weekly HR Systems Team meeting | 0:30 | Every Wednesday |
| Check in on URL changes for internal mobility webpages (ad-hoc) | Meetings - HR Systems team | Business Change: regular catch-up | 0:15 | Ad-hoc |
| Azure Integration Platform Sprint Review | Data Platform Project | Meetings and calls | 1:00 | Confirmed 1 Jun 2026 |
| Hold: Eploy project run through | TSS ePloy integration [119] | — | 0:30 | Confirmed 1 Jun 2026 |
| DTP1092 College staff in PXD | Research management data for REF [DTP1092] | Meetings and calls | 0:30 | Confirmed 1 Jun 2026 |
| Keep free | — | — | — | Do not log. Treat as focus time, absorbed into gap fill. |
| Busy — H&S work | Functional Analyst Team activities | BAU | As per duration | Description: "H&S BAU" |
| Busy — PXD work | Functional Analyst Team activities | BAU | As per duration | Description: "PXD - BAU" |
| Busy (unidentified) | — | — | — | Ask Kevin before logging. |

---

## Open Questions
| ID | Question | Raised | Status |
|----|----------|--------|--------|
| OQ-01 | Busy blocks Tue 2 Jun — H&S BAU or PXD - BAU? | 2026-06-03 | Partially resolved — awaiting Kevin confirmation |

---

## Busy Block Decoder
| Date | Time | Duration | Decoded as | Confirmed by |
|------|------|----------|------------|--------------|
| Tue 2 Jun | ~11:00 | 1:00 | Unknown | Pending OQ-01 |
| Tue 2 Jun | ~12:00 | 1:00 | Unknown | Pending OQ-01 |
| Tue 2 Jun | ~15:30 | 1:30 | Unknown | Pending OQ-01 |

---

## Logged Days Reference
| Date | Total | Notes |
|------|-------|-------|
| Mon 1 Jun 2026 | 7:15 | Weekly Standard applied. First day back from medical leave. |
| Tue 2 Jun 2026 | 7:15 | Data Platform, TSS ePloy, DTP1092 rows added manually. |
| Wed 3 Jun 2026 | 7:15 | FA catchup 0:15, HR Sys Mgmt Team 1-2-1 1:00, HR Sys Mgmt Team meeting 1:00, Weekly HR Systems Team meeting 0:30, Business Change regular catch-up 0:15, Focussed time BAU 4:00. |
| Thu 4 Jun — Thu 25 Jun 2026 | 4:00 | Phased return period. BAU gap fill only. |
