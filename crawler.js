// Crawler "araña": araña realista estilizada (cefalotórax + abdomen, 8 patas con IK de 2 huesos, pies que se apoyan en notas),
// rastro fino que se desvanece y zona teñida. Usa globales de mapa3d.js (nodes, adj, links, proj, col, cx, cam, goal, FOV, depthA...).
// Colores: window.TEMA.arana / window.TEMA.verbos (con valores por defecto sobrios).
// ---- constantes que ajustan el look ----
const LARGO_PATA = 44;                    // px (a escala 1) de fémur+tibia de una pata media
const T_PASO = 190;                       // ms que dura un paso a velocidad baja (baja con la velocidad del cuerpo)
const ALTURA_PASO = 9;                    // px que se levanta el pie en el arco del paso
const ESCALA_ARANA = 1.6;                  // tamaño global de la araña
const MAX_AGARRE = 2;                     // patas delanteras que pueden agarrar notas a la vez
const T_CRECE = 420;                      // ms que tarda una pata en estirarse a la nota
const ANTICIPA = 450;                     // ms estirando antes de jalar el cuerpo
const VEL = 0.2, VIAJE_MIN = 800, VIAJE_MAX = 1800; // unidades/ms y límites de duración del viaje
const RASTRO_MS = 60000;                  // vida del rastro
const DEF = {cuerpo: "#1a1d22", contorno: "#c9ccd1", patas: "#c9ccd1", acento: "#9b6dff", rastro: "rgba(201,204,209,.35)",
  etiquetaFondo: "#1a1d22", etiquetaTexto: "#e6e8eb"};
const tc = k => (window.TEMA && window.TEMA.arana && window.TEMA.arana[k]) || DEF[k];
const DEF_VERBOS = {read: "#56b4e9", write: "#9b6dff", search: "#b48ead"};
function vc(v){ return (window.TEMA && window.TEMA.verbos && window.TEMA.verbos[v]) || DEF_VERBOS[v] || tc("acento"); }   // lo usa mapa3d.js

// ---- arañas: una por agente o sesión (Map por clave). Cada araña lleva su propio estado (incl. `cola` de eventos) y las funciones reciben `sp`; `principal` = la del paseo automático.
const MAX_ARANAS = 6, INACT_MS = 300000, FADE_MS = 4000;
const nuevaSp = ci => ({x: 0, y: 0, z: 0, node: null, prev: null, legs: [], mode: "idle", born: 0, t0: 0, dur: 1, from: {x:0,y:0,z:0},
  arrived: true, settleAt: 0, gid: 0, trail: [], lastPt: 0, pruneAt: 0, mv: 0, ik: null, cola: [], tu: 0,
  ci, fade: 1, last: performance.now(), clave: null, tag: ""});
const principal = nuevaSp(-1), aranas = new Map();   // aranas: clave -> araña (incluye a la principal cuando atiende a una clave)
let activa = principal;
const todas = () => [principal, ...[...aranas.values()].filter(q => q !== principal)];
function colorAr(sp){ if (sp.ci < 0) return tc("acento"); const A = (window.TEMA && (window.TEMA.aranas || window.TEMA.areas)) || [tc("acento")]; return A[(sp.ci + (window.TEMA.aranas ? 0 : 1)) % A.length]; }
const focoSpider = () => activa;
// q = {k: clave (agente o sesión), tag: etiqueta corta}; sin q = la principal (paseo automático)
function elegirArana(q){
  if (!q || !q.k) return principal;
  const now = performance.now(); let sp = aranas.get(q.k);
  if (!sp) {
    if (!principal.clave) { sp = principal; sp.fade = 1; }
    else {
      if (aranas.size >= MAX_ARANAS) { let old = null; for (const o of aranas.values()) if (o !== principal && (!old || o.last < old.last)) old = o; if (old) { aranas.delete(old.clave); if (activa === old) activa = principal; } }
      const usados = new Set([...aranas.values()].map(o => o.ci)); let ci = 0; while (usados.has(ci)) ci++;
      sp = nuevaSp(ci); sp.x = principal.x; sp.y = principal.y; sp.z = principal.z;
    }
    sp.clave = q.k; aranas.set(q.k, sp);
  }
  if (q.tag) sp.tag = q.tag;
  sp.last = now; sp.fade = 1; activa = sp; return sp;
}
function gestionar(now){   // inactivas > 5 min: se desvanecen y se eliminan (la principal solo suelta su clave)
  for (const [k, sp] of [...aranas]) {
    const ina = now - sp.last - INACT_MS; if (ina <= 0) continue;
    if (sp === principal) { aranas.delete(k); sp.clave = null; sp.tag = ""; sp.fade = 1; if (activa === sp) activa = principal; continue; }
    sp.fade = clamp01(1 - ina/FADE_MS);
    if (sp.fade <= 0) { aranas.delete(k); if (activa === sp) activa = principal; }
  }
}
const lastTouch = {}, casc = {}, TOUCH_MS = 90000, CASC_MS = 20000;

