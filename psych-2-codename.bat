::FNF Porter v1. By Gusborg and BombasticTom.
@echo off
::if you want to pass arguments
if [%1] neq [] (
    set psychMods=%1
    set codenameMods=%2
    set modName=%3
    set direction=%4
    goto :skip
)
::initial settings
set hyphens=---------------------------------------
title FNF Porter v1 (Psych to Codename)
echo +%hyphens%+
echo +   FNF Porter v1 (Psych to Codename)   +
echo +      By Gusborg and BombasticTom      +
echo +%hyphens%+
echo Hello Bro
echo If the mod folder has any spaces, it'll break. Please change it if it does!
echo If you want to skip this process, read README.md.
pause
explorer %userprofile%\Downloads

::things the user sets
set /p "psychMods=Where is your PsychEngine\mods folder? Drag the directory here, no quotes or slash at the end: "
set /p "codenameMods=Where is your CodenameEngine\mods folder? Drag the directory here, no quotes or slash at the end: "
::set /p "direction=What direction would you like to go? Type 0 for Psych to Codename, type 1 for Codename to Psych: "
cd %psychMods%
echo Your mods:
dir /ad /b
set /p "modName=What mod would you like to port? If the folder has spaces in it's name, exit and change that! Type it here: "

:skip
::more settings
set input=%psychMods%\%modName%
set output=%codenameMods%\%modName%
md %output%
if %errorlevel% equ 1 (
    echo ERROR: The directory %output% already exists
    echo You might overwrite files, or mix ones that weren't ported with ones that were.
    echo Are you sure you'd like to continue?
    pause
)

::log
set "log=%output%\fnf-porter.log"
echo Thanks for using FNF Porter v1 (Psych to Codename)>%log%
echo Download: https://gamebanana.com/mods/>>%log%
echo %date% %time%>>%log%
echo %hyphens%>>%log%

::set /p "backgroundImages=Where are the background images stored? Please select all of them, or the directory with them in it, and drag them here. Seperated by commas: " 
:: the files and folders to be moved
::First argument is input, second is output, third is filetype (put a dot in front), fourth is more aruments to send like /mov
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
call :copy-nodir images\ images\game
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
goto :finish

::file conversions with python
::python json-to-xml.py

::robocopy %input%\images\menucharacters\*.xml %output%\data\weeks\characters
::robocopy %input%\images\noteSplashes\*.xml %output%\data\splashes\

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

:copy
robocopy /unilog+:%log% /ns /s /xf:readme.txt %4 input%\%1%3 %output%\%2
goto :error
exit /b

::I love making functions for things that are only used once!
:copy-nodir
robocopy /unilog+:%log% /ns /xf:readme.txt %input%\%1 %output%\%2
goto :error
exit /b

:error
if %errorlevel% geq 8 (
    @echo ERROR: %1 couldn't copy to %2. Read %log%
) else (
    @echo SUCCESS: %1 copied to %2
)
exit /b

:python
python %1
exit /b

:finish
echo %hyphens%
echo Done!
echo Check %output% for your mod
echo Check %log% for any errors
pause
