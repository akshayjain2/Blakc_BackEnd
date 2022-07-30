@echo off

if [%1]==[] goto usage
SET conf=%1
goto :run
:usage
SET conf=0.0.0.0:8000
:run
set venv=.\venv\Scripts\activate
set server=.\venv\Scripts\waitress-serve.exe
if exist %server% (
  echo Running Blakc_BackEnd on %conf%
  %venv%
  %server% --listen=%conf% --threads=10 --channel-timeout=3600 Blakc_BackEnd.Blakc_BackEnd.wsgi:application
) else (
  echo [ERROR] Incomplete setup. Please ensure that setup.bat completes without any errors.
  pause
  exit /b
)