# LLM Dialogue Adapter Design

## Goal

Prepare the dialogue layer for LLM-generated NPC lines without adding a network dependency or requiring an API key.

## Scope

This phase adds a provider interface, context builder, prompt builder, and fallback behavior. It does not call a real model API yet.

## Architecture

`dialogue.py` owns:

- `DialogueContext`: structured NPC, event, reaction, relationship, and memory information.
- `build_dialogue_context(entity, event, reaction)`: converts simulation objects into a compact context.
- `build_dialogue_prompt(context)`: creates deterministic instructions for an external dialogue model.
- `generate_dialogue(entity, event, reaction, provider=None)`: uses a provider when supplied, otherwise uses templates.

Provider contract:

```python
class Provider:
    def generate(self, prompt: str) -> str:
        ...
```

If a provider raises an exception or returns blank text, dialogue falls back to templates.

## Success Criteria

- Prompt construction is testable and includes event, action, relationship, and recent memory data.
- A fake provider can generate dialogue in tests.
- Blank or failing providers safely fall back to template dialogue.
- Existing CLI behavior still works without configuration.
