# Interactive CLI Sandbox Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an interactive command-line sandbox for running attacks and inspecting simulation state.

**Architecture:** Put command parsing and text formatting in `src/neon_agency/cli.py`. Keep `main.py` as a thin entrypoint and keep simulation state changes in `simulation.py`.

**Tech Stack:** Python 3.9, pytest, standard library.

---

## Task 1: Command Parsing Tests

- [ ] Add tests for `help`, `status`, `attack mira`, `memories mira`, invalid targets, and unknown commands.
- [ ] Run the focused tests and confirm they fail because `neon_agency.cli` does not exist.

## Task 2: CLI Implementation

- [ ] Add `src/neon_agency/cli.py`.
- [ ] Implement `handle_command(simulation, command)` returning command output text.
- [ ] Implement display helpers for simulation results, status, and memories.
- [ ] Run focused tests and confirm they pass.

## Task 3: Entrypoint Update

- [ ] Update `src/neon_agency/main.py` to start an input loop by default.
- [ ] Keep a non-interactive sample path for tests.
- [ ] Verify `python -m neon_agency.main --demo` works.

## Task 4: Verification and Git

- [ ] Run all tests.
- [ ] Run a manual CLI command sequence.
- [ ] Commit and push to GitHub.
