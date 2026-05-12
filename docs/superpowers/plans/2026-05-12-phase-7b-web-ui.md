# Phase 7B Web UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a minimal same-origin browser UI for the local Neon Agency JSON API.

**Architecture:** Serve one static HTML file from `src/neon_agency/web/index.html` through the existing `http.server` adapter. The page uses vanilla HTML/CSS/JS and calls existing `/state`, `/action`, and `/reset` endpoints; simulation logic stays in `simulation.py` and API serialization stays in `api.py`.

**Tech Stack:** Python standard library `http.server`, package data via `importlib.resources`, vanilla browser JavaScript, pytest.

---

### Task 1: Serve the web shell

**Files:**
- Create: `src/neon_agency/web/index.html`
- Create: `src/neon_agency/web/__init__.py`
- Modify: `src/neon_agency/server.py`
- Test: `tests/test_server.py`

- [ ] **Step 1: Write the failing server test**

```python
from neon_agency.server import NeonAgencyServer, create_handler


def test_root_serves_web_ui_html():
    html = NeonAgencyServer().index_html()

    assert "Neon Agency Control Deck" in html
    assert "fetch('/state')" in html
    assert "data-action=\"help\"" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_server.py::test_root_serves_web_ui_html -q`
Expected: FAIL because `index_html` does not exist.

- [ ] **Step 3: Implement minimal HTML loading**

Use `importlib.resources.files("neon_agency.web").joinpath("index.html").read_text(encoding="utf-8")` inside `NeonAgencyServer.index_html()`.

- [ ] **Step 4: Serve `/` and `/index.html`**

Add a `_send_html` helper to the request handler. `GET /` and `GET /index.html` return the loaded page with `Content-Type: text/html; charset=utf-8`.

- [ ] **Step 5: Run targeted test**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_server.py -q`
Expected: PASS.

### Task 2: Build the static UI

**Files:**
- Modify: `src/neon_agency/web/index.html`
- Test: `tests/test_server.py`

- [ ] **Step 1: Write HTML content assertions**

Assert the page contains sections for reputation, NPC cards, action buttons, reactions log, reset button, and API status.

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_server.py -q`
Expected: FAIL until the HTML includes the required UI hooks.

- [ ] **Step 3: Implement vanilla UI**

Use one HTML file with embedded CSS and JS. JS flow:
1. `loadState()` fetches `/state` and renders city reputation plus NPC cards.
2. Action buttons post `{ action, target }` to `/action`.
3. Responses render `event`, `reactions`, `dialogue`, `dialogue_source`, and updated state.
4. Reset button posts `/reset`, clears the log, and renders the returned state.
5. Errors render a readable status message.

- [ ] **Step 4: Run targeted test**

Run: `.\.venv\Scripts\python.exe -m pytest tests/test_server.py -q`
Expected: PASS.

### Task 3: Documentation and verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Document browser usage**

Mention that `http://127.0.0.1:8765/` opens the browser UI and `/state`, `/action`, `/reset` remain JSON endpoints.

- [ ] **Step 2: Run all tests**

Run: `.\.venv\Scripts\python.exe -m pytest -q`
Expected: all tests pass.

- [ ] **Step 3: Commit and push**

```powershell
git add README.md src/neon_agency/server.py src/neon_agency/web tests/test_server.py docs/superpowers/plans/2026-05-12-phase-7b-web-ui.md
git commit -m "feat: add local web ui"
git push
```
