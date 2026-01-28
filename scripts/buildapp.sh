#!/usr/bin/env bash

# === CONFIG ===
APP_NAME="dicomviewer"
ENTRYPOINT="src/dicomviewer/main.py"
DIST_DIR="dist"
BUILD_DIR="build"

# Optional: add an icon (PyInstaller on Linux/macOS typically wants .icns/.png; .ico mainly for Windows)
# ICON="assets/app.ico"

echo
echo "=== Installing dependencies (if needed) ==="
poetry install

echo
echo "=== Building executable with PyInstaller (via Poetry venv) ==="

# Clean previous builds
rm -rf "$DIST_DIR" "$BUILD_DIR" "${APP_NAME}.spec"

# Build one-file executable
poetry run pyinstaller \
  --name "$APP_NAME" \
  --onefile \
  --windowed \
  --clean \
  --noconfirm \
  --distpath "$DIST_DIR" \
  --workpath "$BUILD_DIR" \
  "$ENTRYPOINT"

# If you want a windowed app (no console), add: --noconsole
# If you want an icon, add: --icon "$ICON"

echo
echo "=== Done. Output: ${DIST_DIR}/${APP_NAME} ==="
