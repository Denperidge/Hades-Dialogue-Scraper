from os import remove, makedirs, removedirs, rename
from os.path import join, isfile, realpath, dirname
from shutil import which
from platform import system
from subprocess import run
from zipfile import ZipFile
from urllib.request import urlretrieve

# This uses the Linux tree command
def create_html_nav(path, title=None, pattern=None, ignore=None, dirs_only=False, level=None):
    tree_bin = is_tree_installed()
    if tree_bin is None:
        print("'tree' binary not found, skipping html nav creation")
        return
    
    index_html = join(path, "index.html")
    # Thanks to https://stackoverflow.com/a/46383157
    tree_command = [
        tree_bin, 
        "-H", ".",  # Base for relative navigation
        "--noreport",  # No console printing
        "--charset", "utf-8",  # Char encoding
        "-o", index_html,  # Output to index.html in provided path
        "--dirsfirst"  # Set dirs first in nav
        ]
    if title:
        tree_command += ["-T", title]
    if pattern:
        tree_command += ["-P" , pattern]
    if ignore:
        tree_command += ["-I", ignore]
    if dirs_only:
        tree_command.append("-d")
    if level is not None:  # Don't use "if level" in case of 0 value
        tree_command += ["-L", str(level)]
        
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
        vendor_dir = realpath(join(dirname(__file__), "../../vendor/"))
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
