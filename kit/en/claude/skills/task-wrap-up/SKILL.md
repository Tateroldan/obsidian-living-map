---
name: task-wrap-up
description: Wraps up a task in the Obsidian vault - updates the project's "State for Claude", lists the assumptions made and proposes or creates the learning if something was reusable. Use when finishing any task that touched a project or produced a lesson, before giving the final answer.
---

# Task wrap-up

Do it without being asked, at the end of every task. It should take a minute, not a session.

## Steps
1. **State for Claude.** Open the project note (from `Home.md`) and update its "State for Claude" section (≤10 lines): date, where we left off, next step, key files. If alternatives were discarded, add "Discarded and why" with one line each.
2. **Learning.** Ask yourself: did we learn something that would help in another project? If so, search `Learnings/` with Grep for a similar one. If it exists, link to it or create one that extends it; if not, create a new one with the `Learning` template (one idea, 3-6 lines, ends with **Connects with:**). Never overwrite: new note with "supersedes [[...]]".
3. **Skills index.** If the learning touches the topic of a skill, add it to its "Fed by" line in `AI/Skills.md` and say whether the skill should be updated.
4. **Learnings index.** Add the learning to `Learnings.md` under its topic.
5. **Assumptions.** End the answer with a short list of what you decided without asking. If there were none, omit it.

## Rules
- Don't invent lessons: if nothing was reusable, don't create a learning.
- One idea per learning; link instead of repeating.
- Check with the living map: the new learning must link to another note (`validar.py` warns if not).
