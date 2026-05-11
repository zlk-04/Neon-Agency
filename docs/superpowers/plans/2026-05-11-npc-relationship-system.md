# NPC Relationship System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-NPC trust, fear, resentment, and familiarity toward the player.

**Architecture:** Store relationship state on each `Entity`, update it during `simulate_player_action` from event kind and perception, and expose it through CLI formatting helpers.

**Tech Stack:** Python 3.9, pytest, dataclasses, standard library.

---

## Task 1: Tests First

- [ ] Add simulation tests for relationship changes after help, assault, steal, threaten, and talk.
- [ ] Add CLI tests for `relationship <entity_id>` and `relationships`.
- [ ] Run focused tests and confirm failures show missing relationship state or commands.

## Task 2: Relationship Model

- [ ] Add `Relationship` dataclass to `models.py`.
- [ ] Add `relationship_to_player` field to `Entity` using `default_factory=Relationship`.
- [ ] Preserve the older numeric field behavior only if tests require it; otherwise replace it.

## Task 3: Relationship Updates

- [ ] Add relationship delta table in `simulation.py`.
- [ ] Apply deltas after perceptions are computed.
- [ ] Keep target and witness updates distinct.
- [ ] Exclude the player entity.

## Task 4: CLI Inspection

- [ ] Add `relationship <entity_id>`.
- [ ] Add `relationships`.
- [ ] Update help text and README.

## Task 5: Verification and Git

- [ ] Run all tests.
- [ ] Run manual CLI sequence.
- [ ] Commit and push to GitHub.
