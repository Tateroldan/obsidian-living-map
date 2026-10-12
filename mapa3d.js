// Mapa vivo 3D: proyeccion propia en canvas 2D (girar, zoom, mover, enfocar). Colores desde window.TEMA, textos desde t().
var AIDX = {}; // area -> posicion (var: crawler.js puede llamar col() antes de cargar el grafo)
const col = a => { const A = (window.TEMA && TEMA.areas) || ["#999"]; return A[(AIDX[a] || 0) % A.length]; };
// vc(verbo) viene de crawler.js (se carga antes).
const FONT = "'Departure Mono', ui-monospace, monospace";
if (document.fonts) document.fonts.load("11px 'Departure Mono'").catch(()=>{});
const $ = id => document.getElementById(id);

const cv = document.getElementById("c"), cx = cv.getContext("2d");
let W, H, DPR = Math.min(devicePixelRatio || 1, 2);
function resize(){ W = innerWidth; H = innerHeight; cv.width = W*DPR; cv.height = H*DPR; cv.style.width = W+"px"; cv.style.height = H+"px"; cx.setTransform(DPR,0,0,DPR,0,0); }
addEventListener("resize", resize); resize();

// ---------- cámara ----------
const FOV = 900, DIST0 = 1000;
const cam = {yaw: .6, pitch: -.35, dist: DIST0, tx: 0, ty: 0, tz: 0, follow: false, lastUser: 0};
const goal = {dist: DIST0, tx: 0, ty: 0, tz: 0};
let _yw = NaN, _pt = NaN, _cy = 1, _sy = 0, _cp = 1, _sp = 0; // senos de la cámara: solo se recalculan si gira
function proj(x, y, z){
  if (cam.yaw !== _yw || cam.pitch !== _pt) { _yw = cam.yaw; _pt = cam.pitch; _cy = Math.cos(_yw); _sy = Math.sin(_yw); _cp = Math.cos(_pt); _sp = Math.sin(_pt); }
  x -= cam.tx; y -= cam.ty; z -= cam.tz;
  let X = x*_cy - z*_sy, Z = x*_sy + z*_cy;
  const Y = y*_cp - Z*_sp; Z = y*_sp + Z*_cp;
  const d = cam.dist + Z; if (d < 40) return null;
  const f = FOV / d;
  return {x: W/2 + X*f, y: H*0.4 + Y*f, s: Math.min(4, f*DIST0/FOV), z: Z};
}
const depthA = p => Math.max(.18, Math.min(1, 1.15 - p.z/900));

