@echo off
set ANACONDA_PATH=C:\\anaconda\\20210227


echo Activating Python environment at %ANACONDA_PATH%

rem add flip package to PYTHONPATH but first make sure that this variable is clear
set PYTHONPATH=
for %%a in ("%~dp0\.") do for %%b in ("%%~dpa\.") do set "PYTHONPATH=%%~dpnxb; %PYTHONPATH%"
rem for %%a in ("%~dp0\.") do for %%b in ("%%~dpa\.") do for %%c in ("%%~dpb\.") do set "PYTHONPATH=%%~dpnxc; %PYTHONPATH%"

call %ANACONDA_PATH%\\Scripts\\activate.bat
if %ERRORLEVEL% NEQ 0 (
	echo %~nx0: Anaconda activation failed with error level %ERRORLEVEL%
	exit /b %ERRORLEVEL%
)