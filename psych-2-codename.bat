::@echo off

::variables that are the same for every mod
set hyphens=---------------------------------------
set difficulties="easy" "normal" "hard"
title FNF Porter v1
echo Hello Bro
echo Put this in your PsychEngine folder
echo Your mods:
dir /AD /B mods\
echo %hyphens%
set /p "modName=What mod would you like to port? Enter the exact folder name: "



set output=psych-to-codename-output\%modName%
set input=mods\%modName%

::folders that are the same in psych and codename
for /D %%A in (fonts,music,shaders,sounds,images,videos) do (
    robocopy /s %input%\%%~A %output%\%%~A
)


robocopy %input%\weeks %output%\data\weeks\weeks\

for %%A in (.) do (
    robocopy /s %input%\songs\ %output%\songs\
    robocopy /s %input%\weeks\ %output%\data\weeks\week\
)

for /D %%A in (.) do (
    robocopy /s /mov %output%\songs\ %output%\songs\song\ *.ogg
)

cd %output%
echo Ported with FNF Porter v1. By Gusborg and BombasticTom. Download for yourself: https://gamebanana.com/mods/ > fnf-porter.txt
cd ..\..\

echo %hyphens%
echo Done!
pause