let dragging = null, px = 0, py = 0;
cv.addEventListener("contextmenu", e => e.preventDefault());
cv.addEventListener("pointerdown", e => { dragging = e.button === 2 || e.shiftKey ? "pan" : "rot"; px = e.clientX; py = e.clientY; cam.lastUser = performance.now(); cv.setPointerCapture(e.pointerId); });
cv.addEventListener("pointerup", () => dragging = null);
cv.addEventListener("pointercancel", () => dragging = null);
const tip = document.createElement("div");
tip.style.cssText = "position:fixed;pointer-events:none;display:none;z-index:50;padding:4px 8px;background:var(--panel);border:1px solid var(--linea);border-radius:2px;font:400 11px "+FONT+";color:var(--texto);white-space:nowrap";
document.body.appendChild(tip);
let tipNode = null;
function showTip(e){
  if (dragging) { tip.style.display = "none"; tipNode = null; return; }
  const n = pick(e.clientX, e.clientY);
  if (!n) { tip.style.display = "none"; tipNode = null; return; }
  if (n !== tipNode) { tipNode = n; tip.innerHTML = "";
    tip.appendChild(document.createTextNode(n.title));
    if (n.folder || n.area) { const f = document.createElement("div"); f.style.cssText = "font-size:11px;color:var(--tenue)"; f.textContent = n.folder || n.area; tip.appendChild(f); }
    tip.style.borderColor = col(n.area); }
  tip.style.display = "block";
  const w = tip.offsetWidth, h = tip.offsetHeight;
  tip.style.left = Math.min(e.clientX + 14, innerWidth - w - 6) + "px"; tip.style.top = Math.min(e.clientY + 16, innerHeight - h - 6) + "px";
}
cv.addEventListener("pointermove", showTip);
cv.addEventListener("pointerleave", () => { tip.style.display = "none"; tipNode = null; });
cv.addEventListener("pointermove", e => {
  if (!dragging) return; const dx = e.clientX - px, dy = e.clientY - py; px = e.clientX; py = e.clientY; cam.lastUser = performance.now();
  if (dragging === "rot") { cam.yaw += dx*.006; cam.pitch = Math.max(-1.45, Math.min(1.45, cam.pitch + dy*.006)); }
  else { const k = cam.dist/FOV, c = Math.cos(cam.yaw), s = Math.sin(cam.yaw);
    goal.tx -= (dx*c)*k; goal.tz -= (-dx*s)*k; goal.ty -= dy*k; cam.follow = false; hint(); }
});
cv.addEventListener("wheel", e => { e.preventDefault(); goal.dist = Math.max(120, Math.min(3200, goal.dist * Math.exp(e.deltaY*.0012))); cam.lastUser = performance.now(); }, {passive: false});
// Clic simple (sin arrastrar) = abrir la nota en Obsidian; se espera un poco por si es doble clic.
let downX = 0, downY = 0, clickT = null;
cv.addEventListener("pointerdown", e => { downX = e.clientX; downY = e.clientY; });
cv.addEventListener("click", e => {
  if (Math.hypot(e.clientX - downX, e.clientY - downY) > 4) return;
  const n = pick(e.clientX, e.clientY); if (!n) return;
  clearTimeout(clickT);
  clickT = setTimeout(() => { location.href = "obsidian://open?vault=" + encodeURIComponent(VAULT) + "&file=" + encodeURIComponent(n.id); }, 260);
});
cv.addEventListener("dblclick", e => { clearTimeout(clickT); const n = pick(e.clientX, e.clientY); if (n) { focus(n, 380); cam.follow = false; hint(); crawlTo(n, "read", null, true); } });
addEventListener("keydown", e => {
  if (e.ctrlKey || e.metaKey || e.altKey || /^(SELECT|INPUT|TEXTAREA)$/.test(e.target.tagName)) return; // Ctrl+F / Ctrl+R son del navegador
  if (e.key === "f" || e.key === "F") { cam.follow = !cam.follow; hint(); }
  if (e.key === "r" || e.key === "R") { Object.assign(goal, {dist: DIST0, tx: 0, ty: 0, tz: 0}); cam.follow = false; hint(); }
});
function focus(n, dist){ goal.tx = n.x; goal.ty = n.y; goal.tz = n.z; if (dist) goal.dist = dist; }
function pick(mx, my){ let best = null, bd = 14; for (const n of nodes) { const p = proj(n.x, n.y, n.z); if (!p) continue; const d = Math.hypot(p.x-mx, p.y-my); if (d < bd) { bd = d; best = n; } } return best; }
function hint(){ const f = $("follow"); f.textContent = t(cam.follow ? "siguiendo" : "seguir"); f.style.color = cam.follow ? "var(--acento)" : ""; }
function textosCtrl(){ $("selTema").setAttribute("aria-label", t("tema")); $("selIdioma").setAttribute("aria-label", t("idioma")); $("c1").textContent = t("ctrl1"); $("c2").textContent = t("ctrl2"); hint(); }

// ---------- grafo ----------
let nodes = [], links = [], byId = {}, adj = {}, areas = [], anchors = {}, dust = [], sim;
const visited = new Set(); let stats = {read:0, write:0, search:0}, since = 0;
const evTimes = [], feedItems = [], recentAreas = [];
const gauss = () => (Math.random()+Math.random()+Math.random()-1.5)/1.5;

