@echo off

echo -=- Luxor to OpenSMCE Game Converter -=-
echo.
echo ===========================================
echo Step 0. Checking the requirements...
echo ===========================================
set good=1

py --version >nul
if %errorlevel% neq 0 (
	echo ! Python is not installed !
	set good=0
)

if not exist data\ (
	echo ! Folder "data" does not exist !
	set good=0
)

rem if exist data\data\ (
rem	echo ! Folder "data" is nested too deeply !
rem	set good=0
rem )

if not exist english\ (
	echo ! Folder "english" does not exist !
	set good=0
)

rem if exist english\english\ (
rem	echo ! Folder "english" is nested too deeply !
rem	set good=0
rem )

if not exist assets\ (
	echo ! Folder "assets" does not exist !
	set good=0
)

if not exist Luxor_appendix\ (
	echo ! Folder "Luxor_appendix" does not exist !
	set good=0
)

if %good% equ 1 (
	echo All good!
) else (
	echo ===========================================
	echo The converter found some issues and will not convert the game properly.
	echo They are listed above.
	echo Before proceeding, fix them and run convert.bat again.
	echo If you think some of these errors are false positive,
	echo contact me on Discord!
	echo ===========================================
	echo.
	echo The converter will now close.
	pause
	goto exit
)

echo.
echo.
echo.
echo If you haven't checked README file yet, just in case please do it before proceeding!
echo The original files will be available in "_BACKUP" directory. If you want, you can delete it afterwards.
echo ===========================================
echo The converter will start working once you press any key.
pause
echo.
echo.
echo.
echo.
echo.
echo ===========================================
echo Step 1. Preparing and backing up...
echo ===========================================
if exist data\data\ (
	echo The "data" folder is nested too deeply, fixing...
	xcopy /q /s /y "data\data\" "data\"
	rmdir /s /q data\data
	echo Done!
)
if exist English\English\ (
	echo The "English" folder is nested too deeply, fixing...
	xcopy /q /s /y "English\English\" "English\"
	rmdir /s /q English\English
	echo Done!
)
mkdir "_BACKUP"
xcopy /q /s /y "data\" "_BACKUP\data\"
xcopy /q /s /y "English\" "_BACKUP\English\"
xcopy /q /s /y "assets\" "_BACKUP\assets\"
xcopy /q /s /y "Luxor_appendix\" "_BACKUP\Luxor_appendix\"
echo.
echo.
echo.
echo.
echo.
echo ===========================================
echo Step 2. Merging data/ with english/...
echo ===========================================
xcopy /q /s /y "English\data\" "data\"
rmdir /s /q English
echo.
echo.
echo.
echo.
echo.
echo ===========================================
echo Step 3. Converting...
echo ===========================================
setlocal enabledelayedexpansion
py -m pip install pillow
py main.py
if %errorlevel% neq 0 (
	echo ===========================================
	echo Oh no^^! Something has gone wrong during the conversion process.
	echo Please screenshot the console and send it to me via Discord^^!
	echo ===========================================
	echo.
	echo The converter will now close.
	choice /m "Would you like to revert the files to the original state"
	set /a keep=2-!errorlevel!
	
	if !keep! equ 1 (
		echo.
		echo Okay, reverting...
		rmdir /s /q output
		rmdir /s /q Luxor
		rmdir /s /q data
		rmdir /s /q assets
		rmdir /s /q Luxor_appendix
		xcopy /q /s /y "_BACKUP\data\" "data\"
		xcopy /q /s /y "_BACKUP\English\" "English\"
		xcopy /q /s /y "_BACKUP\assets\" "assets\"
		xcopy /q /s /y "_BACKUP\Luxor_appendix\" "Luxor_appendix\"
		rmdir /s /q _BACKUP
	)
	goto exit
)
setlocal disabledelayedexpansion
echo.
echo.
echo.
echo.
echo.
echo ===========================================
echo Step 4. Copying additional files...
echo ===========================================
xcopy /q /s "data\music\" "output\music\"
xcopy /q /s "data\sound\" "output\sounds\"
xcopy /q /s "Luxor_appendix\*" "output\"
del "output\music\*.sl3"
del "output\sounds\*.sl3"
echo.
echo.
echo.
echo.
echo.
echo ===========================================
echo Step 5. Cleaning up...
echo ===========================================
ren output Luxor
rmdir /s /q data
rmdir /s /q assets
rmdir /s /q Luxor_appendix
ren "Luxor\_config.json" "Luxor\config.json"
echo The converter finished its job, hopefully successfully.
echo If you haven't spotted any error in this console, you can launch OpenSMCE now..
echo If you have spotted an error though, make sure you have Python installed and all required folders.
echo If you struggle to find a source of the error, send a screenshot of this console to me via Discord!
echo Press any key to close this window.
pause
:exit