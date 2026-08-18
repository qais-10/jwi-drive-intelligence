# JWI Claude Memory

These five files are JWI's global Claude Code memory: operating rules, brand soul, visual design system, voice, and audience. They're meant to live at `~/.claude/` so Claude Code reads them automatically at the start of every session, not just inside this repo.

This folder is the durable backup. Claude Code Remote sessions run in ephemeral containers that get reclaimed, so anything saved only to a container's `~/.claude/` disappears when the container does. Committing copies here means they survive regardless of session lifecycle.

## Files
- `CLAUDE.md` — operating rules, and when to read each file below
- `soul.md` — origin story, beliefs, philosophy
- `design.md` — brand colors, typography, layout patterns
- `voice.md` — tone, word rules, sentence structure, platform rules
- `audience.md` — who JWI is reaching, the problem solved, real sourced language

## To use these on a machine
Copy all five into `~/.claude/`:

```
cp claude-memory/*.md ~/.claude/
```

Claude Code picks up `~/.claude/CLAUDE.md` automatically from there, and the other four get read on demand per the rules inside `CLAUDE.md`.

## Keeping this in sync
When any of the five files change, update both `~/.claude/` and this folder, then commit. This folder is the source of truth across sessions, `~/.claude/` in any single container is not.
