# Template Dialogue Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add deterministic NPC dialogue lines to reaction output.

**Architecture:** Store dialogue on `Reaction`, generate it in a small `dialogue.py` module after decisions are made, and render it in CLI formatting.

**Tech Stack:** Python 3.9, pytest, dataclasses, standard library.

---

## Task 1: Tests First

- [ ] Add unit tests for dialogue generation.
- [ ] Add simulation tests proving reaction dialogue is present.
- [ ] Add CLI tests proving output includes `says`.
- [ ] Run focused tests and confirm failures.

## Task 2: Model and Generator

- [ ] Add `dialogue` field to `Reaction`.
- [ ] Create `src/neon_agency/dialogue.py`.
- [ ] Implement deterministic template lookup from action and relationship.

## Task 3: Simulation Integration

- [ ] Attach dialogue to reactions after decisions.
- [ ] Keep reactions immutable or replace with new `Reaction` instances.

## Task 4: CLI Rendering

- [ ] Print dialogue under each reaction if present.
- [ ] Preserve existing reaction text.

## Task 5: Verification and Git

- [ ] Run all tests.
- [ ] Run manual CLI sequence.
- [ ] Commit and push to GitHub.
