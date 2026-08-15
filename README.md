# Sovereign Grid Self-Initiation Bootstrap v1.0.0 + Vault & Archive v1.0.1

Zero-dependency, cross-platform grid connection trigger for the canonical identifier `basham@sovereign-root`, plus secure vault, immutable archive, and Gate 158 crypto pipeline.

When the identifier is detected in any input stream (argv, stdin, clipboard, terminal, or web page), the bootstrap auto-executes the full verification pipeline and connects to the grid.

## Canonical Trigger Patterns

| Pattern | Form |
|---------|------|
| `basham@sovereign-root:~$` | Native terminal |
| `111118923basham@sovereign-root:~$` | Fused prefix |
| `Basham@sovereign-root` | Capitalized reference |
| `basham@sovereign-root` | Lowercase reference |

## Files

### Core
- **`sovereign_grid_bootstrap.py`** — Core engine (Python 3, stdlib only). Four-gate verification + 15 modular locks + polarization key integrity → Node 129 ONLINE / T1_LOCKED.
- **`sovereign_grid_trigger.sh`** — Shell integration (`.bashrc` / `.zshrc`)
- **`sovereign_grid_trigger.js`** — Browser bookmarklet
- **`sovereign_grid_userscript.js`** — Tampermonkey / Greasemonkey userscript

### Vault & Archive Module (v1.0.1)
- **`sovereign_grid_vault_archive.py`** — Gate 158 crypto pipeline router, HMAC-sealed vault, append-only hash-chained archive, Stellar/BENJI pipeline binding, TSA certificate store.

## Quick Start

### Terminal (one-shot)

```bash
python3 sovereign_grid_bootstrap.py "basham@sovereign-root:~$"
# or
echo "basham@sovereign-root:~$" | python3 sovereign_grid_bootstrap.py --stdin
# or
python3 sovereign_grid_bootstrap.py --clipboard
```

### Vault & Archive Pipeline

```bash
python3 sovereign_grid_vault_archive.py
```

Runs Gate 158 → unlocks vault → stores crypto identifier + Stellar pipeline + TSA cert → builds immutable archive chain.

### Shell Integration

```bash
# Add to ~/.bashrc or ~/.zshrc
source /path/to/sovereign_grid_trigger.sh
```

When you type any of the identifier patterns and press Enter, the grid bootstrap runs automatically.

### Web (manual)

Create a browser bookmark with the contents of `sovereign_grid_trigger.js` as the URL. Click it on any page that contains the identifier.

### Web (automatic)

Install `sovereign_grid_userscript.js` in Tampermonkey or Greasemonkey. It scans every page load and DOM mutation.

## Verification Pipeline (Bootstrap)

1. Identifier Lock — regex confirms canonical form  
2. Gate 1 — `Baptist` → N = 18684484080202612, N mod 49 = 0  
3. Gate 2 — H·N mod 10¹⁴ → S₅₀ construction  
4. Gate 3 — BR-010 canonical 50-byte ASCII → SHA-256  
5. Gate 4 — secp256k1 scalar k, P = kG, curve membership, compressed key  
6. 15 Modular Locks — all polarization key invariants verified  
7. Polarization Key Integrity — 19 tokens, 7 ones, God Seal 43, H_MHZ exact  
8. Grid Connection — `Node 129: ONLINE`, `T1_LOCKED: ACTIVE`

Exit code 0 = grid connected. Exit code 1 = identifier missing or lock failure.

## Gate 158 Crypto Pipeline (Vault Module)

```
(718 | 892) & 158 == 158
```

- Unlocks HMAC-SHA256 sealed vault (key derived from canonical S)
- Stores: crypto identifier (secp256k1 / BTC address / WIF), Stellar BENJI pipeline, TSA certificate (TSU3.12)
- Appends every operation to an immutable previous-hash archive chain
- Temporal attestation ready (RFC 3161 style via stored TSA)

## Design Principles

- Zero external dependencies (Python standard library only)
- Exact integer arithmetic throughout (no floats)
- secp256k1 implemented from scratch
- Cross-platform (Linux / macOS / Windows clipboard + shell)
- The identifier itself is the trigger — no separate invocation required
- Vault unlock gated by Gate 158; all entries content-hashed + HMAC sealed
- Archive is append-only with chain integrity verification

---

`basham@sovereign-root:` — grid armed.  
Gate 158 — vault unlocked.
