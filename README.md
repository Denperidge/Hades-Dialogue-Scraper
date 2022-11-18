# Hades Dialogue Scraper

While looking for quotes from the video game Hades, I noticed not all of them were documented on the game's Wiki. So let's add to it, shall we?

## Installation
- Prerequirements: an installation of the game and Python3
- Simply clone the repository and run the script provided!

## Usage
```bash
python app/main.py "{path/to/hades/gamefiles}" {output_format} {lang}
```
- Path:
    - Must point to top directory of the Hades installation
- Output formats:
    - Availble output formats: `[all, csv, txt, wikitext]`
    - `all` will export in all avaiable output formats
    - A single value is supported by (for example) just writing `csv`
    - Multiple values (seperated by a `,`) are supported.
    - If omitted, defaults to `all`.
    - More export formats can be added through the [export code](app/export/)
- Lang:
    - Available lang values `['de', 'en', 'es', 'fr', 'it', 'ja', 'ko', 'pl', 'pt-BR', 'ru', 'zh-CN']`
    - Note: if lang is omitted, all languages will be extracted & exported.
    - Available values are dependant on which translations are available in the game files


Example usage: 
```bash
python app/main.py "C:/Program Files (x86)/Steam/steamapps/common/Hades" en
```

## ID's & Descriptions
So, the Id's in the filenames are... cryptic. `ZeusWithAthena01` is relatively simple to decypher, especially once reading the text.
However, `BossCharonMiscStart06` starts muddying the waters, especially because all the text you can find in it is `Grrr... nrrraauuuggghhh!!`.

So, I created [description.py](app/description.py). The function in it is run every time a description is generated. It will check the ID against a list of regex (currently only 1, though) and parse it if the regex matches. If no matches are found, the function defaults into splitting up the Camelcase.

This currently results in the examples above being parsed as follows:
- `ZeusWithAthena01` -> `Duo - Zeus and Athena (1)`
- `BossCharonMiscStart06` -> `Boss Charon Misc Start 06`

Due to reasons above and those described in the corresponding issue [(#6)](/../../issues/6) I am not actively working on this parsing. So if you feel like contributing, help over there would be greatly appreciated!


## License
The code in this project is licensed under the [MIT License](LICENSE). The game - and thus anything extracted from it - belongs to Supergiant Games.