var INICIO = "Inicio"; // nota donde arranca la araña (la manda /graph)
var DECISIONES = "Decisiones pendientes"; // nota de casillas abiertas (la manda /graph)
var VAULT = "Boveda"; // nombre de la bóveda para obsidian:// (lo manda /graph)
const MAX_POLVO = 8000, MAX_ANIM = 12, MAX_ETIQ = 40;
// ---- tejido: una nota nueva nace donde la araña llega y esta la une a sus vecinas con hilos
const HILO_MS = 700, HILO_GAP = 420, MAX_HILOS = 10, NACE_MS = 900;
const hilos = [], tejiendo = new Map();           // tejiendo: "a|b" -> hilo (oculta la arista normal mientras crece)
const llaveHilo = (a, b) => a + "|" + b;
function tejer(n){
  const sp = principal, now = performance.now();
  const d = Math.hypot(n.x - sp.x, n.y - sp.y, n.z - sp.z);
  const llega = now + ANTICIPA + (d < 8 ? 500 : Math.min(VIAJE_MAX, Math.max(VIAJE_MIN, d/VEL)));
  n.nace = llega - 150;                            // invisible hasta que la araña llega
  crawlTo(n, "write", n.title, false, null);
  (adj[n.id] || []).slice(0, MAX_HILOS).forEach((m, i) => {
    const h = {a: n, b: m, ini: llega + 200 + i*HILO_GAP, dur: HILO_MS, fin: false};
    hilos.push(h); tejiendo.set(llaveHilo(n.id, m.id), h); tejiendo.set(llaveHilo(m.id, n.id), h); });
}
// pide el grafo ya (no esperar los 30 s) cuando Claude escribe una nota que aún no existe
function refrescarGrafo(){
  if (refrescarGrafo.p) return; refrescarGrafo.p = true;
  setTimeout(() => loadGraph(false).catch(() => {}), 700);
  setTimeout(() => { refrescarGrafo.p = false; loadGraph(false).catch(() => {}); }, 2800);
}

let firmaG = null;
async function loadGraph(first){
  const g = await (await fetch("/graph")).json();
  if (g.vault) VAULT = g.vault;
  if (g.decisiones) DECISIONES = g.decisiones;
  if (g.inicio) INICIO = g.inicio;
  const sig = g.nodes.map(n => n.id + ":" + n.area).join("|") + "#" + g.links.map(l => l.source + ">" + l.target).sort().join("|");
  if (sig === firmaG) { for (const n of g.nodes) if (byId[n.id]) byId[n.id].words = n.words; return; } // nada cambió: ni simulación ni polvo se reinician
  firmaG = sig;
  const old = byId; byId = {}; adj = {};
  const cnt = {}; for (const n of g.nodes) cnt[n.area] = (cnt[n.area] || 0) + 1;
  areas = Object.keys(cnt).sort((a,b) => cnt[b] - cnt[a]);
  AIDX = {}; areas.forEach((a,i) => AIDX[a] = i);
  const R = 300, k = areas.length;
  areas.forEach((a,i) => { // esfera de Fibonacci: cada área en su lugar del espacio
    const y = 1 - (i + .5)/k*2, r = Math.sqrt(1 - y*y), th = i * 2.399963;
    anchors[a] = {x: Math.cos(th)*r*R, y: y*R*.75, z: Math.sin(th)*r*R}; });
  const hayViejos = !first && Object.keys(old).length > 0, nuevas = [], vecinas = {};
  if (hayViejos) for (const l of g.links) { // vecinas ya existentes de cada nota nueva
    if (!old[l.source] && old[l.target]) (vecinas[l.source] = vecinas[l.source] || []).push(old[l.target]);
    if (!old[l.target] && old[l.source]) (vecinas[l.target] = vecinas[l.target] || []).push(old[l.source]); }
  nodes = g.nodes.map(n => { const o = old[n.id], an = anchors[n.area], spread = 25 + Math.sqrt(cnt[n.area])*9;
    if (o) return Object.assign(o, n, {vx:0, vy:0, vz:0}); // mismo objeto: las arañas no se quedan apuntando a nodos viejos
    const v = vecinas[n.id];
    if (hayViejos) nuevas.push(n);
    if (v && v.length) { const c = {x: 0, y: 0, z: 0}; v.forEach(m => { c.x += m.x; c.y += m.y; c.z += m.z; });
      return Object.assign(n, {x: c.x/v.length + gauss()*14, y: c.y/v.length + gauss()*14, z: c.z/v.length + gauss()*14, glow: 0}); }
    return Object.assign(n, {x: an.x + gauss()*spread, y: an.y + gauss()*spread, z: an.z + gauss()*spread, glow: 0}); });
  nodes.forEach(n => { byId[n.id] = n; adj[n.id] = []; });
  links = g.links.filter(l => byId[l.source] && byId[l.target]).map(l => ({source: byId[l.source], target: byId[l.target], heat: 0}));
  links.forEach(l => { adj[l.source.id].push(l.target); adj[l.target.id].push(l.source); });
  if (sim) sim.stop();
  sim = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).distance(l => l.source.area === l.target.area ? 30 : 160).strength(l => l.source.area === l.target.area ? .4 : .02))
    .force("charge", d3.forceManyBody().strength(-22))
    .force("x", d3.forceX(n => anchors[n.area].x).strength(.06))
    .force("y", d3.forceY(n => anchors[n.area].y).strength(.06))
    .force("z", alpha => { for (const n of nodes) { // fuerza propia en el eje z
        n.vz = (n.vz || 0) + (anchors[n.area].z - n.z) * .06 * alpha;
        for (const m of adj[n.id]) if (m.area === n.area) n.vz += (m.z - n.z) * .01 * alpha;
        n.vz *= .6; n.z += n.vz; } })
    .force("col", d3.forceCollide(6)).alpha(first ? 1 : .3).alphaDecay(.02);
  dust = []; let tot = 0; for (const n of nodes) tot += 18 + Math.min(60, n.words/18);
  const fp = Math.min(1, MAX_POLVO / (tot || 1)); // tope global: en bóvedas grandes el polvo se reparte
  nodes.forEach(n => { const k = Math.max(3, (18 + Math.min(60, n.words/18)) * fp); for (let i = 0; i < k; i++) {
    const r = 6 + Math.random()*Math.random()*85, u = Math.random()*2-1, th = Math.random()*Math.PI*2, q = Math.sqrt(1-u*u);
    dust.push({n, dx: q*Math.cos(th)*r, dy: u*r*.8, dz: q*Math.sin(th)*r, z: Math.random()}); } });
  $("sN").textContent = nodes.length; $("sL").textContent = links.length;
  const w = $("wait"); w.style.display = nodes.length ? "none" : "flex";
  if (!nodes.length) { w.dataset.i18n = "vacia"; w.textContent = t("vacia"); }
  arrancarArana();
  nuevas.slice(0, 4).forEach((n, i) => setTimeout(() => tejer(n), i*1500)); // varias a la vez: una tras otra
}
function arrancarArana(){
  if (principal.node || !nodes.length) return;
  const s = byId[INICIO] || nodes[0]; principal.x = s.x; principal.y = s.y; principal.z = s.z;
  crawlTo(s, "read");
}

