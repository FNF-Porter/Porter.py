::Created by Gusborg and BombasticTom. Read LICENSE
::@echo off

::variables that are the same for every mod
set hyphens=---------------------------------------
cd ..
set workingDir=%cd%

title FNF Porter v1 
echo FNF Porter v1
echo Hello Bro
echo Put this in your PsychEngine folder
echo %hyphens%
echo Your mods:
dir /AD /B mods\
set /p "modName=What mod would you like to port? Enter the exact folder name: "

set "input=%workingDir%\mods\%modName%"
md %workingDir%\mods-cne\%modName%\
set "output=%workingDir%\mods-cne\%modName%"
set "log=%output%\fnf-porter.log"
echo Ported with FNF Porter v1. By Gusborg and BombasticTom.>%log%
echo Download: https://gamebanana.com/mods/>>%log%
echo %hyphens%>>%log%
echo ERRORS:>>%log%

:: there's probably some way to do this with a for loop but idk how
call :copy-generic fonts fonts
call :copy-generic music music
call :copy-generic shaders shaders
call :copy-generic sounds sounds
call :copy-generic images images
call :copy-generic videos videos

::robocopy %input%\images\menucharacters\*.xml %output%\data\weeks\characters
::robocopy %input%\images\noteSplashes\*.xml %output%\data\splashes\

::to check when all the calls end
echo I shit myself
echo the shit is dripping donw my legs

::robocopy %input%\weeks %output%\data\weeks\weeks\

::robocopy %input%\characters %output%\data\characters

::for %%A in (%output%\data\characters\) do (
::    python json-to-xml.py %modName%
::)

::robocopy %input%\songs\ %output%\songs\ /xf *.json /s
::cd %output%\songs\
::for /D %%A in (*) do (
::    robocopy /MOV %%A\ %%A\song\
::)
::cd ..

::robocopy %input%\data\ %output%\songs\ /xf credits.txt /s
::cd %output%\songs\
::for /D %%A in (*) do (::
::    robocopy /MOV %%A\ %%A\charts\
::)
::cd ..

goto :eof
:copy-generic
robocopy /s /unilog+:%log% %input%\%~1 %output%\%~2
if %errorlevel% geq 8 (
    echo ERROR: %1 couldn't copy to %2. Read error above>>%log%
) else (
    echo %1 successfully copied to %2>>%log%
)
exit /b
xcopy 
echo %hyphens%
echo Done!
echo Check "%output%" for your mod
pause
