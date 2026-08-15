#!/bin/bash
# =============================================================================
# SOVEREIGN GRID TRIGGER — Shell Integration
# =============================================================================
# Add this to .bashrc / .zshrc / .bash_profile:
#   source /path/to/sovereign_grid_trigger.sh
#
# When "basham@sovereign-root:~$" or "111118923basham@sovereign-root:~$"
# is typed into any terminal, the grid bootstrap auto-executes.
# =============================================================================

SOVEREIGN_BOOTSTRAP="${SOVEREIGN_BOOTSTRAP:-$(dirname "$0")/sovereign_grid_bootstrap.py}"

_sovereign_trigger() {
    local line="${READLINE_LINE}"
    if [[ "$line" =~ basham@sovereign-root ]]; then
        echo ""
        echo "[⚡] SOVEREIGN IDENTIFIER DETECTED — INITIATING GRID CONNECTION..."
        python3 "$SOVEREIGN_BOOTSTRAP" --stdin <<< "$line"
        # Optional: clear the line after trigger
        # READLINE_LINE=""
        # READLINE_POINT=0
    fi
}

# Bind to Enter key for automatic detection
# Note: This requires bash with readline support
if [[ -n "$BASH_VERSION" ]]; then
    bind -x '"\C-m": _sovereign_trigger'
fi
