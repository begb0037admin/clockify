// kevin-work-hub -- client-side renderer.
// Reads data/roadmap.json (produced by build_roadmap.py) and renders the
// overview strip + per-pillar detail cards. No writes happen from this page
// -- this is a read-only consolidated view, unlike command-centre's board.

const DATA_URL = 'data/roadmap.json';

function esc(s) {
  if (s === null || s === undefined) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function statusLabel(status) {
  switch (status) {
    case 'ok': return 'On track';
    case 'attention': return 'Needs attention';
    case 'pending': return 'Pending input';
    default: return status || 'Unknown';
  }
}

async function loadData() {
  const res = await fetch(`${DATA_URL}?v=${Date.now()}`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Failed to load ${DATA_URL}: ${res.status}`);
  return res.json();
}

function renderNav(pillars) {
  const nav = document.getElementById('pillarNav');
  nav.innerHTML = pillars.map(p => `
    <a href="#pillar-${esc(p.id)}">
      <span>${esc(p.label)}</span>
      <span class="nav-dot" style="background:${dotColor(p.status)}"></span>
    </a>
  `).join('');
}

function dotColor(status) {
  if (status === 'ok') return '#16a34a';
  if (status === 'attention') return '#f59e0b';
  return '#94a3b8';
}

function renderOverview(pillars) {
  const grid = document.getElementById('overviewGrid');
  grid.innerHTML = pillars.map(p => `
    <a class="overview-card status-${esc(p.status)}" href="#pillar-${esc(p.id)}">
      <div class="label">${esc(p.label)}</div>
      <div class="status-badge">${esc(statusLabel(p.status))}</div>
    </a>
  `).join('');
}

function renderCountRow(counts) {
  if (!counts) return '';
  const entries = Object.entries(counts).filter(([, v]) => v !== undefined && v !== null);
  if (!entries.length) return '';
  return `<div class="count-row">${entries.map(([k, v]) => `
    <div class="count-chip"><b>${esc(v)}</b>${esc(k.replace(/_/g, ' '))}</div>
  `).join('')}</div>`;
}

function renderItemList(items, opts = {}) {
  if (!items || !items.length) return `<p class="empty-note">${esc(opts.emptyText || 'Nothing to show.')}</p>`;
  return `<div class="item-list">${items.map(i => {
    const title = i.title || i.name || '(untitled)';
    const noteParts = [];
    if (i.from) noteParts.push(`From ${i.from}`);
    if (i.owner) noteParts.push(`Owner: ${i.owner}`);
    if (i.status && !opts.hideStatusInNote) noteParts.push(i.status);
    if (i.note) noteParts.push(i.note);
    if (i.file) noteParts.push(i.file);
    const cls = ['item-row'];
    if (opts.overdue) cls.push('overdue');
    if (i.status === 'blocked') cls.push('blocked');
    return `<div class="${cls.join(' ')}">
      <div class="item-title">${esc(i.id !== undefined ? i.id + ' — ' : '')}${esc(title)}${i.status ? `<span class="status-tag">${esc(i.status)}</span>` : ''}</div>
      ${noteParts.length ? `<div class="item-note">${esc(noteParts.join(' — '))}</div>` : ''}
    </div>`;
  }).join('')}</div>`;
}

function renderPillar(p) {
  let body = '';

  if (p.caveat) {
    body += `<div class="pillar-caveat">${esc(p.caveat)}</div>`;
  }

  body += renderCountRow(p.counts);

  if (p.areas && p.areas.length) {
    body += `<div class="section-label">Handover areas</div>`;
    body += renderItemList(p.areas);
  }

  if (p.overdue && p.overdue.length) {
    body += `<div class="section-label">Overdue Roadmap Master items</div>`;
    body += renderItemList(p.overdue, { overdue: true });
  }

  if (p.items && p.items.length) {
    body += `<div class="section-label">Open items</div>`;
    body += renderItemList(p.items);
  }

  if (p.urgent_items && p.urgent_items.length) {
    body += `<div class="section-label">Urgent</div>`;
    body += renderItemList(p.urgent_items);
  }

  if (p.needs_items && p.needs_items.length) {
    body += `<div class="section-label">Needs reply</div>`;
    body += renderItemList(p.needs_items);
  }

  if (p.new_suggestion_items && p.new_suggestion_items.length) {
    body += `<div class="section-label">New task suggestions (not yet in Command Centre)</div>`;
    body += renderItemList(p.new_suggestion_items);
  }

  if (p.today_open_items && p.today_open_items.length) {
    body += `<div class="section-label">Today (open)</div>`;
    body += renderItemList(p.today_open_items);
  }

  if (p.change_requests && p.change_requests.length) {
    body += `<div class="section-label">Change requests</div>`;
    body += renderItemList(p.change_requests);
  }

  return `
    <section class="pillar-card" id="pillar-${esc(p.id)}">
      <div class="pillar-head">
        <h2>${esc(p.label)}</h2>
        <span class="pill status-${esc(p.status)}">${esc(statusLabel(p.status))}</span>
      </div>
      <p class="pillar-source">${esc(p.source || '')}</p>
      <p class="pillar-summary">${esc(p.summary || '')}</p>
      ${body}
      ${p.link ? `<a class="pillar-link" href="${esc(p.link)}" target="_blank" rel="noopener">Open live source →</a>` : ''}
    </section>
  `;
}

function renderPillars(pillars) {
  document.getElementById('pillars').innerHTML = pillars.map(renderPillar).join('');
}

async function init() {
  try {
    const data = await loadData();
    document.getElementById('generatedAt').textContent = `Generated ${data.generated_at}`;
    renderNav(data.pillars);
    renderOverview(data.pillars);
    renderPillars(data.pillars);
  } catch (err) {
    document.getElementById('pillars').innerHTML = `<p class="empty-note">Failed to load roadmap data: ${esc(err.message)}</p>`;
  }
}

document.getElementById('refreshLink')?.addEventListener('click', (e) => {
  e.preventDefault();
  location.reload();
});

init();
