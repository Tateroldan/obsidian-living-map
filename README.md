# Obsidian Living Map

English · [Español](README.es.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [中文](README.zh.md)

3D map of your Obsidian vault where a spider walks the notes that Claude Code reads (cyan), writes (amber) or searches (violet). It costs no tokens: a `PostToolUse` hook logs every access to `events.jsonl` and the page polls it every 0.8 s. Python standard library only, no `pip install`.

## Install

1. Clone the repo and open `abrir.cmd` (or run `python server.py --abrir`). It opens http://127.0.0.1:8765.
2. If your vault is not at `~/Documents/Boveda`, set `MAPA_BOVEDA` to its path. Change the port with `MAPA_PUERTO` and the note with open checkboxes with `MAPA_DECISIONES`. Everything lives in `config.py`.
   For `validar.py`, copy `reglas.ejemplo.json` to `reglas.json` and adjust types, areas and states to your vault (`reglas.json` is not committed).
3. To watch Claude move, add the hook to `~/.claude/settings.json`:

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

Optional: `validar.py` (PostToolUse `Write|Edit`; warns about missing properties, broken links or pasted secrets) and `diario.py` (SessionEnd; summarizes the session in the daily note).

The first time you open it from a console it asks, once, whether to start automatically with Windows. Change it later with `python server.py --autoarranque on|off|estado`.

## Parts

| File | Purpose |
|---|---|
| `reglas.ejemplo.json` | rules for `validar.py` (allowed properties, forbidden mixes) |
| `config.py` | vault path, port and log (the only place with paths) |
| `server.py` | local server; serves only the page and its pieces, checks `Host` |
| `hook.py` | PostToolUse → `events.jsonl` |
| `salud.py` | orphan notes and never-touched notes |
| `validar.py`, `vecinos.py`, `diario.py` | validate on write, neighbors/path/topic, automatic daily note |
| `mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js` | camera and graph, spider with IK, 6 palettes, 8 languages, panels |

URL parameters: `?tema=rgb&lang=en`. Click a note to open it in Obsidian; double-click to focus it.

## Privacy

Everything runs on `127.0.0.1`. `events.jsonl` stores your note paths; it is in `.gitignore`.

## Kit (the self-learning part)

The map shows what Claude touches; `kit/` gives Claude the working method that makes the vault grow on its own: rules for starting and finishing tasks, linked notes ("neurons"), a librarian agent, a zero-token inbox router, a closing skill and a sample vault. No one's personal notes are included. Preview with `python kit/instalar.py --simulacro`. Details: [kit/LEEME.md](kit/LEEME.md).

## Support

If it is useful to you, you can [buy me a coffee on Ko-fi](https://ko-fi.com/tateroldan) ☕

## Third-party licenses

- d3 7.9.0 (ISC), `vendor/`
- Departure Mono v1.500 (SIL OFL), `fuentes/`

## License

Apache-2.0, see `LICENSE`.
