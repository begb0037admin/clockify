// kevin-work-hub -- client-side renderer.
// Reads data/roadmap.json (produced by build_roadmap.py) and renders one
// tab per pillar (sidebar nav + single visible main view), mirroring
// command-centre's showView()/nav-<id>/.active pattern exactly rather than
// stacking everything on one page. No writes happen from this page -- this
// is a read-only consolidated view, unlike command-centre's task board.

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

function badgeClass(status) {
  if (status === 'ok') return 'badge-ok';
  if (status === 'attention') return 'badge-gold';
  return 'badge-pending';
}

function dotClass(status) {
  if (status === 'ok') return 'dot-ok';
  if (status === 'attention') return 'dot-attention';
  return 'dot-pending';
}

async function loadData() {
  const res = await fetch(`${DATA_URL}?v=${Date.now()}`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Failed to load ${DATA_URL}: ${res.status}`);
  return res.json();
}

/* NAV -- one tab per pillar, house sb-nav pattern */
function renderNav(pillars) {
  const nav = document.getElementById('pillarNav');
  nav.innerHTML = pillars.map(p => `
    <a id="nav-${esc(p.id)}" onclick="showView('${esc(p.id)}')">
      <span>${esc(p.label)}</span>
      <span class="nav-count">${esc(p.open_count ?? '')}</span>
      <span class="nav-status-dot ${dotClass(p.status)}"></span>
    </a>
  `).join('');
}

function itemStatusChipClass(status) {
  if (status === 'done') return 'source-chip chip-done';
  if (status === 'in-progress') return 'source-chip chip-progress';
  return 'source-chip chip-open';
}

function severityChipClass(sev) {
  if (sev === 'high') return 'source-chip chip-high';
  if (sev === 'medium') return 'source-chip chip-medium';
  return 'source-chip chip-low';
}

/* Renders one backlog item: title, type/severity/status chips, recommendation, source. */
function renderBacklog(items) {
  if (!items || !items.length) return `<p class="empty-note">No backlog items logged yet for this area.</p>`;
  return `<div class="item-list">${items.map(i => {
    const chips = [
      `<span class="source-chip">${esc(i.type || '')}</span>`,
      `<span class="${severityChipClass(i.severity)}">${esc(i.severity || '')}</span>`,
      `<span class="${itemStatusChipClass(i.status)}">${esc(i.status || '')}</span>`,
    ].join(' ');
    const metaParts = [];
    if (i.found_by) metaParts.push(`Found by ${i.found_by}`);
    if (i.found_date) metaParts.push(i.found_date);
    return `<div class="item-row">
      <div class="item-title">${esc(i.id ? i.id + ' — ' : '')}${esc(i.title || '(untitled)')}</div>
      <div class="item-chips">${chips}</div>
      ${metaParts.length ? `<div class="item-note">${esc(metaParts.join(' · '))}</div>` : ''}
      ${i.recommendation ? `<div class="item-recommendation"><b>Recommendation:</b> ${esc(i.recommendation)}</div>` : ''}
      ${i.source ? `<div class="item-source">Source: ${esc(i.source)}</div>` : ''}
    </div>`;
  }).join('')}</div>`;
}

/* MAIN -- one .pillar-view section per pillar, house page-header pattern */
function renderPillarView(p) {
  const body = renderBacklog(p.backlog);

  return `
    <div class="pillar-view" id="view-${esc(p.id)}">
      <div class="page-header">
        <div>
          <div class="page-title">${esc(p.label)}</div>
          <div class="header-date">${esc(p.source || '')}</div>
        </div>
        <span class="badge ${badgeClass(p.status)}">${esc(statusLabel(p.status))}</span>
      </div>
      <p class="pillar-summary">${esc(p.summary || '')}</p>
      ${body}
      ${p.link ? `<a class="pillar-link" href="${esc(p.link)}" target="_blank" rel="noopener">Open live source →</a>` : ''}
    </div>
  `;
}

function renderMain(pillars) {
  document.getElementById('main').innerHTML = pillars.map(renderPillarView).join('');
}

/* VIEWS -- mirrors command-centre's showView()/nav-<id>/.active pattern exactly */
let PILLAR_IDS = [];
function showView(v) {
  PILLAR_IDS.forEach(function (id) {
    const el = document.getElementById('view-' + id);
    if (el) el.classList.toggle('active', id === v);
    const navEl = document.getElementById('nav-' + id);
    if (navEl) navEl.classList.toggle('active', id === v);
  });
  try { localStorage.setItem('workRoadmap_lastView', v); } catch (e) {}
}
window.showView = showView;

async function init() {
  try {
    const data = await loadData();
    document.getElementById('generatedAt').textContent = `Generated ${data.generated_at}`;
    PILLAR_IDS = data.pillars.map(p => p.id);
    renderNav(data.pillars);
    renderMain(data.pillars);
    let startView = PILLAR_IDS[0];
    try {
      const saved = localStorage.getItem('workRoadmap_lastView');
      if (saved && PILLAR_IDS.includes(saved)) startView = saved;
    } catch (e) {}
    showView(startView);
  } catch (err) {
    document.getElementById('main').innerHTML = `<p class="empty-note">Failed to load roadmap data: ${esc(err.message)}</p>`;
  }
}

init();
