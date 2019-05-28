#!/usr/bin/env bash

set -e;

python -m http.server 3456 &
SERVER_PID=$!
echo "server PID=$SERVER_PID"
nosetests
bash scripts/black.sh
bash scripts/pylint.sh --full
kill $SERVER_PID
