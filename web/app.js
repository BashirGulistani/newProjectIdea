const apiBase = "";

let ws = null;

function el(id) { return document.getElementById(id); }

function apiKey() { return el("apiKey").value.trim(); }
function me() { return Number(el("me").value); }


async function api(path, opts = {}) {
  const headers = opts.headers || {};
  headers["Content-Type"] = "application/json";
  headers["X-API-Key"] = apiKey();
  const res = await fetch(apiBase + path, { ...opts, headers });
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  if (!res.ok) throw new Error((data && data.detail) ? data.detail : `HTTP ${res.status}`);
  return data;
}


function setWsStatus(s) {
  el("wsStatus").textContent = s;
}

function renderSignal(sig, { inbox } = {}) {
  const created = new Date(sig.created_at).toLocaleString();
  const expires = sig.expires_at ? new Date(sig.expires_at).toLocaleString() : "—";
  const who = inbox ? `from ${sig.sender_id}` : `to ${sig.recipient_id}`;
  const seen = sig.seen ? `seen @ ${new Date(sig.seen_at).toLocaleString()}` : "unseen";

  const div = document.createElement("div");
  div.className = "item";
  div.innerHTML = `
    <div class="top">
      <span>${who}</span>
      <span class="badge">${sig.kind}</span>
    </div>
    <div class="mono">created: ${created}\nexpires: ${expires}\n${seen}</div>
    ${inbox && !sig.seen ? `<button class="secondary" data-seen="${sig.id}">Mark seen</button>` : ""}
  `;
  return div;
}



