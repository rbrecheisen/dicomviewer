@echo off
setlocal enabledelayedexpansion

REM === CONFIG ===
set APP_NAME=dicomviewer
set ENTRYPOINT=src\dicomviewer\main.py
set DIST_DIR=dist
set BUILD_DIR=build

REM Optional: add an icon (must be .ico)
REM set ICON=assets\app.ico

echo.
echo === Installing dependencies (if needed) ===
poetry install

echo.
echo === Building executable with PyInstaller (via Poetry venv) ===

REM Clean previous builds
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
if exist "%APP_NAME%.spec" del /q "%APP_NAME%.spec"

REM Build one-file exe
poetry run pyinstaller ^
  --name "%APP_NAME%" ^
  --onefile ^
  --windowed ^
  --clean ^
  --noconfirm ^
  --distpath "%DIST_DIR%" ^
  --workpath "%BUILD_DIR%" ^
  "%ENTRYPOINT%"

REM If you want a windowed app (no console), add: --noconsole
REM If you want an icon, add: --icon "%ICON%"

echo.
echo === Done. Output: %DIST_DIR%\%APP_NAME%.exe ===
endlocal
