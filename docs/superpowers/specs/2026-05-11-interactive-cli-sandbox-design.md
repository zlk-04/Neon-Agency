# Interactive CLI Sandbox Design

## Goal

Turn the fixed phase 1 demo into a small interactive command-line sandbox where a player can trigger assaults, inspect city status, inspect NPC memories, and ask for help.

## Scope

This phase stays text-only and local. It does not add new event types, persistence, LLM calls, or a graphical interface.

## Commands

- `help`: show available commands.
- `status`: show city reputation and known entities.
- `attack <entity_id>`: simulate the player attacking an NPC.
- `memories <entity_id>`: show that NPC's remembered events.
- `quit` or `exit`: leave the shell.

## Behavior

The CLI should parse one command at a time and return display text. Unknown commands should produce a helpful error instead of raising. Invalid entity ids should be reported cleanly.

## Architecture

Create `src/neon_agency/cli.py` for command parsing and display formatting. Keep `main.py` as the entrypoint. The simulation module remains responsible for world state changes.

## Success Criteria

- Tests cover `help`, `status`, `attack`, `memories`, unknown commands, and invalid targets.
- `python -m neon_agency.main` still runs through the installed package.
- The user can type commands manually in the terminal.
