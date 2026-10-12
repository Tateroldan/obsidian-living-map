---
name: verify-web
description: Verifies a local web page (HTML/JS/CSS) with headless Edge - screenshot and console errors - before saying "done". Use ALWAYS when an agent creates or modifies a local web page, and when splitting web work among parallel agents.
---

# Verify a local web page

## When
Whenever you create or modify a local page (HTML/JS/CSS) and **before saying "done"**.

## Screenshot + console errors (PowerShell)
```
$edge="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"; $d="<temp or scratchpad folder>"; Start-Process -FilePath $edge -ArgumentList @("--headless=new","--user-data-dir=$d\edgeprof","--enable-logging=stderr","--v=0","--hide-scrollbars","--window-size=1280,800","--virtual-time-budget=12000","--screenshot=$d\cap.png","<URL>") -Wait -WindowStyle Hidden -RedirectStandardError "$d\con.txt"; Select-String -Path "$d\con.txt" -Pattern "Uncaught|Error:" | select -First 8
```
- Your own `--user-data-dir` is required: without it, an Edge that is already open steals the command and no screenshot is produced.
- `--virtual-time-budget` gives fetch and animations time to finish.
- For several global scripts at once: concatenate them into one file and pass `node --check` (that is how duplicate identifiers across files show up).

## When the page has to be touched (tabs, steps, buttons, animations)
A plain screenshot doesn't click. Use [cdp-capturas.mjs](cdp-capturas.mjs): `node cdp-capturas.mjs <folder> <url> 390 844` (Edge over the DevTools Protocol, no Playwright; edit only the STEPS block). It allows click-by-text, scrolling, capture mid-animation and reports console errors and HTTP 5xx responses.
- It already sends a real browser User-Agent. With `HeadlessChrome`/`curl` many apps skip the database (counters that ignore bots) and hide a 500 that a real browser would get. If you test with `curl`, use `-A "Mozilla/5.0 (iPhone)"`.
- If the project has a database: after adding a migration, run it on the local database before testing.

## Checklist
- [ ] No "Uncaught" in the console and no 5xx responses.
- [ ] If there is interaction (steps, tabs, animations): tested with clicks and screenshots using `cdp-capturas.mjs`, not just the first screen.
- [ ] No raw text (i18n keys or `{placeholders}`).
- [ ] Reads well in light and dark themes.
- [ ] Tested at 12 widths (280 to 2560) with no overflow and looked at 320, 390, 768, 1440 and 2560: method in [responsive.md](responsive.md). (`--window-size` doesn't go below ~500 px; it is no good for phones.)
- [ ] Mobile menu opened once on a phone width.
- [ ] Tested the **build** (not just the dev server) and the full `npm run check` if it is Next/Vite.
- [ ] You looked at the screenshot with Read before delivering.

## Learn from every page
Before starting a web page, search `Learnings/` with Grep for notes about web errors (for example `area: ai` or the word "web"). When closing the task, if there was a new error, create or extend a learning (error, fix, project and date) and link it in `AI/Skills.md` under this skill. If the error is about verification, improve this skill too.

## Parallel agents
Before splitting the work, define a **contract**: which file belongs to whom and which global names are shared. At the end, one test with everything together (screenshot + console + concatenated `node --check`).
