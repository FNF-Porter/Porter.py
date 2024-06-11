![Window icon](images/big-icon.webp)
# Friday Night Funkin' Mod Porter

Ports FNF mods between engines using Python. Right now, there's only support for Psych Engine to the Base Game, but new modes are coming soon! It has a GUI, cross-platform support, and logs (check the `logs` folder).

## Download
Go to the [releases tab](https://github.com/gusborg88/fnf-porter/releases) for slightly older versions. Read the dependencies section if you want to build it yourself.

For an alternative stable source, use our [GameBanana](https://gamebanana.com/tools/16982)

For latest builds, go to the [actions tab](https://github.com/gusborg88/fnf-porter/actions)

## Issues?
Report it in the [issues tab](https://github.com/gusborg88/fnf-porter/issues/).

Check if it **already exists** before reporting though!

Also, logs are saved to your logs folder, so make sure to read them.

## Contributing
Thanks for contributing! You'll need to install [Python](https://www.python.org/downloads/) ofc, and the other dependencies listed in the next section. You can build after this by running [`build.bat`](build.bat). If you have questions about the code, ask the team.

## Dependencies
You can simply run `dependency-install.bat` to install all of these at once. You have to go to [python.org](https://www.python.org/downloads/) and get Python first, though.
- `luaparser`
- `numpy`
- `pillow`
- `pydub`
- `pyinstaller`
- `PyQt6`

You can start the window by running `psychtobase/main.py`,
or alternatively run `build.bat` to build the application yourself.

Note that your build won't be signed, so Windows Defender will probably delete it. Github actions make builds that don't have this issue, so use those instead.

## License
FNF Porter is licensed under CC-BY-NC 4.0. That means you can modify it, but you have to credit the authors (Gusborg, tposejank, BombasticTom & VocalFan), and you can't make ANY money from it. Because this doesn't use any assets from Funkin' Crew, their license doesn't apply here.

Read [LICENSE](LICENSE) for fancy legal words

This program uses FFmpeg, a free software made for manipulating all sorts of media through codecs.
FFmpeg is protected under the LGPL v2.1 License.

Read [FFmpeg's license](FFMPEG-LICENSE)
