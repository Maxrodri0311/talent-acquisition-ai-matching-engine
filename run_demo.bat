@echo off
title Talent Acquisition AI Engine & Funnel Intelligence Platform
color 0B

echo ===============================================================================
echo   APPLY ON JOB -- TALENT ACQUISITION AI ENGINE & FUNNEL INTELLIGENCE
echo   Staff Data Science, Zero-Trust Security & Kimball Star Schema OLAP
echo ===============================================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [1/3] Running Full End-to-End Pipeline (Data Generator + Matching + OLAP)...
python src\main.py --applications 25000 --postings 250 --candidates 12500
if %errorlevel% neq 0 (
    echo [ERROR] Pipeline execution failed.
    pause
    exit /b 1
)

echo.
echo [2/3] Executing Automated Pytest Verification Suite...
python -m pytest tests\ -v --tb=short
if %errorlevel% neq 0 (
    echo [ERROR] Unit tests failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Running Latency and Throughput Benchmarks...
python benchmarks\run_benchmark.py

echo.
echo ===============================================================================
echo   [SUCCESS] TALENT ACQUISITION AI ENGINE DEMO COMPLETED IN 100%% GREEN STATE!
echo   * Web Dashboard Ready: Open web\index.html in your browser.
echo   * Executive Excel: dist\Talent_Acquisition_Executive_Dashboard.xlsx
echo ===============================================================================
echo.
pause
