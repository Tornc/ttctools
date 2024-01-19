@echo off
title Extension mover

set "currentFolder=%~dp0"
set "extensionFolder=%USERPROFILE%\.tanks\extensions"
set "unusedFolder=%USERPROFILE%\.tanks\extensions\unused_API_extensions"
set "tanksFolder=%PROGRAMFILES(X86)%\Steam\steamapps\common\Tanks"
set "optionsFolder=%USERPROFILE%\.tanks\"

:init
echo First time using this script?
echo Make sure you have the "TanksModAPI_v1.1.4.jar"
echo and the extensions in the same folder as this 
echo "Extension mover" batch file.
echo.
pause

:menu
cls
echo What do you want to do?
echo 1) Run Tanks Mod API
echo 2) Disable extensions (quit Tanks first!)
echo 3) Quit
choice /c 123 /n 
if %errorlevel%==1 call :startAPI
if %errorlevel%==2 call :stopAPI
if %errorlevel%==3 exit
echo.
goto :menu

:startAPI
call :checkExistFolder

:: Move the API jar
if exist "TanksModAPI_v1.1.4.jar" (
	move "TanksModAPI_v1.1.4.jar" "%tanksFolder%"
)

:: Move all new extensions to the extensions folder
for %%F in ("%currentFolder%\*.jar") do (
    move "%%F" "%extensionFolder%\"
)

:: Move all unused extensions into extension folder
for %%I in ("%unusedFolder%\*.jar") do (
    move "%%~I" "%extensionFolder%\"
)

:: Enabling extension settings
call :changeOptions

start /b "" "%tanksFolder%\TanksModAPI_v1.1.4.jar" debug

goto :EOF

:stopAPI
:: Abort if Java is still running
tasklist /FI "IMAGENAME eq javaw.exe" 2>NUL | find /I "javaw.exe" >NUL

if "%errorlevel%"=="0" (
	echo Unable to disable extensions!
    echo Java process is still running.
	goto :EOF
)

call :checkExistFolder

:: Move all extensions to the unused folder
for %%I in ("%extensionFolder%\*.jar") do (
    move "%%~I" "%unusedFolder%\"
)

goto :EOF

:checkExistFolder
:: Create new folders if they don't exist
if not exist "%extensionFolder%" (
	mkdir "%extensionFolder%"
	echo Extension folder created!
)

if not exist "%unusedFolder%" (
	mkdir "%unusedFolder%"
	echo Unused extension folder created!
)

goto :EOF

:changeOptions
setlocal enabledelayedexpansion

set "search_line_1=enable_extensions=false"
set "replace_line_1=enable_extensions=true"

set "search_line_2=auto_load_extensions=false"
set "replace_line_2=auto_load_extensions=true"

set "input_file=%optionsFolder%\options.txt"
set "output_file=%optionsFolder%\settings_modified.txt"

(
    for /f "delims=" %%a in ('type "%input_file%"') do (
        set "line=%%a"
        if "!line!"=="%search_line_1%" (
            echo %replace_line_1%
        ) else if "!line!"=="%search_line_2%" (
            echo %replace_line_2%
        ) else (
            echo %%a
        )
    )
) > "%output_file%"

move /y "%output_file%" "%input_file%"

endlocal

goto :EOF