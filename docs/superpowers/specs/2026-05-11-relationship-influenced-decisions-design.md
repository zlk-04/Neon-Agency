# Relationship Influenced Decisions Design

## Goal

Make NPC decisions respond to their personal relationship with the player, not only personality and event type.

## Scope

This phase changes deterministic decision rules. It does not add new player actions, LLM dialogue, or UI beyond the existing CLI output.

## Rules

Initial relationship-sensitive rules:

- High trust target under threat: `question` instead of immediately fleeing or calling police.
- High fear target under threat: `flee` without calling police.
- High resentment witness to a harmful event: `confront` instead of recording or calling police.
- High trust target in conversation: `warmly_greet` instead of `acknowledge`.
- High resentment theft target: `confront` instead of only calling police.

Thresholds:

- high trust: `trust >= 8`
- high fear: `fear >= 10`
- high resentment: `resentment >= 8`

## Success Criteria

- Existing default behavior remains unchanged for neutral relationships.
- Tests prove trust, fear, and resentment change reactions.
- CLI output naturally displays the new actions.
