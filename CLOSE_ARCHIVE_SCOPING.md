# Close/Archive write path for kevin-work-hub — scoping only, 21 Aug 2026

**Status: scoping only. Nothing in this document has been built. Kevin needs to review and explicitly approve an option (or a variant) before any implementation, deploy, or code change happens.**

## The ask

Kevin wants to close/archive backlog items directly from the live dashboard (https://begb0037admin.github.io/kevin-work-hub/) instead of the current flow — an agent hand-edits `data/backlog.json`'s `status` field, runs `build_roadmap.py`, and pushes. He was told the honest tradeoff up front: a static public GitHub Pages site cannot safely hold a GitHub write token client-side (anyone with the page URL could pull it straight out of the page source or dev tools and use it to write to the repo directly). He chose "scope it properly" over leaving the manual-agent-edit flow in place.

## What already exists elsewhere in the estate (checked before proposing anything new)

`kevin-work-hub` is not the first static Pages site in this estate that needed to write back to a private GitHub repo. `command-centre` and `work-inbox` solved exactly this problem already, live, via a shared Cloudflare Worker — this is the pattern to reuse, not reinvent.

**`cc-tasks-writer` (Cloudflare Worker, `cc-tasks-writer.kevinlelitte.workers.dev`)**
- Holds a GitHub PAT server-side as a Worker secret (`HRIS_GITHUB_PAT`), never exposed to the browser. The client (`command-centre/js/api.js`) POSTs plain JSON to the Worker; the Worker does the authenticated GitHub Contents API read-sha/write round trip itself.
- Writes to **two** repos from one Worker (`command-centre` and `work-inbox` — `OWNER`/`CC_REPO`/`WI_REPO` constants in the source), so there's direct precedent for one small Worker serving more than one repo's write path.
- As of 16 Aug 2026, this secret's GitHub identity was deliberately isolated: rotated off the shared `begb0037admin` PAT (which shares a 5,000/hr budget with every other live automation in the estate — this is what took down `kevin-finance-ai` the same day) onto a dedicated `kevinlelitteadmin` fine-grained token, confirmed live via distinct `committer_login`/`author_email` on real test commits (`drew/memory/cc-tasks-writer-pat-rotation-complete-16aug.md`). This blast-radius-isolation principle is directly relevant to option choice below.
- Handles the write-conflict problem properly: reads the file's current blob `sha` immediately before writing and uses GitHub's optimistic-concurrency check, with a client-side base-sha capture + merge-on-conflict path layered on top (`command-centre/js/api.js` `refreshTasksBaseSha`/`mergeRemote`). Worth reusing rather than re-solving — closing/archiving a backlog item has the same "two agents touch the file around the same time" risk `tasks.json` already had.
- **Important finding, checked directly in the live source, not assumed:** the Worker's only access control is a CORS `Access-Control-Allow-Origin` allow-list (`CORS_ORIGINS` = `cc.lelitte.co.uk`, `wi.lelitte.co.uk`, `begb0037admin.github.io`, the Worker's own workers.dev domain). **This is not real authentication.** CORS is enforced by browsers, not by the server — anyone who has the Worker's URL (which is necessarily public, since it's called directly from public client-side JS on a public Pages site) can bypass it entirely with `curl`/Postman and write to the repo with no further check. This is a known, already-accepted weakness in the *existing, live, Kevin-approved* pattern — not something new I'm flagging as a blocker, but it's worth being explicit that "reuse the existing pattern as-is" inherits this gap rather than closing it.

**`hris-dashboard`** — different shape, not directly reusable here. Its "write path" is either a GitHub Actions self-hosted runner doing an authenticated Playwright scrape, or a manual `.bat` on Kevin's own machine pulling a commit-pinned script and pushing with his own local `gh`/git credentials. Neither involves a public page taking arbitrary write requests from anyone who loads it, so there's no auth pattern here to borrow — the whole point of that pipeline is that only Kevin's own machine or a controlled runner ever writes.

**`ai-log-endpoint.js`** (also in `command-centre/cloudflare-worker/`) is a separate, smaller Worker — a one-way logging sink, not a data-mutation write path. Not relevant as precedent beyond confirming "one small single-purpose Worker per concern" is already the house style rather than one monolith.

## Options