const hexA = (h, a) => { const v = parseInt(h.slice(1), 16); return `rgba(${v>>16},${(v>>8)&255},${v&255},${a})`; };
const smooth = u => u*u*(3 - 2*u), clamp01 = u => Math.max(0, Math.min(1, u));

// notas cercanas: vecinos del grafo, vecinos de vecinos y unas al azar de la misma área (sin O(n²))
function cercanas(n, k){
  const a1 = adj[n.id] || [], pool = a1.slice();   // solo vecinos reales (enlaces del grafo)
  const out = [], seen = new Set([n.id]);
  for (let i = pool.length - 1; i > 0; i--) { const j = (Math.random()*(i+1))|0; [pool[i], pool[j]] = [pool[j], pool[i]]; }
  for (const m of pool) { if (out.length >= k) break; if (!seen.has(m.id)) { seen.add(m.id); out.push(m); } }
  return out;
}
const cortar = t => t.length > 24 ? t.slice(0, 23) + "…" : t;
// agarres: máximo MAX_AGARRE vivos; cada uno lo toma una pata delantera
function lanzar(sp, list, now, gid, primera){
  list.slice(0, MAX_AGARRE).forEach((m, i) => {
    sp.legs.forEach(L => { if (!L.dying && L.m === m) L.dying = now; });
    sp.legs.push({m, born: now + i*90, dying: 0, release: 0, gid, ext: 0, side: -1, tag: cortar(m.title), main: primera && i === 0});
  });
  const alive = sp.legs.filter(L => !L.dying);
  if (alive.length > MAX_AGARRE) alive.slice(0, alive.length - MAX_AGARRE).forEach(L => L.dying = now);
}

function _crawlTo(sp, n, verb, label, quiet){
  if (!n) return;
  const tnow = performance.now();
  sp.prev = sp.node; sp.node = n; sp.mode = verb; sp.born = tnow;
  sp.from = {x: sp.x, y: sp.y, z: sp.z};
  const d = Math.hypot(n.x - sp.x, n.y - sp.y, n.z - sp.z);
  sp.dur = d < 8 ? 500 : Math.min(VIAJE_MAX, Math.max(VIAJE_MIN, d/VEL));
  sp.t0 = tnow + ANTICIPA; sp.arrived = false; sp.settleAt = 0; sp.gid++;
  sp.legs.forEach(L => { if (!L.dying && L.gid !== sp.gid) L.release = sp.t0 + 200 + Math.random()*sp.dur*.5; });
  lanzar(sp, verb === "walk" ? [n] : [n, ...cercanas(n, MAX_AGARRE - 1)], tnow, sp.gid, true);
  n.glow = 1;
  if (verb !== "walk") { // rastro por verbo + cascada a vecinos (1 nivel, ≤30)
    lastTouch[n.id] = {t: tnow, verb};
    (adj[n.id] || []).slice(0, 30).forEach(m => { if (!lastTouch[m.id] || tnow - lastTouch[m.id].t > TOUCH_MS) casc[m.id] = {t: tnow, verb}; });
  } else (adj[n.id] || []).slice(0, 22).forEach(m => m.glow = Math.max(m.glow, .55));
  links.forEach(l => { if (l.source === n || l.target === n) l.heat = 1; });
  if (cam.follow && sp === focoSpider()) focus(n);
  setArea(n.area);
  if (!quiet) setTitle(n.area.toUpperCase(), (verb === "write" ? "escribiendo · " : verb === "search" ? "buscando · " : "leyendo · ") + (label || n.title));
  else setTitle(n.area.toUpperCase(), "nota · " + n.title + " · " + n.words + " palabras · " + (adj[n.id]||[]).length + " enlaces");
}

