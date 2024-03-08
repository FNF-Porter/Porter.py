::@echo off

::variables that are the same for every mod
set hyphens=-------------------------------
set difficulties=easy normal hard
title %currentOperation% - FNF Porter v1

set currentOperation=Welcome

if exist *.exe (
    color 04
    echo Whoops! No .exe mods. /mods folder mods only.
    set currentOperation=Whoops!
    pause
) else ( 
    echo Hello Bro
    echo Please place this .bat in the same folder as your mod
    echo This won't work if the mod folder has spaces!
    echo You can edit that now
    echo %hyphens%
    set currentOperation=Welcome
    pause
)

::sets name of the new folder. Shoutout to this guy on stackoverflow https://superuser.com/questions/160702/get-current-folder-name-by-a-dos-command
for %%a in (.) do set modName=%%~na 
    echo %modName%

::folders that are the same in psych and codename. Shoutout to this website for this script: https://www.tutorialspoint.com/batch_script/batch_script_arrays.htm
set easyFolders=fonts music shaders sounds images videos
for %%b in (%easyFolders%) do (
    xcopy /e /y %%b %modName%\%%b\
)
set currentOperation=Processing...

dir /b data\ 
for %%c in (.) do (
    set %songName%=dir /b data\
)
set %songName% dir /b 

::moves charts to the songs folder
set songName=kero
set chart=%songName%-%%d
for %%d in (%difficulties%) do (
    xcopy /y /i data\%songName%\%chart%.json %modName%\data\%songName%\song\
)

xcopy weeks\ %modName%\data\weeks\weeks\


::for %%a in (%songFolders%) do (
::    echo %%a %modName%\songs\ /e /y
::)

set currentOperation=Done!
echo %hyphens%
echo            Done!             
echo You can close this window now
echo %hyphens%
pause
