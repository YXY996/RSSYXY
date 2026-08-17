@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "LOG_PREFIX=[RSSYXY]"

echo %LOG_PREFIX% %date% %time% 开始每日情报更新

if exist "C:\Users\wisdom\Documents\Codex\AI-Launcher\Start-Gateway-Stack.ps1" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\wisdom\Documents\Codex\AI-Launcher\Start-Gateway-Stack.ps1"
)

git pull --ff-only origin main
if errorlevel 1 goto :failed

if not exist ".venv\Scripts\python.exe" (
  C:\Users\wisdom\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m uv sync
  if errorlevel 1 goto :failed
)

.venv\Scripts\python.exe scripts\apply_sources.py
if errorlevel 1 goto :failed
.venv\Scripts\python.exe -m trendradar
if errorlevel 1 goto :failed
.venv\Scripts\python.exe tools\enrich_articles.py
if errorlevel 1 goto :failed
.venv\Scripts\python.exe tools\build_local_preview.py
if errorlevel 1 goto :failed

git add site-data\enriched.json
git diff --cached --quiet
if not errorlevel 1 goto :no_changes
git commit -m data-daily-ai-briefing
if errorlevel 1 goto :failed
git push origin main
if errorlevel 1 goto :failed

echo %LOG_PREFIX% %date% %time% 更新并同步完成
exit /b 0

:no_changes
echo %LOG_PREFIX% %date% %time% 没有新的中文阅读稿
exit /b 0

:failed
echo %LOG_PREFIX% %date% %time% 更新失败，错误码 %errorlevel%
exit /b 1
