// Plantilla: abre Edge headless, emula celular, hace clics y toma capturas + errores de consola. Sin Playwright.
// Uso:  node cdp-capturas.mjs <carpeta-salida> <url> [ancho=390] [alto=844]
// Edita solo el bloque PASOS. Lee después cada PNG con Read.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';

const [OUT, URL, W = 390, H = 844] = [process.argv[2], process.argv[3], Number(process.argv[4] || 390), Number(process.argv[5] || 844)];
mkdirSync(OUT, { recursive: true });
const edge = spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', [
  '--headless=new', '--remote-debugging-port=9333', `--user-data-dir=${OUT}/edgeprof`, '--hide-scrollbars', '--no-first-run',
  // User-Agent de navegador real: "HeadlessChrome" hace que muchas apps lo traten como bot y se salten la base de datos
  '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1',
  'about:blank',
], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let list;
for (let i = 0; i < 40; i++) { try { list = await (await fetch('http://127.0.0.1:9333/json')).json(); if (list.length) break; } catch {} await sleep(250); }
const ws = new WebSocket(list.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0; const pending = new Map(); const errors = [];
ws.onmessage = (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pending.has(d.id)) { pending.get(d.id)(d.result ?? d.error); pending.delete(d.id); }
  if (d.method === 'Runtime.exceptionThrown') errors.push(d.params.exceptionDetails.exception?.description ?? d.params.exceptionDetails.text);
  if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') errors.push(d.params.args.map((a) => a.value ?? a.description).join(' '));
  if (d.method === 'Network.responseReceived' && d.params.response.status >= 500) errors.push(`HTTP ${d.params.response.status} ${d.params.response.url}`);
};
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = (expression) => send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
const shot = async (name) => { const r = await send('Page.captureScreenshot', { format: 'png' }); writeFileSync(`${OUT}/${name}.png`, Buffer.from(r.data, 'base64')); };
const clickText = (t, sel = 'button,a,[role=tab]') => ev(`[...document.querySelectorAll('${sel}')].find(b=>b.textContent.includes(${JSON.stringify(t)})).click()`);

await send('Runtime.enable'); await send('Page.enable'); await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: W < 700 });
await send('Page.navigate', { url: URL });
await sleep(4000);

// ---------- PASOS (ejemplo) ----------
await shot('1-inicio');
// await clickText('Siguiente'); await sleep(350); await shot('2-transicion');   // captura A MITAD de una animación
// await ev(`document.querySelector('#seccion').scrollIntoView({block:'center'})`);
// -------------------------------------

console.log('errores:', JSON.stringify(errors.slice(0, 8)));
ws.close(); edge.kill();
process.exit(0);
