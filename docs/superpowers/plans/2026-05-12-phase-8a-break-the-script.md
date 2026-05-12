# Phase 8A Break the Script Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let NPC behavior optionally come from an LLM-generated structured intent while keeping deterministic decisions as a safe fallback.

**Architecture:** Add `agent_policy.py` as the boundary between free-form model output and executable simulation actions. The LLM returns JSON with `action`, `target_id`, `reason`, and `dialogue`; `agent_policy.py` validates it against a small allowed action registry and converts it into the existing `Reaction` model. `simulation.py` accepts an optional `decision_provider`; when absent or invalid, the existing `decision.py` rules remain unchanged.

**Tech Stack:** Python stdlib `json`, existing dataclasses, pytest, current DeepSeek-compatible provider interface.

---

### Task 1: Agent policy parser and fallback

**Files:**
- Create: `src/neon_agency/agent_policy.py`
- Create: `tests/test_agent_policy.py`

- [ ] **Step 1: Write failing tests for valid intent JSON**

Test that a provider response like `{"action":"warn_player","target_id":"player","reason":"Mira is worried.","dialogue":"Be careful around Chen."}` becomes a `Reaction` with `actions=("warn_player",)`, custom reason, and dialogue source `deepseek`.

- [ ] **Step 2: Write failing tests for invalid output fallback**

Cover non-JSON text, unknown action such as `teleport`, empty action, and provider exceptions. Each should return the deterministic fallback reaction and mark dialogue as template/fallback-safe.

- [ ] **Step 3: Implement minimal policy module**

Define:
- `ALLOWED_AGENT_ACTIONS`
- `build_decision_prompt(entity, event, perception)`
- `decide_agent_reaction(entity, event, perception, provider=None, fallback_decider=decide_reaction)`
- helper JSON parsing and validation.

- [ ] **Step 4: Run targeted tests**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_agent_policy.py -q`
Expected: PASS.

### Task 2: Simulation integration

**Files:**
- Modify: `src/neon_agency/simulation.py`
- Modify: `src/neon_agency/api.py`
- Modify: `src/neon_agency/server.py`
- Test: `tests/test_simulation.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: Write failing simulation test**

Call `simulate_player_action(..., decision_provider=Provider())` and assert Mira/Rook can use provider-selected actions such as `warn_player` while existing behavior remains unchanged when no provider is passed.

- [ ] **Step 2: Implement optional `decision_provider`**

Thread `decision_provider` through `simulate_player_action`, API handler, and server state. Keep `dialogue_provider` separate for now.

- [ ] **Step 3: Preserve old tests**

Existing tests should pass unchanged when no decision provider is passed.

- [ ] **Step 4: Run targeted tests**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_agent_policy.py tests/test_simulation.py tests/test_api.py -q`
Expected: PASS.

### Task 3: Documentation and verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Document Break the Script**

Explain that NPC behavior can now optionally be proposed by an LLM as structured intent, but the world kernel validates actions and falls back to deterministic rules.

- [ ] **Step 2: Run all tests**

Run: `.\.venv\Scripts\python.exe -m pytest -q`
Expected: all tests pass.

- [ ] **Step 3: Commit and push**

```powershell
git add README.md src/neon_agency/agent_policy.py src/neon_agency/simulation.py src/neon_agency/api.py src/neon_agency/server.py tests/test_agent_policy.py tests/test_simulation.py tests/test_api.py docs/superpowers/plans/2026-05-12-phase-8a-break-the-script.md
git commit -m "feat: add llm npc intent policy"
git push
```
