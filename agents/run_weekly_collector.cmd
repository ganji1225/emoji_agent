@echo off
REM ========================================================
REM  Irodori-TTS 週次ナレッジコレクター（ローカル自動実行）
REM  毎週土曜 09:00 に Windows タスクスケジューラから起動
REM  収集 → agents/knowledge/ 蓄積 → git commit & push
REM ========================================================
setlocal enabledelayedexpansion

set "CLAUDE=%APPDATA%\npm\claude.cmd"
set "PROMPT_FILE=E:\irodori\agents\knowledge\WEEKLY_LOCAL_PROMPT.md"
set "LOG_DIR=E:\irodori\agents\knowledge\run_logs"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM 実行日時のタイムスタンプ（YYYYMMDD_HHMMSS）
set "STAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "STAMP=%STAMP: =0%"
set "LOG=%LOG_DIR%\weekly_%STAMP%.log"

cd /d E:\irodori

REM プロンプトファイルの中身を claude にヘッドレス投入
REM --permission-mode bypassPermissions で対話プロンプトを抑止
type "%PROMPT_FILE%" | "%CLAUDE%" -p --permission-mode bypassPermissions > "%LOG%" 2>&1

echo Exit code: %ERRORLEVEL% >> "%LOG%"
endlocal
