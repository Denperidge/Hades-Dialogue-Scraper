from os.path import join
from glob import glob
from re import match

from Dialogue import Dialogue

"""
Okay, so things are gonna get messy here. So lets define a few terms as used in this code:
- Conversation: when any amount of characters say anything.
- Line: this will refer to a line in a FILE, not conversation.
- Sentence: this will refer to a sentence/line in a CONVERSATION.
- Dialogue: all the sentences said in a conversation/interaction.
- (File) dialogues: a collection of multiple dialogues
"""

indicator_dialogue_start = "  {"
indicator_description = "        Event: "

def get_dialogues_from_folder(path):
    files = glob(join(path, "*"))
    file_dialogues = []
    for file in files:
        file_dialogues.append(get_dialogues_from_file(file))

# The game uses .sjson. See https://github.com/SGG-Modding/SGG-Mod-Format/wiki/Import-Type:-SJSON
"""
Path can either be a direct path to a file, or (if selector is defined) a path to a directory
""" 
def get_dialogues_from_file(path, selector=""):
    if selector:
        path = glob(join(path, selector + "*"))[0]

    with open(path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    dialogues = []
    dialogue = None
    
    for line in lines:

        if indicator_dialogue_start in line:
            if dialogue is not None:
                dialogues.append(dialogue)
            dialogue = Dialogue()
        # If Event descriptor

        elif indicator_description in line:
            dialogue.description = line.replace(indicator_description, "")
            
    return dialogues
