@echo off
setlocal
cd /d "%~dp0"
set "BUNDLED_PYTHON=C:\Users\wisdom\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%BUNDLED_PYTHON%" (
  "%BUNDLED_PYTHON%" tools\build_local_preview.py
) else (
  py -3 tools\build_local_preview.py
)
if errorlevel 1 pause & exit /b 1
start "" http://127.0.0.1:4173/
if exist "%BUNDLED_PYTHON%" (
  "%BUNDLED_PYTHON%" -m http.server 4173 --bind 127.0.0.1 --directory output\local-preview
) else (
  py -3 -m http.server 4173 --bind 127.0.0.1 --directory output\local-preview
)
