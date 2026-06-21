# The Drowned Carillon — a second story on the same engine

*A maritime elegy on the Brass Coast: a sunken cathedral-organ plays beneath the
tide, and each note it strikes calls a little more of the sea inland and a little
more of the living out of true. You can become the hero who silences it, or you
can mend nets, sell chowder, and let the water climb at the edge of hearing.*

This package exists to **prove the Clockwork engine is retargetable**. It is a
wholly different story — tone, threat, people, places — shipped as a
self-contained game package that reuses the engine code **without editing a
single engine file**. *The Clockwork Dark* is the flagship tale; *The Drowned
Carillon* is the demonstration that the story is data and the engine is the
product.

## What lives here

```
games/drowned-carillon/
├── knowledge/      # an OKFS bundle (its own root) — 7 concepts, all links resolve within
│   ├── index.md                  (Architecture — start here)
│   ├── the-drowned-carillon.md   (Lore — the threat)
│   ├── the-receding-tide.md      (Lore — the four tide-phases, arcs & tone)
│   ├── brother-cael.md           (NPC)
│   ├── salt-widow-vesh.md        (NPC)
│   ├── bellfounders-quay.md      (Location — the safe hub)
│   └── the-sunken-nave.md        (Location — the drowned cathedral)
├── data/
│   ├── bestiary.yaml             # 3 foes, same schema as data/bestiary.yaml
│   └── contracts.yaml            # 3 contracts, same schema as data/contracts.yaml
└── README.md
```

## How it reuses the engine (zero engine edits)

- **Knowledge** — `knowledge/` is its *own* `OKFSBundle` root, loaded by the
  unchanged `engine.okfs.OKFSBundle`. It validates with the same rules (required
  frontmatter `type`/`title`/`description`, and every `[[slug]]` link resolves)
  and stays completely separate from the main `knowledge/` bundle and its
  `_index.json` — nothing here pollutes the flagship.

- **Combat** — `data/bestiary.yaml` uses the exact schema the engine's
  `engine.game.combat` reads. Point the engine at it via config
  (`get_config()._data['paths']['bestiary']`) and call `reset_bestiary_cache()`;
  then `resolve_combat` adjudicates fights against *these* foes with the same
  d20 math. The `clockwork` tag still triggers the sympathy "unmaking" path, so a
  brass-tuned chime-husk is unmade by the same code that unmakes a clockwork
  beast — no new mechanics, just new data.

- **Contracts** — `data/contracts.yaml` uses the exact schema the engine's
  `engine.game.contracts.ContractBoard` reads. Point `paths.contracts` at it,
  call `reset_contracts_cache()`, and `available` / `accept` / `complete` grant
  *this* story's rewards through the same engine-authoritative path.

Everything mechanical — dice, combat, fear/sympathy, the evil ticker and Doom
Clock, contracts, the `@skill` registry, the two agents, governance — is
**retained unchanged**. To retarget you rewrite the knowledge and the data, never
the engine. See `knowledge/engine/building-on-the-engine.md` in the repo root.

## Proven by tests

`tests/test_retarget.py` loads this bundle, asserts `validate() == []` and the
expected concepts/types, then drives the **real** engine systems with this
package's data — running `resolve_combat` against the Tide-Cantor and a full
`ContractBoard.available → accept → complete` cycle on *Still the Carillon* — and
asserts the engine produces *this* story's outcomes. The config and caches are
restored in fixtures so the rest of the suite is unaffected.

```bash
python -m pytest tests/test_retarget.py -q
```
