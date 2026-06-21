---
type: Reference
title: LM Studio as MCP Host
description: Running LM Studio as an MCP host that calls external tools via ephemeral or mcp.json servers.
tags: [lmstudio, mcp, tool-calling, rest-api]
source: https://lmstudio.ai/docs/developer/core/mcp
timestamp: 2026-06-21
---

# LM Studio as MCP Host

LM Studio (v0.4.0+) can act as an MCP **host**: a loaded model can call tools exposed by external MCP servers, wired in through LM Studio's REST API. Two server styles exist:

- **Ephemeral servers** — declared per-request, no pre-config. Requires the "Allow per-request MCPs" setting. An `integrations` entry of `"type": "ephemeral_mcp"` carries `server_label`, `server_url`, optional `allowed_tools` (restricts/loads fewer tool defs into the prompt — improves perf), and `headers` (e.g. `Authorization: Bearer ...` for authenticated endpoints).
- **mcp.json servers** — pre-registered in an `mcp.json` file (supports `command`-launched local servers, e.g. browser automation). Requires "Allow calling servers from mcp.json"; referenced as `"integrations": ["mcp/playwright"]`.

Minimal ephemeral request:
```json
{
  "integrations": [{
    "type": "ephemeral_mcp",
    "server_label": "huggingface",
    "server_url": "https://huggingface.co/mcp",
    "allowed_tools": ["model_search"]
  }]
}
```
Posted to `POST /api/v1/chat` (alongside `model`, `input`, `context_length`). Tool calls return as `"type": "tool_call"` blocks containing `tool`, `arguments`, `output`, and `provider_info`. Gotcha: both server styles are gated behind opt-in settings; verify exact field casing against the running build.

**How The Clockwork Dark applies this:** Provider-agnostically, this is the cleanest path to retire our hand-rolled JSON-epilogue protocol (`engine/agents/parsing.py`, `tool_dispatcher.py`): instead of parsing tool intents out of narration text, the backend executes `@skill` tools server-side and hands back structured `tool_call` blocks our dispatcher can consume directly. Because we own both the server and the client, ephemeral MCP is viable — we can stand up a local MCP server exposing dice/combat/inventory/travel skills and register it per session. We'd keep our streaming gate and governance as a thin adapter layer so swapping LM Studio for another OpenAI-compatible host stays a config change, not a rewrite.

Related: [[lmstudio-act-agentic-loop]], [[lmstudio-python-agent-tools]]
