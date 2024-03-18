::@echo off

::variables that are the same for every mod
set hyphens=---------------------------------------

title FNF Porter v1 
echo FNF Porter v1
echo Hello Bro
echo Put this in your PsychEngine folder
echo %hyphens%
echo Your mods:
dir /AD /B mods\
set /p "modName=What mod would you like to port? Enter the exact folder name: "

set output=output\%modName%
set input=mods\%modName%


robocopy %input%\images\menucharacters\*.xml %output%\data\weeks\characters
robocopy %input%\images\noteSplashes\*.xml %output%\data\splashes\

::folders that are the same in psych and codename
for /D %%A in (fonts,music,shaders,sounds,images,videos) do (
    robocopy /s %input%\%%A\ %output%\%%A\
)


robocopy %input%\weeks %output%\data\weeks\weeks\

robocopy %input%\characters %output%\data\characters

::for %%A in (%output%\data\characters\) do (
::    python json-to-xml.py %modName%
::)

robocopy %input%\songs\ %output%\songs\ /xf *.json /s
cd %output%\songs\
for /D %%A in (*) do (
    robocopy /MOV %%A\ %%A\song\
)
cd ..

robocopy %input%\data\ %output%\songs\ /xf credits.txt /s
cd %output%\songs\
for /D %%A in (*) do (
    robocopy /MOV %%A\ %%A\charts\
)
cd ..

cd %output%
echo Ported with FNF Porter v1. By Gusborg and BombasticTom. Download: https://gamebanana.com/mods/ > fnf-porter.txt
cd ..

echo %hyphens%
echo Done!
echo Check output/ for your mod
pause
