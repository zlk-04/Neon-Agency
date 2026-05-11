# NPC Relationship System Design

## Goal

Add per-NPC attitudes toward the player so social consequences are personal, not only city-wide.

## Scope

This phase adds relationship state and CLI inspection. It does not yet make relationships change decision outcomes; that is the next phase.

## Relationship Fields

Each NPC tracks:

- `trust`: belief that the player is safe or helpful.
- `fear`: belief that the player is dangerous.
- `resentment`: personal grievance against the player.
- `familiarity`: how much the NPC has interacted with or observed the player.

## Relationship Effects

Action impact:

- `help` target: trust +8, familiarity +2.
- `help` witness: trust +2, familiarity +1.
- `assault` target: fear +8, resentment +6, familiarity +2.
- `assault` witness: fear +3, resentment +1, familiarity +1.
- `steal` target: resentment +8, fear +2, familiarity +2.
- `steal` witness: resentment +2, familiarity +1.
- `threaten` target: fear +7, resentment +4, familiarity +2.
- `threaten` witness: fear +2, familiarity +1.
- `talk` target: familiarity +3, trust +1.
- `talk` witness: familiarity +1.

## CLI

Add commands:

- `relationship <entity_id>`: show one NPC's attitude toward the player.
- `relationships`: show all NPC relationship summaries.

## Success Criteria

- Each NPC has relationship state.
- Player actions update target and witness relationships differently.
- CLI can inspect one NPC or all NPC relationships.
- Existing simulation and CLI behavior remains compatible.
