#!/usr/bin/env bash
#
# Тест VFS: глубокая структура (3+ уровня).
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

echo "=== Тест VFS: deep ==="
echo

python3 "${PROJECT_DIR}/src/main.py" --vfs "${PROJECT_DIR}/vfs/deep.xml"

echo
echo "=== Тест завершён ==="
