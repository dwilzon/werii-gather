#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="/Users/david/Library/Mobile Documents/com~apple~CloudDocs/Business/Projects/Cogi"
BACKEND_DIR="$PROJECT_ROOT/backend"

cd "$BACKEND_DIR"

if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi

export PYTHONPYCACHEPREFIX="$PROJECT_ROOT/.pycache"
python3 -m app.jobs.daily
