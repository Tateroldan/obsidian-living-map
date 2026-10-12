---
type: learning
area: ai
status: active
created: {{HOY}}
---
# Routine work to a cheap model, hard work to the expensive one

Sorting notes, searching, adding properties and processing the inbox don't need the best model: delegate them to the `librarian` agent (cheap model). Keep the expensive model for deciding, designing and reviewing. Before spending tokens, a rules script (`router_bandeja.py`) resolves the obvious ones with no model at all.

**How to apply it:** escalation order: script → cheap model → expensive model → you. Anything that mixes forbidden topics goes straight to you.

**Connects with:** [[Skills]] · [[Ask what changes the outcome, don't guess]]
