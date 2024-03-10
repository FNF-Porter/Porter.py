::@echo off

::variables that are the same for every mod
set hyphens=-------------------------------
set difficulties="easy" "normal" "hard"
set modName=%~dp0
title FNF Porter v1
if exist "*.exe" (
    color 04
    echo Whoops! No .exe mods. /mods folder mods only.
    pause 
) else ( 
    echo Hello Bro
    echo Please place this .bat in the same folder as your mod
    echo for example
    echo 17 bucks
    echo    characters
    echo    data
    echo    images
    echo    ...
    echo    %~n0%~x0
    echo %hyphens%
)

::folders that are the same in psych and codename. Shoutout to this website for this script: https://www.tutorialspoint.com/batch_script/batch_script_arrays.htm
for /D %%A in (fonts,music,shaders,sounds,images,videos) do (
    robocopy %%A "%modName%"\%%A
)


robocopy weeks\ "%modName%"\data\weeks\weeks\

for %%A in (songs\) do (
    robocopy /s songs\ "%modName%"\songs\songName\song
)

for %%A in (data\*\.json) do (
    echo %%A
)

echo %hyphens%
echo            Done!             
echo You can close this window now
pause

rd /q /s "%modName%"
