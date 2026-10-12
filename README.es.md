# Obsidian Living Map

[English](README.md) · Español · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [中文](README.zh.md)

Mapa 3D de tu bóveda de Obsidian donde una araña camina por las notas que Claude Code lee (cian), escribe (ámbar) o busca (violeta). No gasta tokens: un hook `PostToolUse` anota cada acceso en `events.jsonl` y la página lo consulta cada 0.8 s. Solo Python estándar, sin `pip install`.

## Instalar

1. Clona el repo y abre `abrir.cmd` (o `python server.py --abrir`). Se abre http://127.0.0.1:8765.
2. Si tu bóveda no está en `~/Documents/Boveda`, define `MAPA_BOVEDA` con su ruta. El puerto se cambia con `MAPA_PUERTO` y la nota de casillas abiertas con `MAPA_DECISIONES`. Todo vive en `config.py`.
   Para `validar.py`, copia `reglas.ejemplo.json` a `reglas.json` y ajusta tipos, áreas y estados a tu bóveda (`reglas.json` no se sube).
3. Para ver a Claude moverse, agrega el hook a `~/.claude/settings.json`:

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

Opcionales: `validar.py` (PostToolUse `Write|Edit`; avisa de propiedades faltantes, enlaces rotos o secretos pegados) y `diario.py` (SessionEnd; resume la sesión en la nota diaria).

## Piezas

| Archivo | Para qué |
|---|---|
| `reglas.ejemplo.json` | reglas de `validar.py` (propiedades permitidas, mezclas prohibidas) |
| `config.py` | ruta de la bóveda, puerto y log (único lugar con rutas) |
| `server.py` | servidor local; solo sirve la página y sus piezas, revisa `Host` |
| `hook.py` | PostToolUse → `events.jsonl` |
| `salud.py` | huérfanas y notas nunca tocadas |
| `validar.py`, `vecinos.py`, `diario.py` | validar al escribir, vecinos/camino/tema, diario automático |
| `mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js` | cámara y grafo, araña con IK, 6 paletas, 8 idiomas, paneles |

Parámetros de URL: `?tema=rgb&lang=en`. Clic en una nota la abre en Obsidian; doble clic la enfoca.

## Privacidad

Todo corre en `127.0.0.1`. `events.jsonl` guarda rutas de tus notas; está en `.gitignore`.

## Licencias de terceros

- d3 7.9.0 (ISC), `vendor/`
- Departure Mono v1.500 (SIL OFL), `fuentes/`

## Licencia

Apache-2.0, ver `LICENSE`.