// (la arana vive en crawler.js: principal, aranas, crawlTo (cola por araña), lastTouch, casc, TOUCH_MS, CASC_MS...)

// ---------- eventos ----------
function verbOf(e){ return e.verb === "write" ? "write" : e.verb === "search" ? "search" : "read"; }
const VERBO_T = {read: "leer", write: "escribir", search: "buscar"};
function registrar(v, titulo, n, q){
  stats[v]++; evTimes.push(Date.now());
  if (n) { visited.add(n.id); recentAreas.unshift(n.area); const i = recentAreas.indexOf(n.area, 1); if (i > 0) recentAreas.splice(i, 1); recentAreas.length = Math.min(recentAreas.length, 5); }
  feedItems.unshift({t: new Date(), v, titulo, q}); feedItems.length = Math.min(feedItems.length, 12);
  renderFeed(); renderDatos();
}
// quién hizo el evento: agente (subagente) o, si no hay, la sesión; etiqueta = agent_type o 4 primeros caracteres del id
function quien(e){ const k = e.agente || e.session || ""; return k ? {k, tag: e.agent_type || k.slice(0, 4)} : null; }
function handle(e, ghost, mudo){ // mudo: se cuenta en el feed pero la araña no camina
  let n = byId[e.id]; const q = ghost ? null : quien(e);
  const v = verbOf(e);
  if (!n && !ghost && v === "write" && e.id && !refrescarGrafo.p) refrescarGrafo();
  if (!n) {
    const pref = (e.id || "").split("/")[0];
    const inArea = nodes.filter(x => x.id.startsWith(pref + "/") || x.folder === pref);
    n = inArea.length ? inArea[Math.floor(Math.random()*inArea.length)] : null;
    if (!n && !ghost) { registrar(v, (e.id || e.path || "").split("/").pop() || "/", null, q); return; }
  }
  if (!ghost) registrar(v, n.title, n, q);
  if (!mudo) crawlTo(n, ghost ? "walk" : v, e.id && !byId[e.id] ? e.id : null, false, q);
}
let lastReal = 0;
async function poll(){
  try {
    const r = await (await fetch("/events?since=" + since)).json();
    if (!poll.primed) { since = r.next; poll.primed = true; } // empieza desde ahora
    else { const ev = r.events, corte = Math.max(0, ev.length - MAX_ANIM);
      ev.slice(0, corte).forEach(e => handle(e, false, true)); // ráfaga: lo viejo solo se cuenta, se animan los últimos
      ev.slice(corte).forEach((e,i) => setTimeout(() => handle(e), i*350)); since = r.next; if (ev.length) lastReal = Date.now(); }
  } catch (_) {}
  setTimeout(poll, 800);
}
function idleWalk(){
  if (Date.now() - lastReal > 12000 && nodes.length) {
    const cur = principal.node, nb = cur && adj[cur.id] && adj[cur.id].length ? adj[cur.id] : nodes;
    handle({id: nb[Math.floor(Math.random()*nb.length)].id}, true);
  }
  setTimeout(idleWalk, 2600);
}

