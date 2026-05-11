# Multi Event System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add multiple player action events so the simulation tracks broader social consequences than assault alone.

**Architecture:** Replace the assault-only event flow with a generic `PlayerActionEvent` and `simulate_player_action`, while preserving `simulate_player_assault` as a wrapper. Keep CLI parsing thin and delegate behavior to the simulation layer.

**Tech Stack:** Python 3.9, pytest, dataclasses, standard library.

---

## Task 1: Tests First

- [ ] Add tests for `help`, `steal`, `threaten`, and `talk` simulation behavior.
- [ ] Add CLI tests for each new command.
- [ ] Run focused tests and confirm failures show missing commands/functions/fields.

## Task 2: Domain Model Updates

- [ ] Add `PlayerActionEvent`.
- [ ] Extend `CityReputation` with kindness, theft, and civilian trust fields.
- [ ] Keep `AssaultEvent` compatibility through aliasing or wrapper behavior.

## Task 3: Generic Simulation Flow

- [ ] Implement `simulate_player_action(simulation, action_kind, target_id)`.
- [ ] Refactor `simulate_player_assault` to call the generic function.
- [ ] Generalize perception memory summaries.
- [ ] Update decision rules for each event kind.
- [ ] Update reputation application per action.

## Task 4: CLI Expansion

- [ ] Add commands to help text.
- [ ] Route `help`, `steal`, `threaten`, and `talk` to the generic simulation flow.
- [ ] Update output text to use the action verb and event kind.

## Task 5: Verification and Git

- [ ] Run all tests.
- [ ] Run manual interactive command sequence.
- [ ] Commit and push to GitHub.
