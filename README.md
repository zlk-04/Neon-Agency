# Neon Agency

Neon Agency is an experimental agentic game-simulation prototype. The first milestone is a text-first street scene where NPCs perceive player actions, remember them, choose bounded reactions, and update city-level reputation.

## Phase 1

Phase 1 focuses on the social reaction loop:

1. Player action creates an event.
2. NPCs perceive the event.
3. NPCs store memories.
4. A deterministic decision engine selects allowed reactions.
5. The city reputation changes.

Later phases add per-NPC relationships, relationship-influenced decisions, template dialogue, and an LLM-ready dialogue adapter with deterministic fallback.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Run Demo

```powershell
.\.venv\Scripts\python.exe -m neon_agency.main --demo
```

## Run Interactive Sandbox

```powershell
.\.venv\Scripts\python.exe -m neon_agency.main
```

## Run Local JSON API

```powershell
.\.venv\Scripts\python.exe -m neon_agency.server
```

Default address: `http://127.0.0.1:8765`

Endpoints:

```txt
GET /state
POST /action  {"action": "help", "target": "mira"}
POST /reset
```

The API uses the same simulation engine as the CLI. It keeps one in-memory city state until `/reset` is called or the process exits.

## DeepSeek Dialogue

Template dialogue works without any API key. To enable DeepSeek-generated NPC lines, create a local `.env` file:

```txt
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_MODEL=deepseek-v4-pro
```

`.env` is ignored by git and should not be committed.

Available commands:

```txt
help
status
attack <entity_id>
help <entity_id>
steal <entity_id>
threaten <entity_id>
talk <entity_id>
memories <entity_id>
relationship <entity_id>
relationships
quit
```
