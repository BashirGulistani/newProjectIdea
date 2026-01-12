const apiBase = "";

let ws = null;

function el(id) { return document.getElementById(id); }

function apiKey() { return el("apiKey").value.trim(); }
function me() { return Number(el("me").value); }


