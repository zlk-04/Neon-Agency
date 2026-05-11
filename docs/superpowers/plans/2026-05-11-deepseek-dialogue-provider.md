# DeepSeek Dialogue Provider Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add DeepSeek API configuration and a provider implementation for NPC dialogue.

**Architecture:** Keep API code isolated in `providers/deepseek.py`, configuration in `config.py`, and CLI provider creation in `cli.py`.

**Tech Stack:** Python 3.9, pytest, urllib/request, json, os, pathlib.

---

## Task 1: Tests First

- [ ] Test `.env` parsing and environment override behavior.
- [ ] Test missing key returns no provider.
- [ ] Test DeepSeek provider builds OpenAI-compatible request.
- [ ] Test provider parses response text.
- [ ] Test CLI passes provider into simulation when configured.

## Task 2: Configuration

- [ ] Add `.env` to `.gitignore`.
- [ ] Add `src/neon_agency/config.py`.
- [ ] Implement `load_env_file` and `load_deepseek_config`.

## Task 3: Provider

- [ ] Add `src/neon_agency/providers/__init__.py`.
- [ ] Add `src/neon_agency/providers/deepseek.py`.
- [ ] Implement `DeepSeekDialogueProvider`.

## Task 4: CLI Integration

- [ ] Create provider at shell startup.
- [ ] Pass provider into `simulate_player_action`.
- [ ] Preserve templates when config is missing.

## Task 5: Verification and Git

- [ ] Run all tests.
- [ ] Run CLI without key and verify fallback.
- [ ] Commit and push.
