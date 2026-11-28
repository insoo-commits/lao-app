#!/bin/bash
# usage: ship.sh OLD NEW "message"
set -e
cd /home/user/lao-app
python3 /mnt/project-files/lao-app/src/v2/build_v263.py /home/user/lao-app /mnt/project-files/lao-app/src/v2/laos_credits.json
node --check app.js
sed -i "s/v$1 ·/v$2 ·/; s/app\.js?v=$1\"/app.js?v=$2\"/" index.html
sed -i "s/lao-shell-v$1\"/lao-shell-v$2\"/" sw.js
git add -A
git commit -qm "v$2: $3

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01FbeTC8Mf88SwUz4nKu1RzT"
for i in 1 2 3 4; do git push -q -u origin main && break; sleep $((i*2)); done
H=$(git rev-parse HEAD); sleep 25
for i in $(seq 1 12); do s=$(gh api "repos/insoo-commits/lao-app/actions/runs?head_sha=$H" --jq '.workflow_runs[0]|.status+" "+(.conclusion//"")'); [[ "$s" == completed* ]] && break; sleep 10; done; echo $s
sed -i "s/(v$1 as of 2026-11-20 \[/(v$2 as of 2026-11-20 [/" /tmp/claude/memory/team/silo/MEMORY.md
