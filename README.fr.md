# Obsidian Living Map

[English](README.md) · [Español](README.es.md) · [Português](README.pt.md) · Français · [Deutsch](README.de.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [中文](README.zh.md)

Carte 3D de votre coffre Obsidian où une araignée parcourt les notes que Claude Code lit (cyan), écrit (ambre) ou recherche (violet). Elle ne consomme aucun token : un hook `PostToolUse` consigne chaque accès dans `events.jsonl` et la page l'interroge toutes les 0,8 s. Bibliothèque standard Python uniquement, sans `pip install`.

## Installation

1. Clonez le dépôt et ouvrez `abrir.cmd` (ou lancez `python server.py --abrir`). Cela ouvre http://127.0.0.1:8765.
2. Si votre coffre n'est pas dans `~/Documents/Boveda`, définissez `MAPA_BOVEDA` avec son chemin. Le port se change avec `MAPA_PUERTO` et la note de cases ouvertes avec `MAPA_DECISIONES`. Tout se trouve dans `config.py`.
   Pour `validar.py`, copiez `reglas.ejemplo.json` en `reglas.json` et adaptez types, zones et états à votre coffre (`reglas.json` n'est pas versionné).
3. Pour voir Claude se déplacer, ajoutez le hook à `~/.claude/settings.json` :

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

Optionnels : `validar.py` (PostToolUse `Write|Edit` ; signale propriétés manquantes, liens cassés ou secrets collés) et `diario.py` (SessionEnd ; résume la session dans la note du jour).

La première fois que vous l'ouvrez depuis une console, il demande une seule fois s'il doit démarrer avec Windows. Modifiez-le ensuite avec `python server.py --autoarranque on|off|estado`.

## Composants

| Fichier | Rôle |
|---|---|
| `reglas.ejemplo.json` | règles de `validar.py` (propriétés autorisées, mélanges interdits) |
| `config.py` | chemin du coffre, port et journal (seul endroit avec des chemins) |
| `server.py` | serveur local ; ne sert que la page et ses pièces, vérifie `Host` |
| `hook.py` | PostToolUse → `events.jsonl` |
| `salud.py` | notes orphelines et jamais touchées |
| `validar.py`, `vecinos.py`, `diario.py` | valider à l'écriture, voisins/chemin/thème, note du jour automatique |
| `mapa3d.js`, `crawler.js`, `tema.js`, `idioma.js`, `paneles.js` | caméra et graphe, araignée à cinématique inverse, 6 palettes, 8 langues, panneaux |

Paramètres d'URL : `?tema=rgb&lang=fr`. Un clic sur une note l'ouvre dans Obsidian ; un double-clic la met au point.

## Confidentialité

Tout tourne sur `127.0.0.1`. `events.jsonl` contient les chemins de vos notes ; il est dans `.gitignore`.

## Licences tierces

- d3 7.9.0 (ISC), `vendor/`
- Departure Mono v1.500 (SIL OFL), `fuentes/`

## Licence

Apache-2.0, voir `LICENSE`.