// cola por araña: cada una procesa sus eventos en orden y a su ritmo (antes todos compartían una línea de tiempo)
const COLA_MAX = 8;
function crawlTo(n, verb, label, quiet, q){
  if (!n) return;
  const sp = elegirArana(q);
  sp.cola.push({n, verb, label, quiet});
  if (sp.cola.length > COLA_MAX) sp.cola.splice(0, sp.cola.length - COLA_MAX);   // ráfaga: se queda con lo más reciente
  bombear(sp, performance.now());
}
function bombear(sp, now){   // arranca el siguiente viaje al llegar, o antes si la cola se acumula
  if (!sp.cola.length) return;
  if (!(sp.arrived || sp.cola.length > 3 || now - sp.born > 2600)) return;
  const e = sp.cola.shift(); _crawlTo(sp, e.n, e.verb, e.label, e.quiet);
}

// ---- movimiento: anticipación -> jalón ease-in-out -> llegada -> reposo ----
function _upd1(sp, now){
  const dtm = Math.min(100, Math.max(1, now - (sp.tu || now))); sp.tu = now;   // ms reales: igual a 60 y a 120 Hz
  const n = sp.node; if (!n) return;
  let mv = 0;
  if (now < sp.t0) { const k = clamp01((now - sp.born)/ANTICIPA), p = .04*k*k;
    sp.x = sp.from.x + (n.x - sp.from.x)*p; sp.y = sp.from.y + (n.y - sp.from.y)*p; sp.z = sp.from.z + (n.z - sp.from.z)*p; }
  else if (!sp.arrived) { const u = clamp01((now - sp.t0)/sp.dur), e = smooth(u); mv = Math.sin(u*Math.PI);
    sp.x = sp.from.x + (n.x - sp.from.x)*e; sp.y = sp.from.y + (n.y - sp.from.y)*e; sp.z = sp.from.z + (n.z - sp.from.z)*e;
    if (u >= 1) { sp.arrived = true; sp.settleAt = now + 2200; if (MAX_AGARRE > 1 && !sp.legs.some(L => !L.dying && L.gid === sp.gid && !L.main)) lanzar(sp, cercanas(n, 1), now, sp.gid, false); } }
  else { const k = 1 - Math.exp(-dtm*.0063); sp.x += (n.x - sp.x)*k; sp.y += (n.y - sp.y)*k; sp.z += (n.z - sp.z)*k; }
  sp.mv = mv;
  if (sp.arrived && sp.settleAt && now > sp.settleAt) { sp.settleAt = 0; // reposo: suelta los agarres
    sp.legs.forEach(L => { if (!L.dying && !L.release) L.release = now + Math.random()*500; }); }
  for (const L of sp.legs) if (!L.dying && L.release && now > L.release) L.dying = now;
  sp.legs = sp.legs.filter(L => !L.dying || now - L.dying < 700);
  // rastro fino
  if (now - sp.lastPt > 50) { sp.lastPt = now; const T = sp.trail, last = T[T.length - 1];
    if (!last || Math.hypot(sp.x - last.x, sp.y - last.y, sp.z - last.z) > 1.5) T.push({x: sp.x, y: sp.y, z: sp.z, t: now}); }
  if (now > sp.pruneAt) { sp.pruneAt = now + 500; sp.trail = sp.trail.filter(q => now - q.t < RASTRO_MS); }
}

