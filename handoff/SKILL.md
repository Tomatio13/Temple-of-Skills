---
name: handoff
description: Create a conversation-centered handoff from a long or degraded Codex task to a fresh task, preserving why the session began, what the user asked, how Codex responded, changes in direction, obstacles, unresolved work, and user preferences. Use when the user asks to hand off, transfer, continue in a new session/task/thread, start fresh without losing context, or says the conversation has become too long, slow, confused, or degraded; also match equivalent natural-language requests such as "move this to a new task", "引き継いで", "別セッションに移して", or "この会話を新しくして".
---

# Session Handoff

Move the current conversation to a fresh Codex task without losing its human intent or history. Create the new task directly when thread-management capabilities are available, and always keep a temporary Markdown backup.

## Operating principles

- Preserve the conversation, not a substitute code review. Explain why the task exists, what the user asked, what Codex did, what changed, where work stalled, and what remains unresolved.
- Match the language of the current conversation. Use generic forms of address; do not introduce project-specific personas, honorifics, or relationship labels unless they are materially part of the task.
- Optimize for context retention rather than a fixed length. Use as much space as needed to preserve important phases and causal links, while merging repetition and omitting noise.
- Prefer durable references over duplication. Point to plans, issues, ADRs, commits, diffs, files, or URLs instead of reproducing their contents.
- Mention code or repository state only when it explains the conversation or the current obstacle. Do not produce a file-by-file change summary that the next task can recover from the workspace.
- Summarize observable actions, decisions, outcomes, and stated rationale. Never expose hidden reasoning or chain-of-thought.
- Redact secrets, credentials, tokens, cookies, private keys, and unnecessary personal data.
- Do not archive, delete, compact, or otherwise mutate the source task.

## Workflow

### 1. Establish the handoff scope

- Infer the destination focus from the user's request and the current task. Do not interrupt the handoff with questions unless a missing choice would materially change which work is being transferred.
- Treat a clear natural-language request to move or continue the conversation as authorization to create the destination task.
- If the user only remarks that the task feels slow or long without asking to move it, recommend the handoff but do not silently create a task.

### 2. Recover the conversation history

- Start from the current model-visible conversation.
- When the task has been compacted or the original purpose and major pivots are uncertain, search for available thread-reading capabilities and inspect the source task's turn summaries selectively. Read older pages only until the origin, major user requests, important changes of direction, and unresolved obstacles are recovered.
- Check the live workspace, task state, or running processes only when necessary to verify a claim about what Codex did or why progress stopped.
- Mark uncertainty explicitly. Never reconstruct missing history as fact.

### 3. Write the handoff

Use the following structure, omitting only sections that are genuinely irrelevant:

```markdown
# Handoff: <short description of the continuing work>

## Why this task exists
<The user's original need, situation, and intended outcome.>

## Conversation trajectory
### <Phase or turning point>
- User: <request, correction, concern, or decision>
- Codex: <observable response, action, or decision>
- Outcome: <what changed or what was learned>

## Current understanding and focus
<What the task is now trying to accomplish and why.>

## Friction, dead ends, and discoveries
- <Obstacle or failed approach, whether it is resolved, and what should not be repeated.>

## User constraints and preferences
- <Only constraints or preferences established by the conversation. Mark inferences as inferences.>

## Open questions and pending work
- <Unresolved question, pending decision, blocker, or incomplete objective.>

## Relevant artifacts
- `<path or URL>` - <why the next task may need it>

## First response required from the new task
Restate:
1. why the task exists;
2. the current understanding and focus;
3. the unresolved points;
4. the proposed next action.

Do not use tools, edit files, or continue the work yet. Wait for the user to confirm or correct this understanding.
```

For the trajectory:

- Organize by meaningful phases or turning points, not by every message.
- Retain user corrections and changes of mind because they define the real intent.
- Retain completed work only to explain what the user asked and how Codex responded.
- Record failed approaches when omitting them could cause the next task to repeat the same mistake.
- Omit greetings, acknowledgements, raw logs, repetitive tool output, and generic repository explanations.

### 4. Save a temporary backup

- Save the complete handoff as Markdown in the host operating system's temporary directory, using a unique timestamped or generated filename.
- Do not save it inside the repository unless the user explicitly asks for a durable project artifact.
- If the temporary write fails, keep the complete handoff in the current response and continue with direct delivery when possible.

### 5. Create the fresh task

- Search for Codex thread-management capabilities before choosing a fallback.
- Prefer creating a genuinely new task and placing the full handoff in its initial prompt. Do not use a transcript-preserving fork for this workflow because it carries the bloated history into the destination.
- Keep the destination on the same project and usable source workspace when the host supports it. Do not create or switch Git branches, commit changes, or manufacture a new worktree solely for the handoff.
- Include the handoff inline in the initial prompt; do not rely only on the temporary file path, which may be inaccessible from another host or worktree.
- Instruct the destination task to produce only the required understanding response and then wait. It must not call tools or start implementation before the user replies.
- Give the destination a concise continuation title when title management is available.
- Verify that task creation and handoff delivery succeeded. Emit any created-task directive required by the host only after success.

If direct creation is unavailable or fails:

- Do not claim that a new task was created.
- Return the temporary file path and the complete copyable handoff.
- Give one concise instruction for starting a fresh task with that handoff.

### 6. Close out the source task

- Report the destination task and temporary backup path briefly.
- Do not repeat the full handoff in the source task after successful direct delivery.
- Leave the source task intact as a recoverable record.
