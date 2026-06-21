---
type: Reference
title: Defining Tools for the LM Studio Python Agent
description: How the lmstudio Python SDK turns type-hinted functions into model-callable tools.
tags: [lmstudio, python-sdk, tool-definition, agent]
source: https://lmstudio.ai/docs/python/agent/tools
timestamp: 2026-06-21
---

# Defining Tools for the LM Studio Python Agent

In `lmstudio-python`, a tool is just a plain Python function with type hints and a docstring — the SDK introspects it so the **name, description, and parameter definitions are all passed to the model**:
```python
def add(a: int, b: int) -> int:
    """Given two numbers a and b, returns the sum of them."""
    return a + b
```
Requirements: type annotations on every parameter, and a clear docstring (used as the tool description). The SDK coerces incoming arguments to their annotated types. For more control there is `lmstudio.ToolFunctionDef` (and `ToolFunctionDef.from_callable`) — verify exact signature against the installed SDK.

Tools are handed to the model as a list in the `act()` call:
```python
model.act(
    "Please create a file named output.txt ...",
    [create_file],
)
```
Gotcha: by default a tool that raises has its exception stringified and reported back to the model (so the agent can recover); override via the `handle_invalid_tool_request` callback. Tool quality depends heavily on the model — weak models mis-call or hallucinate tools.

**How The Clockwork Dark applies this:** This is the SDK-sugar version of tool definition, but we deliberately do **not** want to hard-depend on the `lmstudio` package. The portable takeaway is the *contract*: a name, a description, and a typed JSON-Schema-shaped parameter spec. We can generate that same schema from our `@skill` registry and emit it as OpenAI-compatible `tools`/`functions` over the REST API, keeping `tool_dispatcher.py` as the single execution point. If we later run inside LM Studio's agent, `ToolFunctionDef.from_callable` could wrap our skill callables — but our canonical source of truth stays our own registry, so any OpenAI-compatible backend works unchanged.

Related: [[lmstudio-act-agentic-loop]], [[lmstudio-mcp-host]]
