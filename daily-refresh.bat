@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "LOG_PREFIX=[RSSYXY]"
set "TASK_LOG=output\daily-refresh.log"

call :log 开始每日情报更新

REM ===== 1. 启动 AI 网关 =====
if exist "C:\Users\wisdom\Documents\Codex\AI-Launcher\Start-Gateway-Stack.ps1" (
  call :log 启动 AI 网关...
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\wisdom\Documents\Codex\AI-Launcher\Start-Gateway-Stack.ps1"
  REM 等待 LiteLLM 网关就绪（最多 180 秒）
  set /a WAIT_SEC=0
  :wait_litellm
  powershell.exe -NoProfile -Command "Test-NetConnection -ComputerName 127.0.0.1 -Port 20130 -InformationLevel Quiet" >nul 2>nul
  if errorlevel 1 (
    set /a WAIT_SEC+=5
    if !WAIT_SEC! LSS 180 (
      timeout /t 5 /nobreak >nul
      goto wait_litellm
    )
  )
  call :log 网关就绪 (等待约 !WAIT_SEC! 秒)
)

REM ===== 2. 拉取最新代码 =====
call :log 拉取最新代码...
git -C "%~dp0" pull --ff-only origin main
if errorlevel 1 goto :failed

REM ===== 3. 确保虚拟环境 =====
if not exist ".venv\Scripts\python.exe" (
  call :log 创建虚拟环境...
  uv sync
  if errorlevel 1 goto :failed
)

REM ===== 4. 爬取 + AI 翻译 + 生成报告 =====
call :log 爬取+翻译+生成报告...
.venv\Scripts\python.exe -m trendradar
if errorlevel 1 goto :failed

REM ===== 5. 富化（单次最多30篇，异步后台执行）=====
set "RSSYXY_AI_LIMIT=30"
start "RSSYXY-Enrich" /b cmd /c "set PYTHONUTF8=1 && .venv\Scripts\python.exe tools\enrich_articles.py >> output\enrich.log 2>&1"
call :log 后台富化已启动 (单次30篇)

REM ===== 6. 构建本地预览 =====
call :log 构建本地预览...
.venv\Scripts\python.exe tools\build_local_preview.py
if errorlevel 1 goto :failed

REM ===== 7. 同步报告到根目录 =====
copy /Y output\html\latest\current.html index.html >nul
if errorlevel 1 goto :failed

REM ===== 8. 提交并推送 =====
git add index.html site-data\enriched.json
git diff --cached --quiet
if not errorlevel 1 goto :no_changes
git commit -m "chore: daily enriched report (%date% %time:~0,5%)"
if errorlevel 1 goto :failed
git push origin main
if errorlevel 1 goto :failed

call :log 更新并同步完成
exit /b 0

:no_changes
call :log 没有新的数据变更
exit /b 0

:failed
call :log 更新失败，错误码 !errorlevel!
exit /b 1

:log
echo %LOG_PREFIX% %date% %time% %* >> "%TASK_LOG%"
exit /b 0