function _trail1(sp, now){
  const ga = v => { cx.globalAlpha = v*sp.fade; };
  const T = sp.trail; if (T.length < 2) return;
  cx.globalCompositeOperation = "source-over"; cx.strokeStyle = sp.ci < 0 ? tc("rastro") : hexA(colorAr(sp), .6); cx.lineWidth = 1;
  let pts = [];
  const flush = a => { if (pts.length > 1) { ga(Math.min(.3, a*.3)); cx.beginPath(); pts.forEach((p, i) => i ? cx.lineTo(p.x, p.y) : cx.moveTo(p.x, p.y)); cx.stroke(); } };
  for (let i = 0; i < T.length; i++) { const p = proj(T[i].x, T[i].y, T[i].z);
    if (!p) { pts = []; continue; }
    pts.push(p);
    if (pts.length >= 24) { flush(Math.max(0, 1 - (now - T[i].t)/RASTRO_MS)); pts = [p]; } }
  flush(Math.max(0, 1 - (now - T[T.length - 1].t)/RASTRO_MS));
}

// ---- anatomía y marcha (pies fijos en el mundo, IK de 2 huesos) ----
// por pata (de adelante hacia atrás): a=posición del hombro en el cefalotórax (×u), f/l=reposo adelante/lateral, m=largo relativo
const PATAS = [{a: 4, f: 1, l: .55, m: 1.14}, {a: 2, f: .45, l: .9, m: 1}, {a: 0, f: -.3, l: .92, m: 1}, {a: -2, f: -.95, l: .62, m: 1.14}];
const grupo = i => ((i >> 2) + (i & 3)) % 2;   // A: L1,R2,L3,R4 = 0 ; B: R1,L2,R3,L4 = 1
const angDif = (a, b) => Math.atan2(Math.sin(a - b), Math.cos(a - b));

// IK analítica: cadera H, pie F, largos l1 (fémur) l2 (tibia); la rodilla sube y sale hacia afuera (lado sx,sy)
function ikPata(H, F, l1, l2, sx, sy){
  let dx = F.x - H.x, dy = F.y - H.y, D = Math.hypot(dx, dy) || 1, T = l1 + l2, hh;
  if (D >= T*.985) { const k = D/(T*.985); l1 *= k; l2 *= k; T = l1 + l2; hh = T*.05; }  // fuera de alcance: estira elástico
  else { const a0 = (l1*l1 - l2*l2 + D*D)/(2*D); hh = Math.sqrt(Math.max(0, l1*l1 - a0*a0)); }
  const a = (l1*l1 - l2*l2 + D*D)/(2*D), ux = dx/D, uy = dy/D;
  let px = -uy, py = ux; if (px*sx + py*(sy - .9) < 0) { px = -px; py = -py; }
  return {x: H.x + ux*a + px*hh, y: H.y + uy*a + py*hh};
}
// punto en pantalla (desplazamiento ox,oy respecto al cuerpo) -> posición del mundo en el plano de profundidad del cuerpo
function aMundo(sp, ox, oy, b){
  const f = FOV/(cam.dist + b.z), X = ox/f, Y = oy/f, cp = Math.cos(cam.pitch), spn = Math.sin(cam.pitch), cy = Math.cos(cam.yaw), sy = Math.sin(cam.yaw);
  const y = Y*cp, Z0 = -Y*spn;
  return {x: sp.x + X*cy + Z0*sy, y: sp.y + y, z: sp.z - X*sy + Z0*cy};
}
const pantalla = (w, node) => node ? (node._p || proj(node.x, node.y, node.z)) : proj(w.x, w.y, w.z);

// cuadrícula espacial de notas en pantalla (se rehace ~cada 120 ms)
let _gr = null, _grT = 0;
function cuadricula(now){
  if (_gr && now - _grT < 120) return _gr; _grT = now; const g = new Map();
  for (const n of nodes) { const p = n._p; if (!p) continue; const k = ((p.x/64)|0)*4099 + ((p.y/64)|0); (g.get(k) || g.set(k, []).get(k)).push(n); }
  return (_gr = g);
}
function notaCerca(x, y, r, ocupadas, now){
  const g = cuadricula(now), c0 = (x/64)|0, r0 = (y/64)|0, k = Math.ceil(r/64); let best = null, bd = r;
  for (let i = -k; i <= k; i++) for (let j = -k; j <= k; j++) { const lst = g.get((c0 + i)*4099 + r0 + j); if (!lst) continue;
    for (const n of lst) { if (ocupadas.has(n)) continue; const d = Math.hypot(n._p.x - x, n._p.y - y); if (d < bd) { bd = d; best = n; } } }
  return best;
}

