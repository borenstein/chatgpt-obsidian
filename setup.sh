#!/usr/bin/env bash
set -euo pipefail

# 0. Codex has network during this phase *only*
# 1. Ensure pip itself is fresh
python -m pip install --upgrade --no-cache-dir pip

# 2. Install PDM into the global Python (virtualenv is over-kill here)
python -m pip install --no-cache-dir "pdm[venv]>=2.4.0"

# 3. Jump to your repo (Codex clones into /workspace/<repo>)
cd /workspace/*

# 4. Sync dependencies *inside* the container
#    --group :all   = prod + optional/extra groups
#    --no-editable  = install project itself as a wheel, avoids path issues
pdm install --group :all --no-editable --no-lock

# Optional: make 'pytest' work without 'pdm run'
pdm export -f requirements --without-hashes -o /tmp/req.txt
pip install --no-cache-dir -r /tmp/req.txt

