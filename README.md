# Neon Agency

Neon Agency is an experimental agentic game-simulation prototype. The first milestone is a text-first street scene where NPCs perceive player actions, remember them, choose bounded reactions, and update city-level reputation.

## Phase 1

Phase 1 focuses on the social reaction loop:

1. Player action creates an event.
2. NPCs perceive the event.
3. NPCs store memories.
4. A deterministic decision engine selects allowed reactions.
5. The city reputation changes.

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