function iniIK(){ return {feet: Array.from({length: 8}, () => ({w: null, node: null, step: null, err: 0})), h: -1.2, vx: 0, vy: 0, gait: 0, did: false,
  kick: 0, kdir: 1, px: null, py: null, tp: 0, lp: null}; }

// ---- dibujo: patas, cuerpo, etiquetas ----
function _draw1(sp, now){
  const ga = v => { cx.globalAlpha = v*sp.fade; };
  const n = sp.node; if (!n) return;
  const b = proj(sp.x, sp.y, sp.z); if (!b) return;
  const ik = sp.ik || (sp.ik = iniIK()), dt = Math.min(64, Math.max(1, now - (ik.tp || now))); ik.tp = now;
  const s = Math.max(.7, Math.min(2.2, b.s)), u = ESCALA_ARANA*s, L0 = LARGO_PATA*u;
  // velocidad en pantalla sin el movimiento de cámara
  if (ik.lp) { const p0 = proj(ik.lp.x, ik.lp.y, ik.lp.z), p1 = b; if (p0) { const k = Math.min(1, dt*.01);
    ik.vx += ((p1.x - p0.x)/dt - ik.vx)*k; ik.vy += ((p1.y - p0.y)/dt - ik.vy)*k; } }
  ik.lp = {x: sp.x, y: sp.y, z: sp.z};
  const vel = Math.hypot(ik.vx, ik.vy);
  if (vel > .03) ik.h += angDif(Math.atan2(ik.vy, ik.vx), ik.h)*Math.min(1, dt*.006);
  const fx = Math.cos(ik.h), fy = Math.sin(ik.h), rx = -fy, ry = fx;      // adelante y derecha (pantalla, y hacia abajo)
  ik.kick *= Math.exp(-dt/130);
  const breathe = 1 + .035*Math.sin(now/700);
  const bx = b.x + rx*ik.kick*ik.kdir*1.3*u, by = b.y + ry*ik.kick*ik.kdir*1.3*u;
  const hip = (i) => { const P = PATAS[i & 3], sd = (i >> 2) ? 1 : -1; return {x: bx + fx*P.a*u + rx*sd*3.4*u, y: by + fy*P.a*u + ry*sd*3.4*u, sd}; };
  const rest = i => { const P = PATAS[i & 3], h = hip(i), k = .75*P.m*L0, lead = Math.min(.3*L0, vel*T_PASO*1.6);
    return {x: h.x + (fx*P.f + rx*h.sd*P.l)*k + fx*lead, y: h.y + (fy*P.f + ry*h.sd*P.l)*k + fy*lead}; };
  // pasos
  const F = ik.feet, ocup = new Set(), stepping = [0, 0], needs = [false, false];
  for (const f of F) { if (f.node) ocup.add(f.node); if (f.step && f.step.to.node) ocup.add(f.step.to.node); }
  F.forEach((f, i) => { f.g = grupo(i); });
  stepping[0] = stepping[1] = 0; F.forEach(f => { if (f.step) stepping[f.g]++; });
  F.forEach((f, i) => { // pie inicial en el suelo virtual
    if (!f.w) { const r = rest(i); f.w = aMundo(sp, r.x - b.x, r.y - b.y, b); } });
  const thr = .3*L0;
  F.forEach((f, i) => { if (f.step) return; const p = pantalla(f.w, f.node), r = rest(i); f.err = p ? Math.hypot(p.x - r.x, p.y - r.y) : 0; if (f.err > thr) needs[f.g] = true; });
  if (!stepping[ik.gait] && needs[1 - ik.gait] && (ik.did || !needs[ik.gait])) { ik.gait ^= 1; ik.did = false; }
  const stepDur = Math.max(110, T_PASO/(1 + vel*5));
  F.forEach((f, i) => {
    const grab = (i & 3) === 0 && (sp.legs.some(L => L.side === (i >> 2) && L.ext > .05));
    if (f.step) { if (now >= f.step.t0 + f.step.dur) { f.w = f.step.to.w; f.node = f.step.to.node; f.step = null; } return; }
    if (grab || f.err <= thr || f.g !== ik.gait || stepping[1 - f.g]) return;
    const r = rest(i), nt = notaCerca(r.x, r.y, .4*L0, ocup, now), to = nt ? {w: {x: nt.x, y: nt.y, z: nt.z}, node: nt} : {w: aMundo(sp, r.x - b.x, r.y - b.y, b), node: null};
    if (nt) ocup.add(nt);
    f.step = {t0: now, dur: stepDur, from: {w: f.w, node: f.node}, to}; ik.did = true; ik.kick = 1; ik.kdir = f.g ? 1 : -1; stepping[f.g]++;
  });
  // agarres: cada pata delantera toma un agarre (el del lado más cercano a la nota)
  const act = sp.legs.filter(L => !L.dying && now >= L.born).slice(0, MAX_AGARRE), usado = [null, null];
  for (const L of sp.legs) { if (L.side < 0 && !L.dying) { const e = proj(L.m.x, L.m.y, L.m.z); if (e) L.side = ((e.x - bx)*rx + (e.y - by)*ry) >= 0 ? 1 : 0; } }
  for (const L of act) { let sd = L.side; if (sd < 0) continue; if (usado[sd]) sd = 1 - sd; if (usado[sd]) { L.skip = true; continue; } L.skip = false; L.side = sd; usado[sd] = L; }
  for (const L of sp.legs) { const goal = (!L.dying && usado[L.side] === L && now >= L.born) ? 1 : 0;
    L.ext += Math.max(-dt/(goal ? T_CRECE : T_CRECE*.6), Math.min(dt/(goal ? T_CRECE : T_CRECE*.6), goal - L.ext)); L._tip = null; }
  // dibujo
  cx.globalCompositeOperation = "source-over"; cx.lineCap = "round"; cx.lineJoin = "round";
  const cPat = tc("patas"), cCon = sp.ci < 0 ? tc("contorno") : colorAr(sp), cCue = tc("cuerpo");
  const tips = [];
  for (let i = 0; i < 8; i++) {
    const f = F[i], P = PATAS[i & 3], h = hip(i), tot = P.m*L0; let t;
    if (f.step) { const k = clamp01((now - f.step.t0)/f.step.dur), e = smooth(k), a = pantalla(f.step.from.w, f.step.from.node), c = pantalla(f.step.to.w, f.step.to.node);
      t = a && c ? {x: a.x + (c.x - a.x)*e, y: a.y + (c.y - a.y)*e - Math.sin(k*Math.PI)*ALTURA_PASO*u} : null; }
    else t = pantalla(f.w, f.node);
    if (!t) t = rest(i);
    let Lg = null;
    if ((i & 3) === 0) { Lg = sp.legs.find(L => L.side === (i >> 2) && L.ext > .01 && (usado[L.side] === L || !usado[L.side]));
      if (Lg) { const e = proj(Lg.m.x, Lg.m.y, Lg.m.z); if (e) { const w = smooth(clamp01(Lg.ext)); let tx = e.x, ty = e.y, d = Math.hypot(tx - h.x, ty - h.y);
        if (d > tot*1.7) { tx = h.x + (tx - h.x)*tot*1.7/d; ty = h.y + (ty - h.y)*tot*1.7/d; }
        t = {x: t.x + (tx - t.x)*w, y: t.y + (ty - t.y)*w}; Lg._tip = {x: t.x, y: t.y, ok: Lg.ext >= .98 && !Lg.dying}; } } }
    const kn = ikPata(h, t, .48*tot, .52*tot, rx*h.sd, ry*h.sd);
    cx.strokeStyle = cPat; cx.lineWidth = i % 4 === 0 || i % 4 === 3 ? 1.5 : 1.3; ga(.95);
    cx.beginPath(); cx.moveTo(h.x, h.y); cx.lineTo(kn.x, kn.y); cx.lineTo(t.x, t.y); cx.stroke();
    cx.fillStyle = cCon; cx.beginPath(); cx.arc(kn.x, kn.y, Math.max(1.6, 1.25*u), 0, 7); cx.fill();   // rodilla clara
    if (Lg) tips.push(Lg);
  }
  // cuerpo (marco: +x adelante)
  cx.save(); cx.translate(bx, by); cx.rotate(ik.h); ga(1); cx.fillStyle = cCue; cx.strokeStyle = cCon; cx.lineWidth = 1.3;
  cx.beginPath(); cx.moveTo(-1*u, 0); cx.lineTo(-7*u, 0); cx.stroke();                                    // pedicelo
  cx.save(); cx.translate(-12.5*u, 0); cx.rotate(ik.kick*ik.kdir*.07);                                      // abdomen
  cx.beginPath(); cx.ellipse(0, 0, 10.5*u*breathe, 8.2*u*breathe, 0, 0, 7); cx.fill(); cx.stroke();
  cx.strokeStyle = colorAr(sp); ga(.85); cx.lineWidth = 1.2; cx.beginPath(); cx.moveTo(-6*u, 0); cx.lineTo(5*u, 0); cx.stroke();   // acento solo como detalle
  for (let k = 0; k < 3; k++) { const x = (2.5 - k*3.6)*u; cx.beginPath(); cx.moveTo(x - 1.6*u, -3*u + k*.4*u); cx.lineTo(x, 0); cx.lineTo(x - 1.6*u, 3*u - k*.4*u); cx.stroke(); }
  cx.restore();
  ga(1); cx.lineWidth = 1.3;
  cx.beginPath(); cx.ellipse(0, 0, 6.6*u, 5.2*u, 0, 0, 7); cx.fill(); cx.stroke();                         // cefalotórax
  cx.strokeStyle = cPat; cx.lineWidth = 1.2; for (const sd of [-1, 1]) { cx.beginPath(); cx.moveTo(6*u, sd*1.6*u); cx.lineTo(9.5*u, sd*2.4*u); cx.lineTo(10.8*u, sd*1.2*u); cx.stroke(); } // pedipalpos
  cx.fillStyle = cCon; for (const sd of [-1, 1]) { cx.beginPath(); cx.arc(4.4*u, sd*1.7*u, Math.max(.8, .8*u), 0, 7); cx.fill(); }                  // ojos
  cx.restore();
  // etiquetas en las puntas de las patas que agarran
  cx.font = "11px " + FONT; cx.textAlign = "left";
  for (const L of tips) { const t = L._tip; if (!t || !t.ok) continue;
    const x = t.x + 7, y = t.y - 5, w = cx.measureText(L.tag).width + 10;
    ga(.95); cx.fillStyle = tc("etiquetaFondo"); cx.fillRect(x, y - 10, w, 15);
    cx.strokeStyle = (window.TEMA && window.TEMA.verbos && window.TEMA.verbos[sp.mode]) || colorAr(sp); cx.lineWidth = 1; cx.strokeRect(x + .5, y - 9.5, w - 1, 14);
    cx.fillStyle = tc("etiquetaTexto"); cx.fillText(L.tag, x + 5, y + 1); }
  if (sp.tag) { cx.font = "11px " + FONT; cx.textAlign = "center"; ga(.9); cx.fillStyle = colorAr(sp); cx.fillText(sp.tag, b.x, b.y - 20*u); cx.textAlign = "left"; }
  ga(1); cx.globalCompositeOperation = "lighter";
}

// envoltorios públicos (misma interfaz que usa mapa3d.js): recorren todas las arañas
function spiderUpdate(now){ gestionar(now); for (const sp of todas()) { bombear(sp, now); _upd1(sp, now); } }
function drawTrail(now){ for (const sp of todas()) _trail1(sp, now); }
function drawSpider(now){ for (const sp of todas()) _draw1(sp, now); cx.globalAlpha = 1; }
