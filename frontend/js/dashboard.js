(() => {
  const apiBase = (typeof window.API_BASE_URL === 'string' ? window.API_BASE_URL : '').replace(/\/$/, '');

  async function fetchAlerts() {
    const url = `${apiBase}/api/alerts`;
    const { data: sessionData } = await window.supabaseClient.auth.getSession();
    const accessToken = sessionData?.session?.access_token;

    const headers = { 'Content-Type': 'application/json' };
    if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

    const res = await fetch(url, { headers });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `Failed to fetch alerts: ${res.status}`);
    }
    return res.json();
  }

  function formatDateTime(isoString) {
    if (!isoString) return { date: '', time: '' };
    const d = new Date(isoString);
    const date = d.toLocaleDateString();
    const time = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return { date, time };
  }

  function renderRows(alerts) {
    const tbody = document.getElementById('alerts-tbody');
    const empty = document.getElementById('empty-state');
    tbody.innerHTML = '';

    if (!alerts || alerts.length === 0) {
      empty.classList.remove('hidden');
      return;
    }
    empty.classList.add('hidden');

    for (const alert of alerts) {
      const { date, time } = formatDateTime(alert.timestamp || alert.created_at);
      const tr = document.createElement('tr');
      tr.className = 'hover:bg-slate-50';
      tr.innerHTML = `
        <td class="px-4 py-3 text-sm text-slate-700">${alert.driver_id ?? ''}</td>
        <td class="px-4 py-3 text-sm text-slate-700">${alert.driver_name ?? ''}</td>
        <td class="px-4 py-3 text-sm text-slate-700">${date}</td>
        <td class="px-4 py-3 text-sm text-slate-700">${time}</td>
        <td class="px-4 py-3 text-sm text-slate-700">${alert.location ?? ''}</td>
        <td class="px-4 py-3 text-sm">
          <span class="inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
            (alert.status || '').toLowerCase() === 'resolved'
              ? 'bg-green-100 text-green-700'
              : 'bg-amber-100 text-amber-700'
          }">${alert.status ?? ''}</span>
        </td>`;
      tbody.appendChild(tr);
    }
  }

  async function load() {
    const errorEl = document.getElementById('error-state');
    try {
      errorEl.classList.add('hidden');
      errorEl.textContent = '';
      const alerts = await fetchAlerts();
      renderRows(alerts);
    } catch (err) {
      errorEl.textContent = err.message || 'Failed to load alerts';
      errorEl.classList.remove('hidden');
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('refresh-btn')?.addEventListener('click', load);
    load();
  });
})();


