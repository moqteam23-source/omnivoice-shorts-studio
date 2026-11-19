@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer from https://www.python.org/downloads/windows/ and enable "Add Python to PATH".
  pause
  exit /b 1
)

if not exist .venv (
  echo Creating a private Python environment...
  py -3 -m venv .venv
  if errorlevel 1 goto failed
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install omnivoice
if errorlevel 1 goto failed

echo Starting the local voice studio. Keep this window open while generating.
python app.py
if errorlevel 1 goto failed
exit /b 0

:failed
echo Setup or launch failed. Check the message above; see README.md for help.
pause
exit /b 1
