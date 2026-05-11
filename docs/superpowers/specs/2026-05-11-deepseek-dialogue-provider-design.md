# DeepSeek Dialogue Provider Design

## Goal

Allow Neon Agency to use DeepSeek-generated NPC dialogue when a local API key is configured, while preserving deterministic template fallback.

## Scope

This phase adds configuration loading and a DeepSeek HTTP provider. It does not require the user to enter a key during runtime, and it does not commit secrets.

## Configuration

Configuration sources:

1. Environment variables.
2. Local `.env` file in the project root.

Supported keys:

- `DEEPSEEK_API_KEY`
- `DEEPSEEK_MODEL`, default `deepseek-v4-pro`
- `DEEPSEEK_BASE_URL`, default `https://api.deepseek.com`

`.env` must be ignored by git.

## Provider

`DeepSeekDialogueProvider` sends OpenAI-compatible `POST /chat/completions` requests using the standard library.

Request shape:

- `model`
- `messages`
- `temperature`
- `max_tokens`

Failure behavior:

- Provider errors bubble to `generate_dialogue`, which already falls back to templates.
- Blank output also falls back to templates.

## CLI Behavior

When interactive CLI starts:

- If DeepSeek config is present, use `DeepSeekDialogueProvider`.
- If no key is present, continue using template dialogue.

## Success Criteria

- `.env` is ignored.
- Config tests cover environment and `.env` loading.
- Provider tests cover request construction and response parsing without network calls.
- CLI can create a provider from config.
- All existing behavior works without a key.
