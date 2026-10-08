#!/usr/bin/env bash
#
# Тест всех параметров сразу.
# Запускает эмулятор с --vfs, --prompt и --script.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

echo "=== Тест: все параметры ==="
echo

python3 "${PROJECT_DIR}/src/main.py" \
    --vfs "${PROJECT_DIR}/vfs/vfs.xml" \
    --prompt "full-test> " \
    --script "${SCRIPT_DIR}/start.txt"

echo
echo "=== Тест завершён ==="
