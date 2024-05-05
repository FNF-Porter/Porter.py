# Friday Night Funkin Port Tool (fnf porter)
Ports FNF mods between engines using the command prompt. For now, it's a Windows tool that uses Batch, but maybe we'll add Bash (Mac and Linux) support in the future. The Python and C# code is cross-platform, though.
## Using arguments to skip dialog/helper
**Note, this will probably be removed soon when a UI gets made**

All arguments should be directories, seperated by spaces. If you have a space in the directory, it'll break!

First is the input directory, then the output directory, then the mod name, then the direction. 0 is Psych to Codename, 1 is Codename to Psych. Make sure to **erase all quotes**, and that the mod name has **no spaces**.

For example, if I wanted to copy kero from Psych to Codename on my computer, I could type this into the command prompt:

`C:\Users\Gus\Downloads\fnf-porter\psych-2-codename.bat C:\Users\Gus\SavedGames\PsychEngine\mods C:\Users\Gus\SavedGames\CodenameEngine\mods kero 0`

Or, you can find the fnf-porter folder, right click and select Open with Terminal, and just type this:

`psych-2-codename C:\Users\Gus\SavedGames\PsychEngine\mods C:\Users\Gus\SavedGames\CodenameEngine\mods kero 0`

## todo
### Psych to Base Game
IDK the directory yet
- [x] polymod-meta.json
- [x] polymod-icon.png

### Psych to Codename
**On pause, will resume later**

[thank you codename engine wiki for this one](https://github.com/FNF-CNE-Devs/CodenameEngine/wiki#file-structure--table-of-contents)

Strikethrough: not in Psych Engine 
- [] data
  - [] characters
    - [] character.hx
    - [] character.xml
  - [] config
    - [] credits.xml
    - [] discord.json
    - [] menuItems.txt
    - [] options.xml
  - [] dialogue
    - [] boxes
      - [] dialogue-box.xml
      - [] dialogue-box.hx
    - [] characters
      - [] dialogue-character.xml
  - [] notes
    - [] note.hx
  - [] scripts
    - [] script.hx
  - [] splashes
    - [] splash.xml
  - [] stages
    - [] stage.hx
    - [] stage.xml
  - [] titlescreen
    - [] introText.txt
    - [] titlescreen.xml
  - [] weeks
    - [] characters
      - [] week-character.xml (scale and position)
    - [] weeks
      - [] your-week.xml
    - [] weeks.txt
  - [] alphabet.xml
  - [] freeplaySonglist.txt
  - [] global.hx
- [] fonts
- [] images
  - [] characters
  - [] credits
  - [] dialogue
    - [] boxes
    - [] characters
  - [] game
    - [] cutscenes
    - [] notes
    - [] score
    - [] splashes
    - [] ready, set, go, healthbar, restart png
  -[]  icons
  - [] menus
    - [] mainmenu
    - [] options
    - [] pauseAlt
    - [] storymenu
    - [] titlescreen
    - [] update
    - [] menuBG.png
  - [] stages
- [x] music
- [x] shaders
- [] songs
  - [] your-song
    - [] charts
      - [] chart.json
    - [] scripts
      - [] script.hx
    - [] song
      - [] Inst.ogg
      - [] Voices.ogg
    - [] events.json
    - [] cutscene.hx
    - [] dialogue.xml
    - [] meta.json
  - [] global-script.hx
- [x] sounds
- [x] videos
- [] paths.json
### Codename to Psych
 ehhhhh maybe some other day

## Permissions
You can edit it and give it to other people, or embed it into another engine or application. Please credit Gusborg, BombasticTom, and Cobalt though. Also, this isn't subject to the FNF license.
