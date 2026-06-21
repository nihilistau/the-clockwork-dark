---
type: Reference
title: LM Studio Cancelling Predictions (Python SDK)
description: Stop an in-flight prediction via PredictionStream.cancel() in lmstudio-python.
tags: [lmstudio, python, cancellation, streaming]
source: https://lmstudio.ai/docs/python/llm-prediction/cancelling-predictions
timestamp: 2026-06-21
---

# LM Studio Cancelling Predictions (Python SDK)

Aborts an ongoing generation based on custom app logic that can't be expressed as `stopStrings` or `maxPredictedTokens`.

**Key API surface:**
- `model.respond_stream(...)` returns a `PredictionStream`.
- `PredictionStream.cancel()` — interrupts the running prediction.
- Cancellation requires the **streaming** API; the synchronous convenience `respond()` has no mid-flight cancel.

```python
import lmstudio as lms
model = lms.llm()

stream = model.respond_stream("What is the meaning of life?")
for fragment in stream:
    if should_stop():        # custom logic
        stream.cancel()
        # recommended: keep iterating so partial result + stats are recorded
```

**Gotchas:** after `cancel()`, docs recommend letting iteration finish so the partial result and final stats are captured; breaking immediately is permitted but discards the partial output and stats. Verify exact class name (`PredictionStream`) against your SDK version.

**How The Clockwork Dark applies this:** This is the conceptual analog of our `TurnBudget` guard in `engine/agents/resilience.py`, which enforces a per-turn wall-clock and approximate-token ceiling. In our provider-agnostic layer we cancel by closing the httpx SSE stream / stopping iteration on `LMSClient.chat_stream` when the budget trips, rather than calling a SDK `cancel()`. The doc's "let iteration complete to keep partial results" guidance argues for draining and emitting the partial narration on budget-exhaustion instead of hard-aborting.

Related: [[lmstudio-chat-completion]]
