#!/usr/bin/env bash
#
# Тест VFS: несколько файлов в корне.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

echo "=== Тест VFS: several ==="
echo

python3 "${PROJECT_DIR}/src/main.py" --vfs "${PROJECT_DIR}/vfs/several.xml"

echo
echo "=== Тест завершён ==="
