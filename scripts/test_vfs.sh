#!/usr/bin/env bash
#
# Тест параметра --vfs.
# Запускает эмулятор с указанием пути к VFS.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

echo "=== Тест: --vfs ==="
echo

python3 "${PROJECT_DIR}/src/main.py" --vfs "${PROJECT_DIR}/vfs/vfs.xml"

echo
echo "=== Тест завершён ==="
