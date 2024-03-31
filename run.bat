@echo off
setlocal

echo Detecting if Python is installed...
for /f "delims=" %%i in ('python --version 2^>^&1') do set "python_version=%%i"

if "%python_version%" == "" (
    echo Python is not installed. 
    echo Please install Python and try again.
    exit /b
)

for /f "tokens=2 delims=." %%a in ("%python_version%") do (
    set /a major=%%a
)

if %major% LSS 3 (
    echo Python version is less than 3.7. 
    echo Please install Python 3.7 or higher and try again.
    exit /b
)

if %major% LSS 3 (
    echo Python version is less than 3.11. 
    echo Please note that Python 3.11 or higher is recommended for this project.
)

echo Python is installed. Version: %python_version%
echo Detecting if virtual environment is activated...

if not exist ".venv\pyvenv.cfg" (
    echo Creating virtual environment in .venv directory.
    python -3 -m venv .venv
)

if "%VIRTUAL_ENV%" == "" (
    echo Virtual environment is not activated.
    echo Activating virtual environment in .venv directory.
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment is already activated.
)

echo Installing dependencies...
pip install -r requirements.txt

echo Running main.py with arguments: %*
python MainUI.py %*

endlocal
