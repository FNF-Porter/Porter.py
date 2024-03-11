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

set output=output\%modName%
set input=mods\%modName%

robocopy %input%\images\menucharacters\*.xml %output%\data\weeks\characters
robocopy %input%\images\noteSplashes\*.xml %output%\data\splashes\

::folders that are the same in psych and codename
for /D %%A in (fonts,music,shaders,sounds,images,videos) do (
    robocopy /s %input%\%%A %output%\%%A
)


robocopy %input%\weeks %output%\data\weeks\weeks\

::for %%A in (%output%\data\characters\) do (
::    python json-to-xml.py %modName%
::)

robocopy /s %input%\songs\ %output%\songs\

for /D %%A in (%output%\songs\*) do (
    for %%B in (%%A\*) do (
        :: thank you chatgpt
        rem Extract the file name and extension
        set filename=%%~nxB
        rem Create a new directory with the file name (without extension)
        mkdir %%A\!filename:~0,-4!" >nul 2>&1
        rem Move the file to the newly created directory
        move %%B "%%A\!filename:~0,-4!\" >nul 2>&1
    )
)

:: In very early stages, right now it only converts character JSONs
python json-to-xml.py %modName%

::for /D %%A in (%output%\songs\) do (
::    ren %output%\songs\%%A\ 
::)

::for /D %%A in (.) do (
::    robocopy /s /mov %output%\songs\ %output%\songs\song\ *.ogg
::)

cd %output%
echo Ported with FNF Porter v1. By Gusborg and BombasticTom. Download: https://gamebanana.com/mods/ > fnf-porter.txt
cd ..\..\

echo %hyphens%
echo Done!
echo Check output/ for your mod
pause
