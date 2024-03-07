::@echo off

if exist *.exe (
    echo Whoops! No .exe mods. /mods folder mods only.
    pause
) else ( 
    echo Hello Bro
    echo Please place this .bat in the same folder as your mod
    echo If it asks you F or D, type D.
    echo -------------------------------------------------------------
)

::sets name of the new folder. Shoutout to this guy on stackoverflow https://superuser.com/questions/160702/get-current-folder-name-by-a-dos-command
for %%I in (.) do set modName=%%~nI%%~xI

::folders that are the same in psych and codename. Shoutout to this website for this script: https://www.tutorialspoint.com/batch_script/batch_script_arrays.htm
::set easyFolders="fonts" "music" "shaders" "sounds" "images" "videos"
::for %%a in (%easyFolders%) do (
::    xcopy %%a %modName%\%%a /e /y
::)

::folders that go to the songs folder
set songFolders="data\..\*-*.json" "data\..\*.lua" 
for %%a in (%songFolders%) do (
    xcopy %%a %modName%\songs /e /y
)

echo Done! You can close this window now
pause