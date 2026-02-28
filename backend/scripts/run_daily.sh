#!/bin/zsh
set -euo pipefail

PROJECT_ROOT="$HOME/local/code/werii-gather"
cd "$PROJECT_ROOT"

if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi

export PYTHONPYCACHEPREFIX="$PROJECT_ROOT/.pycache"
python3 -m backend.app.jobs.daily
