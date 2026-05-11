# LLM Dialogue Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a provider-ready dialogue adapter while preserving deterministic template fallback.

**Architecture:** Keep dialogue generation in `dialogue.py`, add structured context and prompt construction, and allow `simulate_player_action` to accept an optional dialogue provider.

**Tech Stack:** Python 3.9, pytest, dataclasses, standard library.

---

## Task 1: Tests First

- [ ] Test prompt context includes event, relationship, reaction, and memories.
- [ ] Test fake provider output is used.
- [ ] Test blank provider output falls back to templates.
- [ ] Test provider exceptions fall back to templates.
- [ ] Test simulation can accept provider injection.

## Task 2: Dialogue Adapter

- [ ] Add `DialogueContext`.
- [ ] Add `build_dialogue_context`.
- [ ] Add `build_dialogue_prompt`.
- [ ] Update `generate_dialogue` to accept optional provider.
- [ ] Keep existing template behavior unchanged.

## Task 3: Simulation Integration

- [ ] Add optional `dialogue_provider` argument to `simulate_player_action`.
- [ ] Thread provider through `_attach_dialogue`.
- [ ] Keep `simulate_player_assault` compatible.

## Task 4: Verification and Git

- [ ] Run all tests.
- [ ] Run manual CLI sequence.
- [ ] Commit and push to GitHub.
