# Sovereign Grid Self-Initiation Bootstrap v1.0.0

Zero-dependency, cross-platform grid connection trigger for the canonical identifier `basham@sovereign-root`.

When the identifier is detected in any input stream (argv, stdin, clipboard, terminal, or web page), the bootstrap auto-executes the full verification pipeline and connects to the grid.

## Canonical Trigger Patterns

| Pattern | Form |
|---------|------|
| `basham@sovereign-root:~$` | Native terminal |
| `111118923basham@sovereign-root:~$` | Fused prefix |
| `Basham@sovereign-root` | Capitalized reference |
| `basham@sovereign-root` | Lowercase reference |

## Files

- **`sovereign_grid_bootstrap.py`** — Core engine (Python 3, stdlib only)
- **`sovereign_grid_trigger.sh`** — Shell integration (`.bashrc` / `.zshrc`)
- **`sovereign_grid_trigger.js`** — Browser bookmarklet
- **`sovereign_grid_userscript.js`** — Tampermonkey / Greasemonkey userscript

## Quick Start

### Terminal (one-shot)

```bash
python3 sovereign_grid_bootstrap.py "basham@sovereign-root:~$"
# or
echo "basham@sovereign-root:~$" | python3 sovereign_grid_bootstrap.py --stdin
# or
python3 sovereign_grid_bootstrap.py --clipboard
```

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

## Verification Pipeline

1. Identifier Lock — regex confirms canonical form  
2. Gate 1 — `Baptist` → N = 18684484080202612, N mod 49 = 0  
3. Gate 2 — H·N mod 10¹⁴ → S₅₀ construction  
4. Gate 3 — BR-010 canonical 50-byte ASCII → SHA-256  
5. Gate 4 — secp256k1 scalar k, P = kG, curve membership, compressed key  
6. 15 Modular Locks — all polarization key invariants verified  
7. Polarization Key Integrity — 19 tokens, 7 ones, God Seal 43, H_MHZ exact  
8. Grid Connection — `Node 129: ONLINE`, `T1_LOCKED: ACTIVE`

Exit code 0 = grid connected. Exit code 1 = identifier missing or lock failure.

## Design Principles

- Zero external dependencies (Python standard library only)
- Exact integer arithmetic throughout (no floats)
- secp256k1 implemented from scratch
- Cross-platform (Linux / macOS / Windows clipboard + shell)
- The identifier itself is the trigger — no separate invocation required

---

`basham@sovereign-root:` — grid armed.
