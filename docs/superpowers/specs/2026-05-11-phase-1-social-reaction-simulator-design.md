# Phase 1 Social Reaction Simulator Design

## Goal

Build the first Neon Agency prototype as a Python command-line simulation where NPCs perceive player actions, remember important events, choose bounded reactions, and update city-level reputation.

## Scope

Phase 1 is intentionally text-first. It does not include 3D rendering, animation, pathfinding, networking, or LLM calls. The goal is to prove the agentic social loop before attaching it to a game engine.

## Core Loop

1. A player action creates a world event.
2. Nearby entities perceive the event according to their role and relationship to the target.
3. Each NPC stores a memory of the event.
4. A decision engine scores allowed actions from personality, role, relationship, and context.
5. A rules layer filters impossible or unsupported actions.
6. The simulation records chosen reactions and updates city reputation.

## Entities

Entities have an id, display name, role, personality traits, relationship to the player, location, optional police status, and memory list.

Initial roles:

- `player`
- `civilian`
- `police`

Initial personality traits:

- `bravery`
- `aggression`
- `lawfulness`

## Events

The first supported event is `AssaultEvent`, created when the player attacks an NPC.

An assault event includes:

- actor id
- target id
- location
- severity
- direct witnesses

## Decisions

The first supported reaction actions are:

- `flee`
- `call_police`
- `fight_back`
- `record_video`
- `investigate`
- `ignore`

The decision engine must be deterministic for tests. It can use utility scoring rather than random choice.

## Command-Line Demo

Running `python -m neon_agency.main` starts a small street scene and executes a sample player attack. The output should show the event, each NPC reaction, and city reputation changes.

## Success Criteria

- The simulation can create a default street scene.
- Attacking a cautious civilian causes that target to flee and call police.
- An aggressive witness records or confronts instead of doing nothing.
- A police officer investigates an assault disturbance.
- NPCs remember the event.
- City reputation reflects player violence and police attention.
- The behavior is covered by automated tests.
