# Codex Session Handoff Skill

A conversation-centered handoff skill for moving a long or degraded Codex task to a fresh task without losing why the session began, what the user asked, how Codex responded, where the work stalled, or what remains unresolved.

The skill creates a fresh Codex task when thread-management capabilities are available, sends the complete handoff inline, saves a temporary Markdown backup, and asks the destination task to restate its understanding before continuing.

## Install

Place the files in a user-level Codex skill directory with this layout:

```text
handoff/
├── SKILL.md
└── agents/
    └── openai.yaml
```

For a standard Codex setup, the resulting paths are:

```text
~/.codex/skills/handoff/SKILL.md
~/.codex/skills/handoff/agents/openai.yaml
```

Restart Codex only if the skill does not appear automatically.

## Use

Invoke it explicitly with `$handoff`, or ask naturally, for example:

- `Move this conversation to a new task without losing context.`
- `Hand this work off to a fresh Codex task.`
- `別セッションに移して`
- `この会話を引き継いで新しいタスクにして`

The handoff output follows the language of the source conversation.

## Design focus

- Preserve the user-agent conversation and changes of intent.
- Keep important obstacles, dead ends, constraints, and unresolved questions.
- Avoid duplicating code diffs or information recoverable from the workspace.
- Redact secrets and unnecessary personal data.
- Leave the source task intact.
- Do not use a transcript-preserving fork, which would carry the bloated history forward.

## License

MIT License. See `LICENSE`.