### Option A — New Worker, clone cc-tasks-writer's pattern exactly (CORS-only)
A new small Cloudflare Worker (e.g. `kevin-work-hub-writer`) holding its own GitHub token, exposing one POST route that takes `{id, action}` (`close`/`archive`/reopen), reads `data/backlog.json`'s current sha, flips that one item's `status`, writes back, returns the same `{ok, merged, attempts}` shape `cc-tasks-writer` already returns. Frontend gets a small button per card wired the same way `command-centre/js/api.js` already does its writes.
- **Effort:** Low–medium (roughly half a day). This is almost a line-for-line port of already-proven, already-live code — low risk of new categories of bug.
- **Security:** Inherits the CORS-only gap described above as-is. Low real-world stakes here (worst case: someone who finds the Worker URL flips a backlog item's status — fully recoverable from git history, no financial/PII exposure), but it would be building a second instance of a gap that's already flagged rather than fixing it once.

### Option B — New Worker, cc-tasks-writer pattern + a lightweight shared secret (recommended)
Same as A, plus one cheap addition: the Worker requires a shared-secret header (`x-hub-key` or similar) on the write request, checked server-side before touching GitHub, in addition to the existing CORS allow-list. Kevin sets the passphrase once; the frontend prompts for it once (browser prompt or a stored value) and attaches it to future write calls. Not real user-identity auth — no login, no per-user audit trail — but it closes the actual gap (a bare URL alone, found or guessed, is no longer sufficient to write) for a very small increment of effort.
- **Effort:** Low–medium, marginally above A (a few extra lines in the Worker, a small prompt/storage bit in the frontend).
- **Security:** Meaningfully better than A for the cost. Proportionate to what's actually being protected — a personal backlog list, not financial data — while not just copying forward a known weakness uncritically.
- **Token isolation:** would use its own fine-grained PAT scoped only to `kevin-work-hub`, separate from `cc-tasks-writer`'s `HRIS_GITHUB_PAT` — smaller blast radius per repo, consistent with the isolation principle Kevin already approved and had built 16 Aug for exactly this reason (a compromised or leaked secret here can't touch `command-centre`/`work-inbox` data, and vice versa).

**Open judgment call, not decided here:** a new dedicated Worker (as sketched above) vs. adding a third repo route directly onto the existing `cc-tasks-writer` Worker. The dedicated-Worker route keeps kevin-work-hub's low-stakes writes on their own secret and their own deploy/rotation lifecycle, separate from command-centre/work-inbox's higher-stakes task data — consistent with the isolation work already done. Extending the existing Worker avoids standing up a second Worker/deploy pattern but re-concentrates scope into an already multi-repo secret. I'd lean toward the dedicated Worker, but this is genuinely Kevin's call to weigh in on, not a default I should silently pick.

### Option C — Full authentication (GitHub OAuth device flow, or Cloudflare Access in front of the write route)
A real login step — either Cloudflare Access gating the Worker route behind Kevin's own identity, or a GitHub OAuth device-code flow so the write is attributed to an actual logged-in user, not a shared secret.
- **Effort:** High. New infra, new failure modes (token refresh, session expiry, redirect handling on a static Pages site with no server-side session store), disproportionate build time for a personal single-user tool.
- **Security:** Strongest of the three, but arguably overkill given what's actually being protected — reversible status flags on a personal to-do backlog, not financial transactions or PII. Would make sense if this dashboard ever became multi-user or held sensitive data; it doesn't today.

## Recommendation

**Option B** — a small dedicated Worker, cloned from the proven `cc-tasks-writer` pattern (same sha-check/merge-on-conflict logic, same response shape, same "one Worker, one concern" house style), with its own isolated fine-grained PAT scoped to `kevin-work-hub` only, plus a lightweight shared-secret header to close the one real gap in the pattern being reused rather than copying it forward silently. This keeps effort low by reusing already-live, already-debugged code almost verbatim, while not shipping a second known-weak endpoint into the estate when the fix is cheap.

If Kevin decides the CORS-only posture is fine given the low stakes (git history is a full undo button either way), Option A is a strictly smaller version of the same build and easy to fall back to.

## What this does NOT cover (needs Kevin's input before implementation)

- Exact wording/placement of the close/archive UI on each backlog card (button vs. swipe vs. menu) — a UI decision, not an engineering one.
- Whether "archive" should be a distinct status from "closed"/"done", or whether archived items disappear from the default view vs. stay visible with a chip — same `_readme`/schema question `add_backlog_item.py`'s conventions already touch on.
- Whether reopening a closed item should be possible from the UI too, or agent-only.
- Per command-centre's own standing rule, any UI/visual change here needs a screenshot and Kevin's literal "approved" before going live — same gate `kevin-work-hub` v1 and v2 already went through this same night.

## On the disputed "hold all further changes" instruction

Flagged in the dispatch as something to check. Verified directly against Drew's own memory (`drew/memory/meeting-records-pipeline-reliability-scoping-21aug.md`, written the same night): that instruction was Kevin's explicit "no further ad hoc content changes to the Roadmap pipeline until he and Lauren have a dedicated review session" — scoped specifically to `meeting-records`' `build_roadmap.py`/`build_sk_1on1.py`/`brief_chrome.py` speaking-briefs pipeline (the meeting-prep content generator), not to `kevin-work-hub`. Nothing in that memory entry, or in anything checked for this scoping pass, extends it to kevin-work-hub. This scoping doc does not conflict with that hold, and no code has been changed here regardless.

## Next step

Kevin reviews this doc and picks A, B, C, or a variant. Once he does, implementation follows command-centre's own mandatory backup-and-verify sequence for the actual `data/backlog.json` write path, and the UI approval gate for anything visible on the page, before anything goes live.
