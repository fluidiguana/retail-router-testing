@echo off
REM Batch script to run the evaluation
REM Usage: run_eval.bat

REM Check if OPENAI_API_KEY is set
if "%OPENAI_API_KEY%"=="" (
    echo ERROR: OPENAI_API_KEY environment variable is not set.
    echo.
    echo Please set it using:
    echo   set OPENAI_API_KEY=your-api-key-here
    echo.
    echo Or set it permanently in your system environment variables.
    exit /b 1
)

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found at venv\Scripts\python.exe
    echo Please run: python -m venv venv
    exit /b 1
)

echo Running evaluation with venv...
echo.

REM Run the evaluation using venv's Python directly
venv\Scripts\python.exe run_eval.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Evaluation completed successfully!
) else (
    echo.
    echo Evaluation failed with exit code: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