// ---------- HUD ----------
function setTitle(){} // compatibilidad con crawler.js
function setArea(){}
const hhmm = d => String(d.getHours()).padStart(2,"0") + ":" + String(d.getMinutes()).padStart(2,"0") + ":" + String(d.getSeconds()).padStart(2,"0");
const esc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;");
function colorDeClave(k){ const sp = aranas.get(k); return sp ? colorAr(sp) : "var(--tenue)"; }
function renderFeed(){
  $("log").innerHTML = feedItems.length ? feedItems.map(f => `<div><i>${hhmm(f.t)}</i><span class="v-${f.v}">${esc(t(VERBO_T[f.v]))}</span><span class="n">${f.q ? `<b class="ag" style="color:${colorDeClave(f.q.k)}">${esc(f.q.tag)}</b>` : ""}${esc(f.titulo)}</span></div>`).join("")
    : `<div class="vacio">${esc(t("sinEventos"))}</div>`;
}
function renderDatos(){
  const now = Date.now(); while (evTimes.length && now - evTimes[0] > 600000) evTimes.shift();
  $("sR").textContent = stats.read; $("sW").textContent = stats.write; $("sS").textContent = stats.search;
  $("rate").textContent = evTimes.filter(x => now - x < 60000).length;
  const fs = focoSpider(), n = fs.node; $("cur").textContent = n ? n.title : t("ninguna"); $("curArea").textContent = n ? (n.folder || n.area) : "";
  const ars = todas().filter(q => q === principal ? !!q.clave : true);
  $("arList").innerHTML = (ars.length ? ars : [principal]).map(q => `<span style="color:${colorAr(q)}">■ ${esc(q.tag || t("principalAr"))}</span>`).join(" ");
  $("areasR").innerHTML = recentAreas.length ? recentAreas.map(a => `<div><i style="background:${col(a)}"></i>${esc(a)}</div>`).join("") : `<div style="color:var(--tenue)">${esc(t("ninguna"))}</div>`;
  const live = lastReal && now - lastReal < 15000;
  $("punto").className = live ? "on" : ""; $("estTxt").dataset.i18n = live ? "live" : "idle"; $("estTxt").textContent = t(live ? "live" : "idle");
  drawSpark();
}
function drawSpark(){
  const c = $("spark"), w = c.clientWidth, h = c.clientHeight; if (!w) return;
  if (c.width !== w*DPR || c.height !== h*DPR) { c.width = w*DPR; c.height = h*DPR; }
  const g = c.getContext("2d"); g.setTransform(DPR,0,0,DPR,0,0); g.clearRect(0,0,w,h);
  const B = 20, span = 600000/B, now = Date.now(), b = Array(B).fill(0);
  evTimes.forEach(x => { const i = B - 1 - Math.floor((now - x)/span); if (i >= 0 && i < B) b[i]++; });
  const mx = Math.max(3, ...b), bw = w/B;
  g.strokeStyle = TEMA.linea; g.lineWidth = 1;
  g.beginPath(); g.moveTo(0, h - .5); g.lineTo(w, h - .5); g.stroke();
  g.strokeStyle = TEMA.acento; g.lineWidth = 1.5; g.beginPath();
  b.forEach((v,i) => { const x = (i + .5)*bw, y = h - 2 - (h - 6)*v/mx; i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.stroke();
}
setInterval(renderDatos, 1000);

// selectores y plegado
const selT = $("selTema"), selI = $("selIdioma");
TEMAS_ORDEN.forEach(id => selT.add(new Option(TEMAS[id].nombre, id)));
Object.keys(IDIOMAS).forEach(c => selI.add(new Option(IDIOMAS[c], c)));
selT.onchange = () => aplicarTema(selT.value); selI.onchange = () => aplicarIdioma(selI.value);
let FONDO_RGB = "14,15,17";
document.addEventListener("tema", e => { selT.value = e.detail; FONDO_RGB = getComputedStyle(document.documentElement).getPropertyValue("--fondo-rgb").trim() || FONDO_RGB; renderFeed(); });
document.addEventListener("idioma", e => { selI.value = e.detail; textosCtrl(); renderFeed(); renderDatos(); if (window.renderPaneles) renderPaneles(); });
function plegar(cls, btn, abierto){ document.body.classList.toggle(cls, !abierto); $(btn).setAttribute("aria-pressed", abierto); }
$("tgFeed").onclick = () => plegar("sin-feed", "tgFeed", document.body.classList.contains("sin-feed"));
$("tgDatos").onclick = () => plegar("sin-datos", "tgDatos", document.body.classList.contains("sin-datos"));
const estrecho = innerWidth < 760;
plegar("sin-feed", "tgFeed", !estrecho); plegar("sin-datos", "tgDatos", !estrecho);
aplicarTema(TEMA.id); aplicarIdioma(IDIOMA); selT.value = TEMA.id; selI.value = IDIOMA;

// ---------- dibujo ----------
// etiquetas sin encimarse: cada una reserva su rectángulo y la que choca no se dibuja
const ocupados = [];
function cabe(x, y, w, h){
  for (const o of ocupados) if (x < o.x + o.w && x + w > o.x && y < o.y + o.h && y + h > o.y) return false;
  ocupados.push({x, y, w, h}); return true;
}
const prio = n => (n.glow > .05 ? 8 : 0) + (visited.has(n.id) ? 4 : 0) + n._p.s;
const QUIETO = matchMedia("(prefers-reduced-motion: reduce)").matches;
// los paneles del HUD también ocupan sitio: ninguna etiqueta queda cortada debajo de ellos
let _rp = [], _rpT = -1e9;
function reservarPaneles(now){
  if (now - _rpT > 400) { _rpT = now; _rp = ["bar", "feed", "datos", "ctrl", "pDec", "pSal"].map(id => $(id).getBoundingClientRect()).filter(r => r.width && r.height); }
  for (const r of _rp) ocupados.push({x: r.left, y: r.top, w: r.width, h: r.height});
}
function zonas(cw){
  const acc = {}, foco = focoSpider().node, actA = foco && foco.area;
  for (const n of nodes) { const z = acc[n.area] || (acc[n.area] = {x:0, z:0, y:1e9, c:0, v:0}); z.x += n.x; z.z += n.z; z.c++; if (n.y < z.y) z.y = n.y; if (visited.has(n.id)) z.v++; }
  cx.textAlign = "center";
  for (const a of areas) { const o = acc[a]; if (!o) continue;
    const p = proj(o.x/o.c, o.y - 18, o.z/o.c); if (!p) continue;
    const act = a === actA, da = depthA(p), sub = tn("nNotas", o.c) + " · " + tn("nTocadas", o.v), w = Math.max(a.length, sub.length)*cw + 8;
    if (!cabe(p.x - w/2, p.y - 11, w, 27) && !act) continue;
    cx.globalAlpha = (act ? .9 : .5) * da; cx.fillStyle = col(a); cx.font = "11px " + FONT; cx.fillText(a.toUpperCase(), p.x, p.y);
    cx.globalAlpha = .45 * da; cx.fillStyle = TEMA.textoTenue; cx.fillText(sub, p.x, p.y + 12); }
}
function etiquetas(cw){
  cx.save(); cx.textAlign = "left"; cx.lineWidth = 3; cx.lineJoin = "round"; cx.strokeStyle = "rgb(" + FONDO_RGB + ")"; cx.fillStyle = TEMA.texto;
  const cand = nodes.filter(n => n._p && n._p.s >= 1.6).sort((a,b) => prio(b) - prio(a)); let puestas = 0;
  for (const n of cand) { if (puestas >= MAX_ETIQ) break; const p = n._p;
    if (!cabe(p.x + 4, p.y - 8, n.title.length*cw + 6, 14)) continue; puestas++;
    cx.globalAlpha = Math.min(.85, (p.s - 1.6)*.8 + (n.glow > .05 ? .4 : 0)) * depthA(p);
    cx.strokeText(n.title, p.x + 6, p.y + 3); cx.fillText(n.title, p.x + 6, p.y + 3); } // halo del color del fondo
  cx.restore();
}
function frame(now){
  requestAnimationFrame(frame); // primero: un error al dibujar no detiene la animación
  try { dibujar(now); } catch (e) { if (!frame.avisado) { frame.avisado = true; console.error("mapa vivo:", e); } }
}
function dibujar(now){
  if (!QUIETO && !dragging && now - cam.lastUser > 5000) cam.yaw += .0016;
  if (TEMA.ciclo && !QUIETO) cicloRGB(now);
  { const fs = focoSpider(); if (cam.follow && fs.node) { goal.tx = fs.x; goal.ty = fs.y; goal.tz = fs.z; } }
  cam.dist += (goal.dist - cam.dist)*.12; cam.tx += (goal.tx - cam.tx)*.08; cam.ty += (goal.ty - cam.ty)*.08; cam.tz += (goal.tz - cam.tz)*.08;
  const claro = !!TEMA.claro, boost = claro ? 2.2 : 1;
  cx.globalCompositeOperation = "source-over"; cx.fillStyle = "rgba(" + FONDO_RGB + ",.42)"; cx.fillRect(0,0,W,H);
  cx.globalCompositeOperation = claro ? "source-over" : "lighter";
  for (const d of dust) { const p = proj(d.n.x + d.dx, d.n.y + d.dy, d.n.z + d.dz); if (!p) continue;
    const g = d.n.glow, sz = (1 + g) * Math.max(.6, p.s*.9);
    cx.fillStyle = col(d.n.area); cx.globalAlpha = Math.min(1, (.09 + d.z*.13 + g*.3) * boost) * depthA(p); cx.fillRect(p.x, p.y, sz, sz); }
  for (const l of links) { l.heat *= .985; const a = proj(l.source.x, l.source.y, l.source.z), b = proj(l.target.x, l.target.y, l.target.z); if (!a || !b) continue;
    { const h = tejiendo.size && tejiendo.get(llaveHilo(l.source.id, l.target.id)); if (h && now < h.ini + h.dur) continue; } // la dibuja el tejido
    cx.strokeStyle = TEMA.arista; cx.globalAlpha = Math.min(.35, (.045 + l.heat*.06) * (claro ? 2 : 1)) * Math.min(depthA(a), depthA(b)); cx.lineWidth = 1;
    cx.beginPath(); cx.moveTo(a.x, a.y); cx.lineTo(b.x, b.y); cx.stroke(); }
  // hilos de seda: crecen desde la nota nueva hacia cada vecina y al llegar la hacen brillar
  for (let i = hilos.length - 1; i >= 0; i--) { const h = hilos[i];
    if (now < h.ini) continue;
    const u = clamp01((now - h.ini)/h.dur), e = smooth(u), A = proj(h.a.x, h.a.y, h.a.z), B = proj(h.b.x, h.b.y, h.b.z);
    if (u >= 1) { if (!h.fin) { h.fin = true; h.b.glow = Math.max(h.b.glow, 1); h.a.glow = Math.max(h.a.glow, .8); }
      tejiendo.delete(llaveHilo(h.a.id, h.b.id)); tejiendo.delete(llaveHilo(h.b.id, h.a.id)); hilos.splice(i, 1); continue; }
    if (!A || !B) continue;
    const x = A.x + (B.x - A.x)*e, y = A.y + (B.y - A.y)*e, da = Math.min(depthA(A), depthA(B));
    cx.strokeStyle = vc("write"); cx.lineWidth = 1.6; cx.globalAlpha = .85*da; cx.beginPath(); cx.moveTo(A.x, A.y); cx.lineTo(x, y); cx.stroke();
    cx.fillStyle = "#ffffff"; cx.globalAlpha = .9*da; cx.beginPath(); cx.arc(x, y, 2.4, 0, 7); cx.fill(); // chispa en la punta
    cx.fillStyle = vc("write"); cx.globalAlpha = .25*da; cx.beginPath(); cx.arc(x, y, 7, 0, 7); cx.fill(); }
  for (const n of nodes) { n.glow *= .992; const p = n._p = proj(n.x, n.y, n.z); if (!p) continue;
    let nk = 1; if (n.nace) { if (now < n.nace) continue; nk = clamp01((now - n.nace)/NACE_MS); if (nk >= 1) n.nace = 0; } // nace: aparece al llegar la araña
    const c = col(n.area), r = (1.6 + Math.min(3, n.words/400) + n.glow*2.5) * p.s * (nk < 1 ? .25 + .75*smooth(nk) : 1), da = depthA(p);
    if (nk < 1) { cx.strokeStyle = vc("write"); cx.lineWidth = 1.4; cx.globalAlpha = (1 - nk)*.8*da; cx.beginPath(); cx.arc(p.x, p.y, r + 4 + nk*34*p.s, 0, 7); cx.stroke(); } // onda de nacimiento
    const sal = window.SALUD && SALUD.on, dim = sal && SALUD.nunca.has(n.id) ? .3 : 1;
    if (!claro) { cx.globalAlpha = (.06 + n.glow*.2) * da * dim; cx.fillStyle = c; cx.beginPath(); cx.arc(p.x, p.y, r*2.4 + 3, 0, 7); cx.fill(); } // halo del color del área
    cx.globalAlpha = (.55 + n.glow*.45) * da * dim; cx.fillStyle = visited.has(n.id) ? c : TEMA.nodo; cx.beginPath(); cx.arc(p.x, p.y, r, 0, 7); cx.fill();
    if (sal && SALUD.huer.has(n.id)) { cx.strokeStyle = TEMA.alerta || "#D55E00"; cx.lineWidth = 1.2; cx.globalAlpha = .5 * da; cx.beginPath(); cx.arc(p.x, p.y, r*2.6 + 2, 0, 7); cx.stroke(); }
    const lt = lastTouch[n.id], cs = casc[n.id];
    if (lt) { const k = 1 - (now - lt.t)/TOUCH_MS;
      if (k <= 0) delete lastTouch[n.id];
      else { cx.fillStyle = vc(lt.verb); cx.globalAlpha = k*.9*da; cx.beginPath(); cx.arc(p.x, p.y, r*1.15, 0, 7); cx.fill();
        cx.strokeStyle = vc(lt.verb); cx.lineWidth = 1; cx.globalAlpha = k*.5*da; cx.beginPath(); cx.arc(p.x, p.y, r*(1.6 + (1-k)*1.6), 0, 7); cx.stroke(); } }
    if (cs) { const k = 1 - (now - cs.t)/CASC_MS;
      if (k <= 0) delete casc[n.id];
      else { cx.fillStyle = vc(cs.verb); cx.globalAlpha = k*.4*da; cx.beginPath(); cx.arc(p.x, p.y, r*1.6, 0, 7); cx.fill(); } } }

  cx.globalCompositeOperation = "source-over";
  ocupados.length = 0; cx.font = "11px " + FONT; const cw = cx.measureText("M").width;
  if (nodes.length) for (const q of todas()) { const p = q.node && proj(q.x, q.y, q.z); if (p) ocupados.push({x: p.x - 70, y: p.y - 46, w: 140, h: 72}); } // sitio de las etiquetas de cada araña
  reservarPaneles(now); zonas(cw);
  if (cam.dist < 520) etiquetas(cw);
  cx.globalCompositeOperation = claro ? "source-over" : "lighter";

  if (nodes.length) { spiderUpdate(now); drawTrail(now); drawSpider(now); }
  cx.globalAlpha = 1; cx.globalCompositeOperation = "source-over";
}

(async () => {
  textosCtrl(); renderFeed();
  for (;;) { // si el servidor aún no responde, se avisa y se reintenta
    try { await loadGraph(true); break; }
    catch (_) { const w = $("wait"); w.dataset.i18n = "sinServidor"; w.textContent = t("sinServidor"); await new Promise(r => setTimeout(r, 2000)); }
  }
  renderDatos();
  requestAnimationFrame(frame); poll(); setTimeout(idleWalk, 6000);
  setInterval(() => loadGraph(false).then(() => renderDatos()).catch(() => {}), 30000);
})();
