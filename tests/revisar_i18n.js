// Revisa idioma.js (lo corre el CI con node): cada idioma tiene todas las claves y ninguna clave sobra.
// Uso: node tests/revisar_i18n.js   (desde la raíz del repo)
const fs = require("fs");
global.window = {};
global.localStorage = { getItem() { return null; }, setItem() {} };
global.location = { search: "" };
global.navigator = { language: "es" };
global.document = { documentElement: {}, querySelectorAll() { return []; }, dispatchEvent() {} };
global.CustomEvent = function () {};
eval(fs.readFileSync("idioma.js", "utf8"));

const claves = Object.keys(window.I18N.es);
const fuente = ["index.html", "mapa3d.js", "crawler.js", "tema.js", "paneles.js"].map(f => fs.readFileSync(f, "utf8")).join("\n");
const errores = [];
for (const [idioma, textos] of Object.entries(window.I18N)) {
  for (const k of claves) if (textos[k] == null || textos[k] === "") errores.push(`${idioma}: falta «${k}»`);
}
for (const k of claves) if (!new RegExp("[\"'`]" + k + "[\"'`]").test(fuente)) errores.push(`clave sin uso: «${k}»`);
if (errores.length) { console.error(errores.join("\n")); process.exit(1); }
console.log(`idiomas ok: ${Object.keys(window.I18N).length} idiomas, ${claves.length} claves`);
