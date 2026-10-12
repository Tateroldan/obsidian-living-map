# Neural-set kit

The living map shows what Claude touches; this kit gives Claude **the working method** that makes the vault grow on its own: rules for starting and finishing every task, linked notes ("neurons"), an agent that tidies up and a router that sorts the inbox without spending tokens. It contains nobody's personal notes: everything is generic and adapts through `reglas.json`.

Spanish version: [LEEME.md](LEEME.md).

## What is included

| Piece | Where | What it does |
|---|---|---|
| Rules for Claude | `en/claude/CLAUDE.template.md` | When starting (open `Home`, search learnings), when finishing (state, assumptions, learning) and way of working |
| Example vault | `en/example-vault/` | Folders, guide, templates, 4 sample learnings, skills index |
| Agent | `en/claude/agents/librarian.md` | Processes the inbox, adds properties, creates and links learnings (cheap model) |
| Skill `task-wrap-up` | `en/claude/skills/task-wrap-up/` | Automates the "when finishing" routine: state, assumptions, learning |
| Skill `verify-web` | `en/claude/skills/verify-web/` | Screenshot and console with headless Edge before saying "done" |
| Inbox router | `router_bandeja.py` | Sorts by keywords, no tokens; moves only the safe ones |
| Installer | `instalar.py` | Copies everything without overwriting and asks before touching your `CLAUDE.md` |

## Install

```
python kit/instalar.py --lang en --simulacro   # see what it would do, writes nothing
python kit/instalar.py --lang en               # step by step, asks before each group
```

- The example vault is created at `MAPA_BOVEDA` (or `~/Documents/Boveda`). If the folder already has notes, only the missing files are added.
- The `CLAUDE.md` block is shown and you are **always** asked; a `.bak` copy is saved first.
- Hooks are not edited automatically: the installer prints the lines for `settings.json`.
- `--lang en` also copies `reglas.ejemplo.en.json` to `reglas.json` (English property names, folders and messages: `type/area/status/created`, `00 Inbox`, `Learnings`...).

## How it grows on its own

1. Claude opens `Home.md` and searches the learnings on the topic before giving an opinion.
2. When done, `task-wrap-up` updates the project state and creates a learning if something was reusable.
3. `validar.py` checks every note as it is written (properties, links, secrets).
4. The router and the librarian process the inbox; the living map lets you watch it all, and the spider weaves each new note into the network.

## What it does NOT include

Domain skills (video, games, marketing…): everyone creates their own with `find-skills` or by hand and lists them in `AI/Skills.md`. The example learnings are only a guide: replace them with yours.
