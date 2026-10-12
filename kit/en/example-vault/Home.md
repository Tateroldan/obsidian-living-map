---
type: index
area: system
status: active
created: {{HOY}}
---
# Home

Entry point of the vault. Claude starts here: it opens this index and, from there, only the note of the project you are working on.

| Topic | Where |
|---|---|
| What was learned (linked notes) | [[Learnings]] |
| Claude skills and agents | [[Skills]] |
| How all of this works | [[How this vault works]] |
| What only you decide | [[Open decisions]] |
| Day-to-day tasks | [[Pending]] |
| Quick captures | `00 Inbox` · daily notes in `00 Daily` |

## Your projects
Add one row per project: its name, the link to its note and the full path of its code folder.
Every project note has a "State for Claude" section (template `State for Claude`).

## Rules to keep things apart
- Every new note goes in the folder of its topic. If you don't know where, leave it in `00 Inbox` and process it later.
- If two topics must never mix, write it in `reglas.json` (key `no_mezclar`): the validator warns on its own.
