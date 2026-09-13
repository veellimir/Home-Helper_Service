@echo off
setlocal

set RUFF=".venv\Scripts\ruff.exe"

echo ========================================
echo Ruff format
echo ========================================

%RUFF% format .
if errorlevel 1 (
    echo Ruff format failed.
    exit /b 1
)

echo.
echo ========================================
echo Ruff check
echo ========================================

%RUFF% check . --fix
if errorlevel 1 (
    echo Ruff check failed.
    exit /b 1
)

echo.
echo ========================================
echo All checks passed.
echo ========================================

endlocal
