---
type: Architecture
title: The Clockwork Dark — Knowledge Index
description: Root of the OKFS knowledge bundle; start here and follow the links.
tags: [index, okfs, clockwork]
timestamp: 2026-06-22
---

# The Clockwork Dark — Knowledge Index

This is the root of our **OKFS** knowledge bundle — one concept per Markdown
file, traversed by following `[[slug]]` links. Agents and humans start here and
read only what's relevant (progressive disclosure), not 3,000 lines at once.

## How to read this
The format itself is defined in [[okfs-spec]]; the project-wide convention (all
docs, including the root agent guides, are OKFS) is [[okfs-conventions]]. The
bundle is loaded by `engine/okfs/` (`OKFSBundle`), validated for frontmatter +
link integrity, and queried by the agents through a confidence cascade.

## Start points
- **What we're building** → [[clockwork-architecture]]
- **How we talk to the LLM today + where it's going** → [[lmstudio-integration-overview]]
- **Native-LLM migration plan** (structured output, tool-calls, MCP) → [[llm-migration-plan]]

## The Engine (more than this one game)
- **The Clockwork Engine** (three layers, turn flow) → [[clockwork-engine]]
- **Agent architecture** (the two powers, in depth) → [[agent-architecture]]
- **Build your own game on it** (retargeting) → [[building-on-the-engine]]
- **Systems catalog** (every system + its tools) → [[systems-catalog]]
- **Extending the engine** (add a skill / interceptor / challenge / concept) → [[extending-the-engine]]
- **Project log** → [[changelog]]

## Runbooks (setup)
- **Run on the networked beast** → [[run-on-the-beast]]
- **ComfyUI image generation** → [[install-comfyui]]
- **Voxtral TTS/ASR voice** → [[install-voxtral]]

## The reactive world
- **How the world changes** → [[the-reactive-world]] · [[the-village-empties]]
- **Set-pieces** → [[the-tunnel-mouth]] · [[the-first-warden]]
- **Places & people** → [[the-forge]]

## Game lore
- **The world & the wound** → [[the-clockwork-dark]] · [[evil-phases]] · [[the-heartlands]] · [[the-harvest]] · [[beneath-the-tunnels]]
- **Powers, people & craft** → [[the-two-powers]] · [[the-tinkers]] · [[maris-hearth]] · [[sympathy-and-naming]]
- **Pacing, work & the end** → [[doom-arcs]] · [[the-notice-board]] · [[the-tinkers-questline]] · [[the-convergence]]

## LM Studio reference (provider-agnostic)
LM Studio is our current local backend; these concepts capture its capabilities,
each with a "how The Clockwork Dark applies this" note so nothing hard-couples us
to one vendor.

- REST: [[lmstudio-streaming-events]], [[lmstudio-stateful-chats]]
- OpenAI-compat: [[lmstudio-structured-output]], [[lmstudio-tool-use]], [[lmstudio-responses-api]]
- Python SDK: [[lmstudio-chat-completion]], [[lmstudio-structured-response]], [[lmstudio-cancelling-predictions]], [[lmstudio-repl]]
- Agentic / tools: [[lmstudio-act-agentic-loop]], [[lmstudio-python-agent-tools]], [[lmstudio-mcp-host]]
