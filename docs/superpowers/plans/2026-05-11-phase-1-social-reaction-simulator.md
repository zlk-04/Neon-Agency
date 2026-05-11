# Phase 1 Social Reaction Simulator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python command-line prototype where NPCs perceive a player assault, remember it, choose bounded reactions, and update city reputation.

**Architecture:** Use a small pure-Python domain model with deterministic utility scoring. Keep the engine independent from the CLI so tests can verify behavior without shelling out.

**Tech Stack:** Python 3.9, pytest, dataclasses, standard library only for runtime.

---

## File Structure

- `requirements.txt`: development dependency list.
- `.gitignore`: excludes virtual environments, caches, and build artifacts.
- `README.md`: project overview and run instructions.
- `src/neon_agency/models.py`: entities, traits, memory, city reputation, and reaction records.
- `src/neon_agency/events.py`: event dataclasses.
- `src/neon_agency/rules.py`: allowed action filtering.
- `src/neon_agency/decision.py`: deterministic utility decisions.
- `src/neon_agency/perception.py`: decides which NPCs perceive an event and how.
- `src/neon_agency/simulation.py`: scene setup and orchestration.
- `src/neon_agency/main.py`: command-line demo entrypoint.
- `tests/test_simulation.py`: phase 1 behavior tests.

## Tasks

### Task 1: Project Scaffolding

- [x] Create virtual environment at `.venv`.
- [ ] Add `.gitignore`, `requirements.txt`, and `README.md`.
- [ ] Install pytest in `.venv`.

### Task 2: TDD Core Simulation Behavior

- [ ] Write failing tests for default scene assault reactions.
- [ ] Verify tests fail because package does not exist yet.
- [ ] Implement the smallest domain model and simulation code to pass.
- [ ] Run tests and keep them green.

### Task 3: CLI Demo

- [ ] Add `python -m neon_agency.main` demo output.
- [ ] Add test coverage for demo-level result formatting if needed.
- [ ] Run the demo through `.venv`.

### Task 4: GitHub Setup

- [ ] Initialize git repository.
- [ ] Commit phase 1 prototype.
- [ ] Add remote `https://github.com/zlk-04/Neon-Agency.git`.
- [ ] Push `main` to GitHub.
