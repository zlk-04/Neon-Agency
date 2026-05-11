# Template Dialogue Layer Design

## Goal

Add deterministic NPC dialogue lines that explain reactions using the current event, chosen action, and relationship state.

## Scope

This phase adds template dialogue only. It does not call LLM APIs, add persistence, or add branching conversations.

## Behavior

Each reaction can have a dialogue line:

- `thank`: gratitude after help.
- `question`: conflicted response when trust softens a threat response.
- `flee`: fear-driven response.
- `call_police`: lawful/reporting response.
- `confront`: resentment-driven response.
- `warmly_greet`: trusted social greeting.
- `acknowledge`: neutral social response.
- `record_video`: witness documentation response.
- `investigate`: police response.
- `approve`: witness approval after help.

Dialogue should be deterministic and testable.

## Architecture

Add `src/neon_agency/dialogue.py` with `generate_dialogue(entity, event, reaction)`. Add optional `dialogue` to `Reaction`. The simulation creates reactions first, then fills dialogue lines before returning `SimulationResult`.

## Success Criteria

- Tests cover direct dialogue generation for core actions.
- Simulation results include dialogue on reactions.
- CLI output prints `Name says: "..."` under reaction lines.
- Existing behavior remains deterministic.
