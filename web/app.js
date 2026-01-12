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




async function refresh() {
  const userId = me();
  const inbox = await api(`/signals/inbox?user_id=${userId}&limit=100`);
  const outbox = await api(`/signals/outbox?user_id=${userId}&limit=100`);

  const inboxEl = el("inbox");
  inboxEl.innerHTML = "";
  inbox.forEach(sig => inboxEl.appendChild(renderSignal(sig, { inbox: true })));

  const outboxEl = el("outbox");
  outboxEl.innerHTML = "";
  outbox.forEach(sig => outboxEl.appendChild(renderSignal(sig, { inbox: false })));
}

async function send() {
  const payload = {
    sender_id: me(),
    recipient_id: Number(el("to").value),
    kind: el("kind").value,
    ttl_minutes: el("ttl").value ? Number(el("ttl").value) : null
  };

  try {
    const sig = await api("/signals", { method: "POST", body: JSON.stringify(payload) });
    el("sendResult").textContent = "sent:\n" + JSON.stringify(sig, null, 2);
    await refresh();
  } catch (e) {
    el("sendResult").textContent = "error: " + e.message;
  }
}

function connectWs() {
  if (ws) {
    ws.close();
    ws = null;
  }
  const userId = me();
  const proto = location.protocol === "https:" ? "wss" : "ws";
  ws = new WebSocket(`${proto}://${location.host}/ws?user_id=${userId}`);

  ws.onopen = () => setWsStatus("connected");
  ws.onclose = () => setWsStatus("disconnected");
  ws.onerror = () => setWsStatus("error");
  ws.onmessage = (evt) => {
    try {
      const msg = JSON.parse(evt.data);
      if (msg.type === "signal_created") {
        refresh();
      }
    } catch {}
  };
}


document.addEventListener("click", async (e) => {
  const btn = e.target.closest("button[data-seen]");
  if (!btn) return;
  const signalId = Number(btn.getAttribute("data-seen"));
  try {
    await api(`/signals/${signalId}/seen?user_id=${me()}`, { method: "POST" });
    await refresh();
  } catch (err) {
    alert(err.message);
  }
});

el("sendBtn").addEventListener("click", send);
el("refreshBtn").addEventListener("click", refresh);
el("connectBtn").addEventListener("click", connectWs);






