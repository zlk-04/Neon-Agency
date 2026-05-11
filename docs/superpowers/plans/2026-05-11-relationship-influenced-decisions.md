# Relationship Influenced Decisions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Use per-NPC relationship state as an input to deterministic NPC reaction choices.

**Architecture:** Keep relationship updates in `simulation.py`, but read `entity.relationship_to_player` in `decision.py` when selecting actions. Add new bounded actions to `rules.py`.

**Tech Stack:** Python 3.9, pytest, dataclasses, standard library.

---

## Task 1: Tests First

- [ ] Add tests proving neutral behavior still works.
- [ ] Add tests for high trust under threat choosing `question`.
- [ ] Add tests for high fear under threat choosing `flee`.
- [ ] Add tests for high resentment witness choosing `confront`.
- [ ] Add tests for high trust conversation choosing `warmly_greet`.
- [ ] Run focused tests and confirm they fail.

## Task 2: Decision Rules

- [ ] Add relationship threshold constants in `decision.py`.
- [ ] Update target threat decision to consider fear and trust before personality.
- [ ] Update theft target decision to consider resentment.
- [ ] Update witness decision to consider resentment for harmful events.
- [ ] Update talk target decision to consider trust.

## Task 3: Action Rules

- [ ] Add `question` and `warmly_greet` to allowed base actions.
- [ ] Keep all actions filtered through `rules.py`.

## Task 4: Verification and Git

- [ ] Run all tests.
- [ ] Run manual CLI sequence showing relationship-influenced output.
- [ ] Commit and push to GitHub.
