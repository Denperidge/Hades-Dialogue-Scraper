from os.path import join
from glob import glob
from re import match

"""
Okay, so things are gonna get messy here. So lets define a few terms:
- Dialogue: any spoken word. This 
"""

def get_file_dialogues_from_folder(path):
    files = glob(join(path, "*"))
    file_dialogues = []
    for file in files:
        file_dialogues.append(get_dialogues_from_file(file))

# The game uses .sjson. See https://github.com/SGG-Modding/SGG-Mod-Format/wiki/Import-Type:-SJSON
def get_dialogues_from_file(path):
    with open(path, "r", encoding="UTF-8") as file:
        lines = file.readlines()
    
    for line in lines:
        # If Event descriptor
        if "Event: " in line:




