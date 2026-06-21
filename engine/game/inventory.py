"""
Inventory helpers
=================

One canonical ``add_item`` so combat, crafting, challenges, contracts, and
encounters all share the same find-or-append + quantity-merge logic instead of
maintaining four near-identical private copies. Callers pass provenance
``tags`` (e.g. ``["contract"]``) to record where an item came from.
"""

from __future__ import annotations

from collections.abc import Sequence

from engine.game.state import GameState, InventoryItem


def add_item(
    state: GameState,
    item_id: str,
    name: str = "",
    qty: int = 1,
    *,
    tags: Sequence[str] | None = None,
) -> None:
    """Grant ``qty`` of ``item_id`` to ``state``, merging into a stack if held.

    No-op when ``item_id`` is falsy. ``name`` falls back to ``item_id``; ``tags``
    records provenance on a freshly-created stack only.
    """
    if not item_id:
        return
    for entry in state.inventory:
        if entry.id == item_id:
            entry.qty += qty
            return
    state.inventory.append(
        InventoryItem(id=item_id, name=name or item_id, qty=qty, tags=list(tags or []))
    )
