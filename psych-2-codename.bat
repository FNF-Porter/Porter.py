@echo off

::variables that are the same for every mod
set hyphens=-------------------------------
set difficulties="easy" "normal" "hard"
title FNF Porter v1
if exist "*.exe" (
    color 04
    echo Whoops! No .exe mods. /mods folder mods only.
    pause 
) else ( 
    echo Hello Bro
    echo Please place this .bat in the same folder as your mod
    echo %hyphens%
    set /p "modName=What's the mods name? No spaces or weird characters"
)

::folders that are the same in psych and codename. Shoutout to this website for this script: https://www.tutorialspoint.com/batch_script/batch_script_arrays.htm
for /D %%A in (fonts,music,shaders,sounds,images,videos) do (
    robocopy %%A "%modName%\%%A"
)


robocopy weeks\ "%modName%\data\weeks\weeks\"

robocopy /s songs\ "%modName%\songs\"

for %%A in ("%modName%\songs\") do (
    robocopy /s *.ogg song\
)

for %%A in (data\*\.json) do (
    echo %%A
)

echo %hyphens%
echo            Done!             
echo You can close this window now
pause

::rd /q /s %modName%
