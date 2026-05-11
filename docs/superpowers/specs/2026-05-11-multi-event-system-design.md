# Multi Event System Design

## Goal

Expand Neon Agency from a single assault simulation into a small player-behavior social consequence simulator.

## Scope

This phase adds more text-only player actions. It does not add LLM calls, persistence, inventory, combat resolution, or a graphical interface.

## Player Actions

- `attack <entity_id>`: violent action. Keeps existing assault behavior.
- `help <entity_id>`: kind action. Target appreciates the player; witnesses approve.
- `steal <entity_id>`: theft action. Target reports theft; witnesses record or call police.
- `threaten <entity_id>`: intimidation action. Target backs away or calls police based on lawfulness.
- `talk <entity_id>`: social action. Target acknowledges the player; witnesses ignore it.

## Reputation

Extend city reputation with:

- `player_violence_score`
- `player_kindness_score`
- `player_theft_score`
- `police_attention`
- `civilian_trust`

## Architecture

Create a generic `PlayerActionEvent` with a `kind` field. `simulate_player_action` becomes the main orchestration function. Existing `simulate_player_assault` remains as a compatibility wrapper for tests and older code.

Perception remains simple:

- target receives `target`
- direct witnesses receive `witnessed`
- police at the same location receive `heard` for harmful events

Decision logic chooses bounded reactions according to event kind, perception, role, and personality.

## Success Criteria

- CLI supports `attack`, `help`, `steal`, `threaten`, and `talk`.
- NPC memories record each event kind.
- Reputation changes differently for each action type.
- Existing assault tests remain valid.
- All new behavior is covered by tests.
