#!/usr/bin/env bash
#
# Тест VFS: минимальная структура.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

echo "=== Тест VFS: minimal ==="
echo

python3 "${PROJECT_DIR}/src/main.py" --vfs "${PROJECT_DIR}/vfs/minimal.xml"

echo
echo "=== Тест завершён ==="
