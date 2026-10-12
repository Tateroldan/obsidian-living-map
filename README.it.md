# Obsidian Living Map

[English](README.md) · [Español](README.es.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · Italiano · [日本語](README.ja.md) · [中文](README.zh.md)

Mappa 3D del tuo vault di Obsidian in cui un ragno cammina sulle note che Claude Code legge (ciano), scrive (ambra) o cerca (viola). Non consuma token: un hook `PostToolUse` registra ogni accesso in `events.jsonl` e la pagina lo interroga ogni 0,8 s. Solo libreria standard di Python, nessun `pip install`.

## Installazione

1. Clona il repository e apri `abrir.cmd` (oppure esegui `python server.py --abrir`). Si apre http://127.0.0.1:8765.
2. Se il tuo vault non è in `~/Documents/Boveda`, imposta `MAPA_BOVEDA` con il suo percorso. La porta si cambia con `MAPA_PUERTO` e la nota con caselle aperte con `MAPA_DECISIONES`. Tutto sta in `config.py`.
   Per `validar.py`, copia `reglas.ejemplo.json` in `reglas.json` e adatta tipi, aree e stati al tuo vault (`reglas.json` non viene committato).
3. Per vedere Claude muoversi, aggiungi l'hook a `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Read|Write|Edit|Grep|Glob|Bash|PowerShell",
        "hooks": [{ "type": "command", "command": "python \"PATH/obsidian-living-map/hook.py\"" }] }
    ]
  }
}
```

Opzionali: `validar.py` (PostToolUse `Write|Edit`; avvisa di proprietà mancanti, link rotti o segreti incollati) e `diario.py` (SessionEnd; riassume la sessione nella nota giornaliera).

La prima volta che lo apri da una console chiede, una sola volta, se avviarsi con Windows. Cambialo dopo con `python server.py --autoarranque on|off|estado`.

## Componenti

| File | A cosa serve |
|---|---|
| `reglas.ejemplo.json` | regole di `validar.py` (proprietà ammesse, mescolanze vietate) |
| `config.py` | percorso del vault, porta e log (unico posto con percorsi) |
| `server.py` | server locale; serve solo la pagina e i suoi pezzi, controlla `Host` |
| `hook.py` | PostToolUse → `events.jsonl` |
| `salud.py` | note orfane e mai toccate |
| `validar.py`, `vecinos.py`, `diario.py` | validare in scrittura, vicini/percorso/tema, nota giornaliera automatica |
| `mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js` | camera e grafo, ragno con IK, 6 palette, 8 lingue, pannelli |

Parametri URL: `?tema=rgb&lang=it`. Un clic su una nota la apre in Obsidian; doppio clic la mette a fuoco.

## Privacy

Tutto gira su `127.0.0.1`. `events.jsonl` contiene i percorsi delle tue note; è nel `.gitignore`.

## Supporto

Se ti è utile, puoi [offrirmi un caffè su Ko-fi](https://ko-fi.com/tateroldan) ☕

## Licenze di terzi

- d3 7.9.0 (ISC), `vendor/`
- Departure Mono v1.500 (SIL OFL), `fuentes/`

## Licenza

Apache-2.0, vedi `LICENSE`.
