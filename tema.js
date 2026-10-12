// Temas del mapa vivo. window.TEMAS = {id: {...}}, window.TEMA = activo, aplicarTema(id).
(function(){
  const ar = (cuerpo, contorno, patas, acento, rastro, ef, et) => ({cuerpo, contorno, patas, acento, rastro, etiquetaFondo: ef, etiquetaTexto: et});
  window.TEMAS = {
    okabe: { nombre: "Okabe-Ito", alerta: "#D55E00", claro: false, vineta: 0, grano: 0,
      fondo: "#0e0f11", panel: "#141518", linea: "#26282d", texto: "#d8d9dc", textoTenue: "#7c7f86",
      acento: "#9B6DFF", nodo: "#b4b7bd", arista: "#8a8d94",
      areas: ["#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7","#999999"],
      verbos: {read: "#56B4E9", write: "#9B6DFF", search: "#CC79A7"},
      arana: ar("#1a1d23", "#d8d9dc", "#8f939b", "#9B6DFF", "#8a8d94", "#141518", "#d8d9dc") },
    magma: { nombre: "Magma", alerta: "#e75263", claro: false, vineta: 0, grano: 0,
      fondo: "#0b0a10", panel: "#121018", linea: "#26212f", texto: "#e4dde6", textoTenue: "#80768a",
      acento: "#9B6DFF", nodo: "#b9aebf", arista: "#8b7f94",
      areas: ["#fcfdbf","#fec287","#fb8861","#e75263","#b73779","#8c2981","#fe9f6d","#f1605d"],
      verbos: {read: "#fec287", write: "#e75263", search: "#b73779"},
      arana: ar("#1b1722", "#e4dde6", "#8b7f94", "#9B6DFF", "#8b7f94", "#121018", "#e4dde6") },
    "mono-oscuro": { nombre: "Mono oscuro", alerta: "#ff4d4d", claro: false, vineta: 0, grano: 0,
      fondo: "#000000", panel: "#0a0a0a", linea: "#222222", texto: "#ededed", textoTenue: "#808080",
      acento: "#9B6DFF", nodo: "#a1a1a1", arista: "#6b6b6b",
      areas: ["#ededed","#c7c7c7","#a1a1a1","#8a8a8a","#737373","#5e5e5e","#4d4d4d","#d9d9d9"],
      verbos: {read: "#a1a1a1", write: "#ededed", search: "#9B6DFF"},
      aranas: ["#56B4E9","#E69F00","#009E73","#CC79A7","#D55E00","#F0E442"], // en mono las áreas son grises: las arañas llevan color propio
      arana: ar("#161616", "#ededed", "#808080", "#9B6DFF", "#6b6b6b", "#0a0a0a", "#ededed") },
    "mono-claro": { nombre: "Mono claro", alerta: "#d92d20", claro: true, vineta: 0, grano: 0,
      fondo: "#fafafa", panel: "#ffffff", linea: "#e1e1e1", texto: "#111111", textoTenue: "#6b6b6b",
      acento: "#6E3FE0", nodo: "#555555", arista: "#bdbdbd",
      areas: ["#111111","#333333","#525252","#6e6e6e","#8a8a8a","#a3a3a3","#404040","#7a7a7a"],
      verbos: {read: "#6b6b6b", write: "#111111", search: "#6E3FE0"},
      aranas: ["#0072B2","#B36B00","#007A5A","#B8427D","#C24E00","#5B4BD6"],
      arana: ar("#2a2a2a", "#8a8a8a", "#6b6b6b", "#6E3FE0", "#6b6b6b", "#ffffff", "#111111") },
    cine: { nombre: "Cine", alerta: "#c0452f", claro: false, vineta: .55, grano: .05,
      fondo: "#0a0d10", panel: "#0f1417", linea: "#1e282b", texto: "#cdd5d2", textoTenue: "#6f7f80",
      acento: "#9B6DFF", nodo: "#9fb0ad", arista: "#5f7475",
      areas: ["#d9822b","#4f8a8b","#b5683a","#7da39a","#8a6f4e","#3f6c78","#c4a574","#6a8f7a"],
      verbos: {read: "#4f8a8b", write: "#9B6DFF", search: "#c4a574"},
      arana: ar("#141b1f", "#cdd5d2", "#7f9391", "#9B6DFF", "#5f7475", "#0f1417", "#cdd5d2") },
    // RGB: neón sobre negro; con ciclo:true los colores de área y el acento giran de tono (cicloRGB)
    rgb: { nombre: "RGB", alerta: "#FF1744", claro: false, vineta: .3, grano: 0, ciclo: true,
      fondo: "#050507", panel: "#0b0b10", linea: "#1f1f2b", texto: "#f2f2f7", textoTenue: "#8a8aa0",
      acento: "#00E5FF", nodo: "#c8c8d8", arista: "#7a7aa0",
      areas: ["#FF1744","#FF9100","#FFEA00","#00E676","#00E5FF","#2979FF","#D500F9","#FF4081"],
      verbos: {read: "#00E5FF", write: "#FF2D95", search: "#B4FF39"},
      arana: ar("#0b0b10", "#f2f2f7", "#9a9ab5", "#00E5FF", "#7a7aa0", "#0b0b10", "#f2f2f7") }
  };
  const orden = Object.keys(window.TEMAS);
  const rgb = h => [1,3,5].map(i => parseInt(h.slice(i, i+2), 16));
  window.TEMA = window.TEMAS[orden[0]]; window.TEMA.id = orden[0];
  window.aplicarTema = function(id){
    if (!window.TEMAS[id]) id = orden[0];
    const T = window.TEMAS[id]; T.id = id; window.TEMA = T;
    const r = document.documentElement.style;
    r.setProperty("--fondo", T.fondo); r.setProperty("--panel", T.panel); r.setProperty("--linea", T.linea);
    r.setProperty("--texto", T.texto); r.setProperty("--tenue", T.textoTenue); r.setProperty("--acento", T.acento);
    r.setProperty("--nodo", T.nodo); r.setProperty("--arista", T.arista);
    r.setProperty("--v-read", T.verbos.read); r.setProperty("--v-write", T.verbos.write); r.setProperty("--v-search", T.verbos.search);
    r.setProperty("--alerta", T.alerta || "#D55E00"); r.setProperty("--vineta", T.vineta); r.setProperty("--grano", T.grano);
    r.setProperty("--fondo-rgb", rgb(T.fondo).join(","));
    document.documentElement.dataset.tema = id;
    try { localStorage.setItem("mapavivo.tema", id); } catch (_) {}
    document.dispatchEvent(new CustomEvent("tema", {detail: id}));
  };
  window.TEMAS_ORDEN = orden;
  // tono (0-360) a hex: el resto del código espera colores #rrggbb
  const hsl = (h, s, l) => { const a = s*Math.min(l, 1 - l), f = n => { const k = (n + h/30) % 12; return Math.round(255*(l - a*Math.max(-1, Math.min(k - 3, 9 - k, 1)))).toString(16).padStart(2, "0"); }; return "#" + f(0) + f(8) + f(4); };
  let ultCiclo = 0;
  window.cicloRGB = function(now){ // lo llama el bucle de dibujo; una vuelta completa cada 30 s
    const T = window.TEMA; if (!T.ciclo || now - ultCiclo < 40) return; ultCiclo = now;
    const h0 = now*.012;
    for (let i = 0; i < T.areas.length; i++) T.areas[i] = hsl((h0 + i*360/T.areas.length) % 360, 1, .58);
    T.acento = T.arana.acento = hsl((h0 + 190) % 360, 1, .62);
    document.documentElement.style.setProperty("--acento", T.acento);
  };
  let g = null; try { g = localStorage.getItem("mapavivo.tema"); } catch (_) {}
  try { const q = new URLSearchParams(location.search).get("tema"); if (q) g = q; } catch (_) {}
  const arrancar = () => window.aplicarTema(g && window.TEMAS[g] ? g : orden[0]);
  if (document.documentElement) arrancar();
})();

