from sys import argv
from os.path import realpath, isdir, join, basename, dirname
from os import makedirs
from glob import glob
from extract import get_dialogues_from_file
from export import export_dialogues


if __name__ == "__main__":
    game_path = realpath(argv[1])
    lang = argv[2].lower()
    game_text_dir = join(game_path, "Content/Game/Text")
    lang_dir = join(game_text_dir, lang)
    lang_codes = [basename(path).lower() for path in glob(join(game_text_dir, "*")) if isdir(path)]
    export_dir = realpath(join(dirname(argv[0]), "../", "export/", lang))

    # Create output_dir if needed
    makedirs(export_dir, exist_ok=True)

    # Check if the correct dir has been passed
    if not isdir(game_text_dir):
        raise Exception("The Text directory could not be found at {}. Are you sure you've entered the correct path to the Hades folder?".format(game_text_dir))
    
    # Check if a correct language has been passed
    if lang not in lang_codes:
        raise Exception("The language directory could not be found at {}. Are you sure you've entered a correct Language code? Possible options:".format(lang_codes))

    # If English is being extracted, a different extracting method has to be used
    # See Extract.py for more info on why this is
    if lang == "en":
        en = True
        lang_dir = join(game_text_dir, "de")
    else:
        en = False

    dialogues = \
        get_dialogues_from_file(lang_dir, "_NPCData", en)
    
    export_dialogues(dialogues, export_dir)

