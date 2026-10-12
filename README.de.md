# Obsidian Living Map

[English](README.md) · [Español](README.es.md) · [Português](README.pt.md) · [Français](README.fr.md) · Deutsch · [Italiano](README.it.md) · [日本語](README.ja.md) · [中文](README.zh.md)

3D-Karte deines Obsidian-Vaults, auf der eine Spinne über die Notizen läuft, die Claude Code liest (Cyan), schreibt (Bernstein) oder durchsucht (Violett). Sie kostet keine Tokens: Ein `PostToolUse`-Hook protokolliert jeden Zugriff in `events.jsonl`, und die Seite fragt ihn alle 0,8 s ab. Nur die Python-Standardbibliothek, kein `pip install`.

## Installation

1. Klone das Repo und öffne `abrir.cmd` (oder starte `python server.py --abrir`). Es öffnet http://127.0.0.1:8765.
2. Liegt dein Vault nicht unter `~/Documents/Boveda`, setze `MAPA_BOVEDA` auf seinen Pfad. Den Port änderst du mit `MAPA_PUERTO`, die Notiz mit offenen Kästchen mit `MAPA_DECISIONES`. Alles steht in `config.py`.
   Für `validar.py` kopiere `reglas.ejemplo.json` nach `reglas.json` und passe Typen, Bereiche und Status an deinen Vault an (`reglas.json` wird nicht eingecheckt).
3. Damit du Claude beim Laufen siehst, füge den Hook in `~/.claude/settings.json` ein:

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

Optional: `validar.py` (PostToolUse `Write|Edit`; warnt vor fehlenden Eigenschaften, kaputten Links oder eingefügten Geheimnissen) und `diario.py` (SessionEnd; fasst die Sitzung in der Tagesnotiz zusammen).

Beim ersten Start aus einer Konsole wird einmalig gefragt, ob der Server mit Windows starten soll. Später änderbar mit `python server.py --autoarranque on|off|estado`.

## Bestandteile

| Datei | Zweck |
|---|---|
| `reglas.ejemplo.json` | Regeln für `validar.py` (erlaubte Eigenschaften, verbotene Mischungen) |
| `config.py` | Vault-Pfad, Port und Log (einziger Ort mit Pfaden) |
| `server.py` | lokaler Server; liefert nur die Seite und ihre Teile, prüft `Host` |
| `hook.py` | PostToolUse → `events.jsonl` |
| `salud.py` | verwaiste und nie berührte Notizen |
| `validar.py`, `vecinos.py`, `diario.py` | beim Schreiben validieren, Nachbarn/Pfad/Thema, automatische Tagesnotiz |
| `mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js` | Kamera und Graph, Spinne mit IK, 6 Paletten, 8 Sprachen, Panels |

URL-Parameter: `?tema=rgb&lang=de`. Klick auf eine Notiz öffnet sie in Obsidian; Doppelklick fokussiert sie.

## Datenschutz

Alles läuft auf `127.0.0.1`. `events.jsonl` speichert die Pfade deiner Notizen; sie steht in `.gitignore`.

## Unterstützung

Wenn es dir nützt, kannst du mir [auf Ko-fi einen Kaffee spendieren](https://ko-fi.com/tateroldan) ☕

## Lizenzen Dritter

- d3 7.9.0 (ISC), `vendor/`
- Departure Mono v1.500 (SIL OFL), `fuentes/`

## Lizenz

Apache-2.0, siehe `LICENSE`.
