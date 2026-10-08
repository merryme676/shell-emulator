#!/usr/bin/env bash
#
# Тест параметра --script.
# Запускает эмулятор со стартовым скриптом.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

echo "=== Тест: --script ==="
echo

python3 "${PROJECT_DIR}/src/main.py" --script "${SCRIPT_DIR}/start.txt"

echo
echo "=== Тест завершён ==="
