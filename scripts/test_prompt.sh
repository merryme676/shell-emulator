#!/usr/bin/env bash
#
# Тест параметра --prompt.
# Запускает эмулятор с пользовательским приглашением.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

echo "=== Тест: --prompt ==="
echo

python3 "${PROJECT_DIR}/src/main.py" --prompt "custom> "

echo
echo "=== Тест завершён ==="
