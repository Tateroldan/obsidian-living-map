---
type: index
area: ai
status: active
created: {{HOY}}
---
# Skills

Index of Claude's skills and agents and of the learnings that feed them. **It is only an index**: each skill lives in `~/.claude/skills/<name>/SKILL.md` and its content is not copied here.

> [!tip] Rule
> When a learning is born that touches the topic of a skill, it is added here on that skill's "Fed by" line and you check whether the skill needs updating. That is how the system improves on its own.

## System
### Agent: librarian
Keeps the vault tidy: processes the inbox, adds properties, creates and links learnings, finds broken links. File: `~/.claude/agents/librarian.md`.
- **Fed by:** [[How this vault works]] · [[Learnings]] · [[Routine work to a cheap model, hard work to the expensive one]]

### task-wrap-up
When a task ends: updates the project's "State for Claude", lists the assumptions and proposes the learning if something was reusable.
- **Fed by:** [[One learning, one idea, always linked]] · [[Ask what changes the outcome, don't guess]]

## Web development
### verify-web
Before saying "done" on a local web page, takes a screenshot and reads the console with headless Edge.
- **Fed by:** (add the web-error learnings you pick up here)

**Connects with:** [[Home]] · [[Learnings]] · [[Search learnings before giving an opinion]]
