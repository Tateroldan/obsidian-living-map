---
type: guide
area: system
status: active
created: {{HOY}}
---
# How this vault works

Guide for you and for Claude. If something new doesn't fit here, adjust this note.

> [!info] Neural set
> That is the name of the whole system: the notes in `Learnings` linked to each other with **Connects with:**, plus the Claude skills and agents that feed on them (index in [[Skills]]). Every task adds notes and the next one takes advantage of them.

## The 3 layers
1. **Folders = kind of place** (few, never more than 2 levels): `00 Inbox` (quick captures) · `00 Daily` · areas (`Work`, `Personal`, `Projects`, `Ideas`, `AI`) · `Learnings` (the notes that capture lessons) · `99 Archive` (finished things; never deleted) · `Attachments` (images) · `_System` (this guide).
2. **Properties = what the note is** (every note has them):
   - `type`: learning · prompt · project · plan · guide · script · index · daily
   - `area`: work · personal · projects · ideas · ai · system
   - `status`: active · idea · done · superseded · archived
   - `created`: YYYY-MM-DD
3. **Links = what it is about** (`[[...]]`): every note links to at least one other; learnings end with **Connects with:**.

The allowed values live in `reglas.json` (copy of `reglas.ejemplo.en.json`, with `"idioma": "en"`). If you change the lists above, change them there too.

## Flow
- **Capture:** anything quick goes to `00 Inbox` or to the daily note.
- **Process (once a week):** `"{{PY}}" "{{REPO}}/kit/router_bandeja.py"` (no tokens, dry run first) and the ambiguous ones go to the **librarian** agent.
- **Find:** the search box, the graph view and the living map.
- **Close:** finished things change to `status: done`; old things go to `99 Archive`. Nothing is deleted.
- **Health:** `python salud.py` writes a report of orphan notes and never-touched notes.

## Rules
- Learnings: never overwrite; if something changes, write a new note with "supersedes [[...]]" and mark the old one `status: superseded`.
- Templates (Ctrl+P → "Insert template"): `Learning`, `Prompt`, `Project`, `Daily`, `State for Claude`.
- Helpers: the **librarian** agent (tell Claude "hand it to the librarian") and the skills in [[Skills]].
- **Confidence (optional):** on learnings from an untested source, add `confidence: verified | inferred | unverified`.

## For Claude (read before writing here)
- Create notes with the 4 properties; pick `type`/`area` from the lists above.
- Before answering about a topic, look for existing learnings (Grep in `Learnings/` or by `area:`).
- Short notes with one idea; link instead of repeating.

**Connects with:** [[Home]] · [[Learnings]] · [[Skills]]
