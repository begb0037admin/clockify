# AGENT_MODEL.md

> Which seat does what, where the handoffs are, and who is allowed to
> write to disk. Read this when you need to know who should be doing
> what — not what the work is.

This file lives in every project root and in project-os-template/.
It changes rarely. Per-project state lives in STATUS.md and HANDOVER.md.

---

## 1. The Four Seats

### Seat A — Kevin's Chat (Reasoning, Routing, Daily Operations Driver)

- **Where it runs:** Claude.ai chat (Hope or Kevin seat), opened each morning.
- **What it owns:**
  * All reasoning, planning, and routing.
  * Reading Granola via MCP to pull today's meetings.
  * Reading Outlook inbox via Chrome.
  * Building the daily Clockify timesheet plan.
  * Pushing KB updates and HANDOVER files to GitHub via API (PAT from MORNING.md).
  * Generating inbox briefing and pushing to GitHub Pages via API.
  * Issuing Chrome commands to Seat D for Clockify entry logging.
  * Writing COWORK BRIEFs for structural/build work only.
  * Every daily session starts here.
- **What it does not own:**
  * Does not execute browser clicks directly — issues commands to Seat D.
  * Does not make structural code changes to the dashboard — that is Seat C.

---

### Seat B — Kev + VS Code Terminal (Not used in daily ops)

- **Where it runs:** VS Code integrated terminal.
- **What it owns:**
  * Available for one-off script execution if needed.
- **What it does not own:**
  * Not part of the daily Clockify workflow.
  * Not needed unless Seat A specifically dispatches a RUN SCRIPT command.

---

### Seat C — Cowork (Dashboard Builds and Structural Changes)

- **Where it runs:** Cowork, with file tools and bash shell.
- **What it owns:**
  * All structural changes to `index.html` (dashboard builds, feature additions, fixes).
  * Applying COWORK BRIEFs issued by Seat A.
  * Git commits and pushes for code changes.
  * Reporting results back exactly — output verbatim, no editorialising.
- **What it does not own:**
  * Not part of daily operations. Called only for build/fix work.
  * Does not make architectural decisions. Stop and report if something unexpected requires a decision.
  * Does not validate live UI behaviour — that is Seat D.
- **Stop-and-report rule:** If anything unexpected is encountered mid-task, stop immediately, report the exact error, and wait. Do not attempt to solve the problem.
- **Brief format rule:** COWORK BRIEFs contain commands only. No prose lines mixed in.

---

### Seat D — Chrome / Claude in Chrome (Clockify Executor)

- **Where it runs:** Claude in Chrome extension, against https://app.clockify.me/timesheet
- **What it owns:**
  * Executing Clockify timesheet entry clicks on instruction from Seat A.
  * Confirming 07:15 daily total is reached.
  * Reporting exactly what it sees — no interpretation.
- **What it does not own:**
  * No reasoning or planning — executor only.
  * No disk read or write.
  * No terminal, no git, no node.
  * No code edits.

---

## 2. Dispatch Language

Every time Seat A finishes reasoning it ends with one of these —
labelled, ready to act on, no ambiguity about who acts next.

| Signal | Who acts | Used for |
|---|---|---|
| 🔵 RUN SCRIPT | Kev + VS Code | Read-only terminal commands. Run exactly, paste output back. |
| 🟡 COWORK BRIEF | Cowork via Kev | Write to disk, git operations. Commands only, no prose. |
| 🔴 CHROME BRIEF | Chrome via Kev | Browser smoke-test. Numbered checklist, specific expected outputs. |

**Routing rules:**
- Seat A always goes first. No other seat opens without a dispatch
  command.
- One dispatch at a time. Wait for the result before issuing the next.
- If Cowork reports something unexpected, bring it back to Seat A
  before issuing any further briefs.

---

## 3. Handoff Triggers

| From | To | Trigger |
|---|---|---|
| Seat A | Seat B (RUN SCRIPT) | Need to read disk, run a test, check git state |
| Seat A | Seat B (COWORK BRIEF) | Edit is fully designed, exact change known |
| Seat A | Seat B (CHROME BRIEF) | Commit landed, behaviour needs browser verification |
| Seat C | Seat A (via Kev) | Unexpected finding mid-task |
| Seat D | Seat A (via Kev) | Defect needs a decision |
| Seat D | Seat C (via Seat A) | Defect has a mechanical fix |

---

## 4. Cold-Start Order

Every seat, every session, reads in this order:

1. `CLAUDE.md` — project identity, rules, what's in and out of scope
2. `STATUS.md` — current phase and next step
3. `HANDOVER.md` — what the last session did and what's next

That is the entire bootstrap. No fourth file unless HANDOVER.md
specifically directs it. No human recap required if the handover
was written correctly.

**Cowork cold-start exception:** Cowork receives HANDOVER.md only,
plus the COWORK BRIEF. It does not receive CLAUDE.md or STATUS.md —
those invite architectural reasoning Cowork should not be doing.

**Chrome cold-start exception:** Chrome receives the CHROME BRIEF
only. No project docs.

---

## 5. Rollover and End-of-Session Discipline

**Trigger:** roll at ~70% context. Don't wait for the cap.

**Before any session closes:**

1. Stop new work.
2. Replace HANDOVER.md — never append. Write: TL;DR, state of play,
   next concrete action, watch-outs.
3. Bump STATUS.md — only the lines that changed.
4. Promote in-flight decisions to ADRs.
5. Commit everything.

Chat history is disposable. The docs are the memory.
A HANDOVER.md that grows session over session means durable knowledge
isn't being promoted. Keep it small.

---

## 6. Disk-Write Authority

**Cowork is the only seat that writes files to disk.**

No exceptions. If Seat A or Seat D believes a file needs to change,
the output is a handoff to Seat C — not an edit attempt.

---

## 7. Quick Reference

| Seat | Surface | Daily ops? | Role |
|------|---------|------------|------|
| A — Kevin's Chat | Claude.ai chat | ✅ Yes — primary driver | Reasoning, Granola, Outlook, GitHub API writes, Chrome dispatch |
| B — Kev + VS Code | VS Code terminal | ❌ No | Manual script execution only if dispatched |
| C — Cowork | Cowork + bash | ❌ Not daily — build/fix only | Dashboard builds, structural index.html changes |
| D — Chrome | Claude in Chrome | ✅ Yes — executor only | Logs Clockify entries on instruction from Seat A |

---

## Last updated

2026-06-03 — Architecture redesign. Seat A now drives daily ops directly (Granola MCP, Outlook via Chrome, GitHub API). Cowork retired from daily ops — build/fix only. Seat D is executor only.
