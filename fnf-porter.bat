::USER SETTINGS
::To make the changes, remove the two semicolons before set, and remove one semicolon before skip.
::set "input=Write PsychEngine/mods directory here"
::set "output=Write CodenameEngine/mods directory here"
::skip
::Ok, stop editing

::FNF Porter v1. By Gusborg and BombasticTom.
@echo off
::if you want to pass arguments
if [%1] neq [] (
    set input/mods=%1
    set output/mods=%2
    set modName=%3
    set direction=%4
    goto :skip
)
::setup
set hyphens=---------------------------------------
title FNF Porter v1
echo +%hyphens%+
echo +                 FNF Porter v1                 +
echo +   By Gusborg, BombasticTom, and CobaltBar   +
echo +%hyphens%+
echo Hello Bro
echo If the mod folder has any spaces, it'll break. Please change it if it does!
echo If you want to skip this process, read README.md.
pause
explorer %userprofile%\Downloads

::things the user sets
echo Directions:
echo 0 - Psych to Codename (partially done)
echo 1 - Codename to Psych (not started)
echo 2 - Psych to Base game (select this one)
echo 3 - Codename to Base game (not started)
set /p "direction=What direction would you like to go? "

if %direction% equ 2 (
        set "inputName=PsychEngine"
        set "outputName=FridayNightFunkin"
) else if %direction% neq 2 (
        echo Don't use this for now, we are working on it
        exit
)
explorer %userprofile%\Downloads
echo Where is your %inputName% folder? Drag the directory here, no quotes or slash at the end
set /p "inputPre="
echo Where is your %outputName% folder? Drag the directory here, no quotes or slash at the end
set /p "outputPre="

:skip
cd %inputPre%\mods
echo Your mods:
dir /ad /b
echo What mod would you like to port? If the folder has spaces in it's name, exit and change that!
set /p "modName="

::more settings
set input=%inputPre%\mods\%modName%
set output=%outputPre%\mods\%modName%
cd %output%
md %output%
if %errorlevel% equ 1 (
    echo WARNING: The directory %output% already exists
    echo You might overwrite files, or mix ones that weren't ported with ones that were.
    echo Are you sure you'd like to continue?
    pause
)
goto :%direction%

::log
set "log=%output%\fnf-porter.log"
echo Thanks for using FNF Porter v1>%log%
echo Download: https://gamebanana.com/mods/>>%log%
echo %date% %time%>>%log%
echo %hyphens%>>%log%


::PSYCH TO CODENAME
goto :eof
:0
::First argument is input, second is output, third is filetype (put a dot in front), fourth is more aruments to send like /mov
::set /p "backgroundImages=Where are the background images stored? Please select all of them, or the directory with them in it, and drag them here: " 
call :copy fonts fonts
call :copy music music
call :copy shaders shaders
call :copy sounds sounds
call :copy videos videos
call :copy images\credits images\credits
call :copy images\icons images\icons
call :copy images\

::images
call :copy-filetype images\menucharacters data\weeks\characters json
call :copy-filetype images\menucharacters images\menus\storymenu\characters
call :copy-no-subdir images\ images\game
call :copy %backgroundImages% images\stages


call :copy weeks data\weeks\weeks
call :copy characters data\characters
call :copy data\credits.txt data\config\credits.txt
call :copy scripts data
call :copy songs songs
call :copy data songs
call :copy stages data\stages
cd %output%\songs\
for /d %%a in (*) do (
    robocopy %%a\*.ogg %%a\song
    robocopy %%a\*.json %%a\charts
    robocopy %%a\*.lua %%a\scripts
)
exit /b

:2
call :copy pack.png pack.png
cd %output%
ren pack.png polymod_icon.png
call :copy songs

::file conversions with python
::python json-to-xml.py

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
:copy
robocopy /unilog+:%log% /ns /s /xf:readme.txt %4 input%\%1%3 %output%\%2
goto :error
exit /b

goto :eof
::I love making functions for things that are only used once!
:copy-no-subdir
robocopy /unilog+:%log% /ns /xf:readme.txt %input%\%1%3 %output%\%2
goto :error
exit /b

goto :eof
:error
if %errorlevel% geq 8 (
    @echo ERROR: %1 couldn't copy to %2. Read %log%
) else (
    @echo SUCCESS: %1 copied to %2
)
exit /b

goto :eof
:python
python %1
exit /b

echo %hyphens%
echo Done!
echo Check %output% for your mod
echo Check %log% for any errors
pause
