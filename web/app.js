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




