from sys import argv
from os.path import realpath, isdir, join, basename, dirname
from os import makedirs
from glob import glob
from extract import get_dialogues_from_file, get_dialogues_from_folder
from export import export_dialogues


def extract_and_export(game_text_dir, lang):
    lang_dir = join(game_text_dir, lang)
    # If English is being extracted, a different extracting method has to be used
    # See Extract.py for more info on why this is
    if lang == "en":
        en = True
        lang_dir = join(game_text_dir, "de")
    else:
        en = False

    dialogues = get_dialogues_from_folder(lang_dir, "_*", en)

    export_dir = realpath(join(dirname(argv[0]), "../", "export/", lang))
    # Create output_dir if needed
    makedirs(export_dir, exist_ok=True)
    export_dialogues(dialogues, export_dir)



if __name__ == "__main__":

    # SETUP: get & check game directory
    game_path = realpath(argv[1])
    game_text_dir = join(game_path, "Content/Game/Text")
    game_lang_dirs = [path for path in glob(join(game_text_dir, "*")) if isdir(path)]
    lang_codes = [basename(path).lower() for path in game_lang_dirs]



    # Check if the correct dir has been passed
    if not isdir(game_text_dir):
        raise Exception("The Text directory could not be found at {}. Are you sure you've entered the correct path to the Hades folder?".format(game_text_dir))
    
    # If lang code is provided
    # SETUP: get & check lang code
    if len(argv) >= 3:
        lang = argv[2].lower()
        # Check if a correct language has been passed
        if lang not in lang_codes:
            raise Exception("The language directory could not be found at {}. Are you sure you've entered a correct Language code? Possible options:".format(lang_codes))
        
        extract_and_export(game_text_dir, lang)

    # If no lang ocde is provided
    else:
        # Extract from all languages
        for lang in lang_codes:
            extract_and_export(game_text_dir, lang)
        
    


