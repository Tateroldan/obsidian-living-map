---
name: verificar-web
description: Verifica una página web local (HTML/JS/CSS) con Edge headless - captura de pantalla y errores de consola - antes de decir "listo". Usar SIEMPRE que un agente cree o modifique una página web local, y al repartir trabajo web entre agentes en paralelo.
---

# Verificar página web local

## Cuándo
Siempre que crees o modifiques una página local (HTML/JS/CSS) y **antes de decir "listo"**.

## Captura + errores de consola (PowerShell)
```
$edge="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"; $d="<carpeta temporal o scratchpad>"; Start-Process -FilePath $edge -ArgumentList @("--headless=new","--user-data-dir=$d\edgeprof","--enable-logging=stderr","--v=0","--hide-scrollbars","--window-size=1280,800","--virtual-time-budget=12000","--screenshot=$d\cap.png","<URL>") -Wait -WindowStyle Hidden -RedirectStandardError "$d\con.txt"; Select-String -Path "$d\con.txt" -Pattern "Uncaught|Error:" | select -First 8
```
- `--user-data-dir` propio es obligatorio: sin él, un Edge ya abierto se roba el comando y no se genera la captura.
- `--virtual-time-budget` da tiempo a fetch y animaciones.
- Sintaxis de varios scripts globales a la vez: concaténalos en un archivo y pasa `node --check` (así saltan los identificadores duplicados entre archivos).

## Cuando hay que tocar la página (pestañas, pasos, botones, animaciones)
La captura simple no hace clics. Usa [cdp-capturas.mjs](cdp-capturas.mjs): `node cdp-capturas.mjs <carpeta> <url> 390 844` (Edge por DevTools Protocol, sin Playwright; edita solo el bloque PASOS). Permite clic por texto, scroll, captura a mitad de una animación y avisa de errores de consola y respuestas HTTP 5xx.
- Ya trae User-Agent de navegador real. Con `HeadlessChrome`/`curl` muchas apps se saltan la base de datos (contadores que ignoran bots) y ocultan un 500 que el navegador real sí da. Si pruebas con `curl`, usa `-A "Mozilla/5.0 (iPhone)"`.
- Si el proyecto tiene base de datos: tras agregar una migración, correrla en la base local antes de probar.

## Checklist
- [ ] Sin "Uncaught" en la consola ni respuestas 5xx.
- [ ] Si hay interacción (pasos, pestañas, animaciones): probada con clics y capturas con `cdp-capturas.mjs`, no solo la pantalla inicial.
- [ ] Sin textos crudos (claves i18n o `{placeholders}`).
- [ ] Se lee bien en tema claro y en oscuro.
- [ ] Probada en 12 anchos (280 a 2560) sin desbordes y mirada a 320, 390, 768, 1440 y 2560: método en [responsive.md](responsive.md). (`--window-size` no baja de ~500 px; no sirve para celular.)
- [ ] Menú móvil abierto una vez en celular.
- [ ] Probado el **build** (no solo el servidor de desarrollo) y `npm run check` completo si es Next/Vite.
- [ ] Leíste la captura con Read antes de entregar.

## Aprender de cada página
Antes de empezar una página web, busca con Grep en `Aprendizajes/` neuronas sobre errores web (por ejemplo `area: ia` o la palabra «web»). Al cerrar la tarea, si hubo un error nuevo, crea o amplía una neurona (error, arreglo, proyecto y fecha) y enlázala en `IA/Skills.md` bajo esta skill. Si el error es de verificación, mejora también esta skill.

## Agentes en paralelo
Antes de repartir, define un **contrato**: qué archivo es de quién y qué nombres globales se comparten. Al final, una prueba con todo junto (captura + consola + `node --check` concatenado).
