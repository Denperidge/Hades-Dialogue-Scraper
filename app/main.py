from sys import argv
from os.path import realpath, isdir, join, basename
from glob import glob
from extract import get_file_dialogues_from_folder


if __name__ == "__main__":
    game_path = realpath(argv[1])
    lang = argv[2].lower()
    game_text_dir = join(game_path, "Content/Game/Text")
    lang_dir = join(game_text_dir, lang)
    lang_codes = [basename(path).lower() for path in glob(join(game_text_dir, "*")) if isdir(path)]

    # Check if the correct dir has been passed
    if not isdir(game_text_dir):
        raise Exception("The Text directory could not be found at {}. Are you sure you've entered the correct path to the Hades folder?".format(game_text_dir))
    
    # Check if a correct language has been passed
    if lang not in lang_codes:
        raise Exception("The language directory could not be found at {}. Are you sure you've entered a correct Language code? Possible options:".format(lang_codes))
    
    dialogues = get_file_dialogues_from_folder(lang_dir)
    print(dialogues)
