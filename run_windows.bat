@echo off
set VENV_DIR=venv

if not exist "%VENV_DIR%\" (
    echo No virtual environment found. Creating...
    python -m venv %VENV_DIR%

    call %VENV_DIR%\Scripts\activate

    if exist requirements.txt (
        echo Installing dependencies...
        pip install -r requirements.txt
    ) else (
        echo File requirements.txt not found. No dependency installed.
    )

    echo Environment Installed, running...
) else (
    echo Environment already installed, running...
    call %VENV_DIR%\Scripts\activate
)

python init.py