from platform import system
from os import remove, makedirs, removedirs, rename
from subprocess import run
from os.path import join, isfile, realpath, dirname
from shutil import which
from urllib.request import urlretrieve
from zipfile import ZipFile


def export_dialogues(dialogues, output_dir, output_format="csv"):
    output_format = output_format.lower().strip()

    filename_all = join(output_dir, "all." + output_format)

    # I'll be honest, this one's not for readability. I just wanted to see if I could
    speakers =  set([sentence.speaker for dialogue in dialogues for sentence in dialogue.sentences])

    if output_format == "csv":
        to_string = to_string_csv


    with open(filename_all, "w", encoding="UTF-8") as file:
        file.write(to_string(dialogues))
    
    for speaker in speakers:
        filename_speaker = join(output_dir, "{0}.{1}".format(speaker, output_format))
        # Same her as above. I just wanted to practice list comprehension. I'm so sorry
        dialogues_speaker = [dialogue for dialogue in dialogues if speaker in [sentence.speaker for sentence in dialogue.sentences]]
        with open(filename_speaker, "w", encoding="UTF-8") as file:
            file.write(to_string(dialogues_speaker))

def to_string_csv(dialogues):
    string = "Id|Description|Speaker|Text\n"
    

    for dialogue in dialogues:
        for sentence in dialogue.sentences:
            string += "{0.id}|{0.description}|{1.speaker}|{1.text}\n".format(dialogue, sentence)
    
    return string

# This uses the Linux tree command
def create_html_nav(path, glob=None):
    tree_bin = is_tree_installed()
    if tree_bin is None:
        print("'tree' binary not found, skipping html nav creation")
        return
    
    index_html = join(path, "index.html")
    # Thanks to https://stackoverflow.com/a/46383157
    tree_command = [tree_bin, "-H", ".", "--noreport", "--charset", "utf-8", "-o", index_html]
    if glob is not None:
        tree_command += ["-P" , glob]
    run(tree_command, cwd=path)
        



def is_tree_installed():
    # If on Unix, it should be pre-installed
    os = system()
    if (os != "Windows"):
        # Thanks to https://stackoverflow.com/a/34177358
        if which("tree") is not None:
            return "tree"
        else:
            print("'tree' binary not found. Is it added to path?")
            return None
    # If on Windows, don't use the built-in tree
    elif os == "Windows":
        vendor_dir = realpath(join(dirname(__file__), "../vendor/"))
        tree_path = join(vendor_dir, "tree.exe")
        tree_url = "https://download.sourceforge.net/project/gnuwin32/tree/1.5.2.2/tree-1.5.2.2-bin.zip"

        if isfile(tree_path):
            return tree_path
        else:
            print("Detected Windows runtime, but no local Cygwin32 tree binary")
            print("Do you wish to install it from {}".format(tree_url))
            print("If 'yes', the zip will be downloaded, tree.exe extracted to {}, and then the other downloaded files cleaned. No changes to PATH will be made.")
            print("If 'no', html generation will be skipped.")
            prompt = input("Download tree? y/[n]: ").lower().strip()
            if len(prompt) < 1:
                return None
            elif prompt[0] != "y":
                return None
            else:
                makedirs(dirname(tree_path), exist_ok=True)
                zip_filename = tree_path + ".zip"
                print("Downloading zip...")
                urlretrieve(tree_url, zip_filename)
                print("Extracting...")
                ZipFile(zip_filename).extract("bin/tree.exe", path=vendor_dir)
                rename(join(vendor_dir, "bin/tree.exe"), tree_path)
                print("Cleaning up...")
                remove(zip_filename)
                removedirs("vendor/bin")

                return tree_path
