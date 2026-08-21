# Clockify Morning Logging Prompt
> Paste this into Claude in Chrome at the start of each working day.
> Claude in Chrome must have the BEGB0037 extension active and be signed into Clockify.

---

Good morning. We are continuing the Clockify project.

**Step 1 — Bootstrap. Fetch and read these four files before doing anything else:**

- https://raw.githubusercontent.com/begb0037admin/clockify/main/CLAUDE.md
- https://raw.githubusercontent.com/begb0037admin/clockify/main/docs/STATUS.md
- https://raw.githubusercontent.com/begb0037admin/clockify/main/docs/HANDOVER.md
- https://raw.githubusercontent.com/begb0037admin/clockify/main/docs/reference/CLOCKIFY_KB.md

Do not proceed until all four are read. Do not ask me to recap — the files are the recap.

---

**Step 2 — Establish today's date.**

State today's date clearly. Confirm it is a working day (Mon–Fri). If it is a weekend or bank holiday, stop and say so.

---

**Step 3 — Open Clockify Calendar view for today.**

Navigate to: https://app.clockify.me/calendar

Switch to Day view. Navigate to today's date. List every event you can see, with:
- Event title
- Start time
- Duration

Do not map anything yet. Just list what you see.

---

**Step 4 — Identify unmapped events.**

Cross-reference the event list against the Calendar Event to Project/Task Mapping table in CLOCKIFY_KB.md.

For each event state:
- ✅ Mapped — project, task, duration
- ❓ Unmapped — pause and ask me before proceeding

Do not guess on unmapped events. Do not proceed past this step until every event is either mapped or explicitly skipped by me.

---

**Step 5 — Build the Timesheet entry plan.**

Present a table:

| Project | Task | Duration |
|---------|------|----------|
| ... | ... | HH:MM |
| Focussed time: Email and Teams messages | BAU | HH:MM (gap fill) |
| **TOTAL** | | **07:15** |

Gap fill = 07:15 minus sum of all meeting durations.
Gap fill is always the last row.
Total must equal exactly 07:15. If it does not, stop and flag it.

Wait for me to confirm the plan before touching the Timesheet.

---

**Step 6 — Log to Timesheet.**

Navigate to: https://app.clockify.me/timesheet

Confirm the correct week is showing.

**If today is Monday:** click Apply on the Weekly Standard template before adding any rows.

For each row in the confirmed plan:
1. Find the matching row if it already exists (from Weekly Standard), or add a new row
2. Task selection: click the arrow next to "N Tasks" to expand inline — do NOT click the task count badge
3. Enter the duration in today's column
4. Confirm the row is saved before moving to the next

Enter the gap fill (Focussed time: BAU) row last.

After all rows are entered, confirm the daily total shown in Clockify equals 07:15. Screenshot or read the total aloud.

---

**Step 7 — Update project docs.**

Make the following updates locally (clone the repo if not already cloned, or edit files in place):

**docs/HANDOVER.md** — replace with a new entry for today:
- TL;DR of what was logged
- State of play (days logged, days remaining this week)
- Next concrete action
- Watch out for (anything unmapped, anything to confirm)

**docs/STATUS.md** — update:
- Move today's date to Completed
- Update Up Next to tomorrow's date
- Update Logged Days Reference in CLOCKIFY_KB.md with today's date, total, and any notes

**docs/reference/CLOCKIFY_KB.md** — update:
- Add today to Logged Days Reference table
- Add any newly confirmed mappings to Calendar Event to Project/Task Mapping table
- Add any newly decoded Busy blocks to Busy Block Decoder table

---

**Step 8 — Push to GitHub.**

Run in the terminal (repo root):

```bash
git add CLAUDE.md docs/STATUS.md docs/HANDOVER.md docs/reference/CLOCKIFY_KB.md
git commit -m "Timesheet logged: [TODAY'S DATE]"
git push origin main
```

Confirm push succeeded. State the commit message used.

---

**Hard rules (always apply):**
- Never attempt Clockify API writes
- Never log more or less than 07:15 without Kevin's explicit instruction
- Always read CLOCKIFY_KB.md before touching the Timesheet
- Always update docs and push at end of session
- Always ask before logging any unmapped or Busy event
