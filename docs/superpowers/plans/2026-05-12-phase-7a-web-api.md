# Phase 7A Web API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development while implementing. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a local JSON API around the existing Neon Agency simulation without adding third-party dependencies.

**Architecture:** Keep simulation logic unchanged. `api.py` owns pure request/state serialization functions that are easy to test. `server.py` adapts `http.server` requests to those pure functions and keeps one in-memory simulation instance.

**Tech Stack:** Python standard library, `http.server`, existing `neon_agency.simulation`, pytest.

---

### Task 1: Pure API serialization and action handling

**Files:**
- Create: `tests/test_api.py`
- Create: `src/neon_agency/api.py`

- [ ] Write failing tests for `serialize_state`, `handle_action_request`, and error responses.
- [ ] Run targeted tests with `.\.venv\Scripts\python.exe -m pytest tests/test_api.py -q` and confirm they fail because `neon_agency.api` is missing.
- [ ] Implement serialization helpers for reputation, entities, relationships, memories, events, and reactions.
- [ ] Implement JSON-like result helpers with HTTP-style `status` and `body` fields.
- [ ] Ensure invalid actions and invalid targets return structured `400` errors without mutating simulation.
- [ ] Run targeted tests until green.

### Task 2: HTTP server adapter

**Files:**
- Create: `src/neon_agency/server.py`
- Modify: `README.md`

- [ ] Implement `GET /state`, `POST /action`, and `POST /reset` with Python `http.server`.
- [ ] Keep a single simulation in memory and reset it via `create_default_street()`.
- [ ] Parse JSON request bodies safely and return `application/json` responses.
- [ ] Add a startup entrypoint for `.\.venv\Scripts\python.exe -m neon_agency.server` on `127.0.0.1:8765`.
- [ ] Document API usage briefly in `README.md`.

### Task 3: Verification and release

**Files:**
- Verify all changed files.

- [ ] Run `.\.venv\Scripts\python.exe -m pytest -q`.
- [ ] Inspect `git diff` and ensure no secrets or `.env` contents are printed/committed.
- [ ] Commit with `feat: add local json api`.
- [ ] Push to GitHub.
