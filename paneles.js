// Paneles del HUD: DECISIONES pendientes (/decisiones) y modo SALUD de la bóveda (/salud). Se carga después de mapa3d.js (usa $, esc, t, TEMA).
window.SALUD = {on: false, huer: new Set(), nunca: new Set(), top: [], total: 0};
const obsDecisiones = () => "obsidian://open?vault=" + encodeURIComponent(VAULT) + "&file=" + encodeURIComponent(DECISIONES);
let listaDec = [];
function renderPaneles(){
  $("nDec").textContent = listaDec.length;
  $("decList").innerHTML = listaDec.length ? listaDec.map(d => `<div class="it">${esc(d)}</div>`).join("") : `<div class="vac">${esc(t("sinDecisiones"))}</div>`;
  const S = SALUD;
  $("salList").innerHTML = `<header class="lbl al">${esc(t("huerfanasT", {n: S.huer.size}))}</header><header class="lbl">${esc(t("nuncaT", {n: S.nunca.size}))}</header>`
    + `<header class="lbl">${esc(t("masTocadas"))}</header>` + (S.top.length ? S.top.slice(0, 5).map(x => `<div class="it pl">${x.n} · ${esc(x.id.split("/").pop())}</div>`).join("") : `<div class="vac">${esc(t("ninguna"))}</div>`);
}
async function cargarDecisiones(){
  try { const r = await (await fetch("/decisiones")).json(); if (Array.isArray(r)) listaDec = r; } catch (_) {}
  renderPaneles();
}
async function cargarSalud(){
  try { const r = await (await fetch("/salud")).json();
    SALUD.huer = new Set(r.huerfanas || []); SALUD.nunca = new Set(r.nunca || []); SALUD.top = r.top || []; SALUD.total = r.total || 0; } catch (_) {}
  renderPaneles();
}
function conmutar(btn, panel, abrir){ $(btn).setAttribute("aria-pressed", abrir); if (panel) $(panel).hidden = !abrir; }
$("decList").onclick = () => { location.href = obsDecisiones(); };
$("tgDec").onclick = () => conmutar("tgDec", "pDec", $("pDec").hidden);
$("tgSalud").onclick = () => { SALUD.on = !SALUD.on; conmutar("tgSalud", "pSal", SALUD.on); if (SALUD.on) cargarSalud(); };
cargarDecisiones(); setInterval(cargarDecisiones, 30000);
setInterval(() => { if (SALUD.on) cargarSalud(); }, 60000);
