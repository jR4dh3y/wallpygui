#!/bin/bash
set -euo pipefail

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "pyinstaller not found. Install with: pip install pyinstaller"
  exit 1
fi

# Clean
rm -rf build dist __pycache__

# Version from tag or fallback
PKGVER=${PKGVER:-$(git describe --tags --abbrev=0 2>/dev/null || echo 0.0.1)}

# Ensure optimized bytecode generation (removes asserts, docstrings level 1)
export PYTHONOPTIMIZE=1

SPEC=wallgui.spec

pyinstaller --clean --noconfirm "$SPEC"

# Rename for release asset convenience
if [ -d dist/wallgui ]; then
  tar -C dist -czf "dist/wallgui-${PKGVER}.tar.gz" wallgui
  echo "Archive: dist/wallgui-${PKGVER}.tar.gz"
fi

echo "build ready under dist/wallgui"