# Hades Dialogue Scraper

While looking for quotes from the video game Hades, I noticed not all of them were documented on the game's Wiki. So let's add to it, shall we?



## Installation
Pre-requirements: an installation of the game, Python3, pip

## Usage
`python app/main.py {path/to/hades/gamefiles} {lang}`
Example: `python app/main.py C:/Program Files (x86)/Steam/steamapps/common/Hades en`

Available lang values (as of writing): `['de', 'en', 'es', 'fr', 'it', 'ja', 'ko', 'pl', 'pt-BR', 'ru', 'zh-CN']`


## Why does extracting `en` Dialogue use `de` files?
Okay so this is a bit wonky. The English dialogue is hardcoded in the games LUA files. All the translations are added in subfolders in `Content/Game/Text/{lang}/_*.sjson`. However, the devs added comments into these sjson files of the corresponding English dialogue, in the right order. So instead of extracting from the .lua files, I chose to extract from one of the languages .sjson.

So why `de` specifically? A nice combination of being able to read it a bit, and it being the first alphabetically.
