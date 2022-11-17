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

Now, in the .sjson files, there is a Texts array with contains all *SENTENCES*.
It is important to note that they are not grouped by dialogue.
However, it seems that they *are* added in the correct order for the dialogue to play out

Example of two subsequent sentece objects:
    {
      /*
        Event: ZeusWithAthena01
        Zeus: Why, look, Zagreus, here comes brave Athena, first to reach you among all my kin, in all her shrewdness. So proactive, you contacted Zagreus prior to even telling me, my dear!
        Athena: Lord Father, would that I could settle even more such matters quickly and discreetly, so that only the most vital of them rise up to the level of your notice, sir. Though, I'm certain Zagreus and I are very grateful you have intervened.
      */
      Id = "Zeus_0196"
      Speaker = "Zeus"
      DisplayName = "Ah, sieh nur, Zagreus, da kommt die tapfere Athene, in ihrer ganzen Klugheit. Hat dich als Erste erreicht, ganz die Planerin. Du hast Verbindung mit Zagreus aufgenommen und es mir erst danach erzählt, meine Liebe!"
    }
    {
      /*
        Event: ZeusWithAthena01
        Zeus: Why, look, Zagreus, here comes brave Athena, first to reach you among all my kin, in all her shrewdness. So proactive, you contacted Zagreus prior to even telling me, my dear!
        Athena: Lord Father, would that I could settle even more such matters quickly and discreetly, so that only the most vital of them rise up to the level of your notice, sir. Though, I'm certain Zagreus and I are very grateful you have intervened.
      */
      Id = "Athena_0224"
      Speaker = "Athena"
      DisplayName = "Ehrwürdiger Vater, ich wünschte, ich könnte noch mehr derlei Angelegenheiten rasch und diskret beilegen, damit nur die wichtigsten davon deine Beachtung finden. Obgleich ich sicher bin, dass Zagreus und ich dein Eingreifen sehr schätzen."
    }

So these two sentences are from the same dialogue, yet are in different objects,
with the only common factor being the comments having the dialogue's ID ("Event: ...")
The dialogue's ID is used to create a description

So, when going through the file:
- Create a dialogues dict(id, dialogue)
- If encountering a event id, check if it exists in the dict
    - If it doesn't exist in the dict, add the currently being worked on Dialogue, create a new Dialogue object
    - If it does, pass
- If encountering a speaker, remember their name
- If encountering a sentence, add "{last_encountered_speaker}: {line_text}" to dialogues[last_encountered_id].sentences
"""

indicator_sentence_start = "  {"
indicator_description = "        Event: "
indicator_speaker = "      Speaker = "
indicator_sentence = "      DisplayName = "

def get_dialogues_from_folder(path):
    files = glob(join(path, "*"))
    file_dialogues = []
    for file in files:
        file_dialogues.append(get_dialogues_from_file(file))


def sanitize_json_value(value):
    return value.replace("\n", "").strip('"')

# The game uses .sjson. See https://github.com/SGG-Modding/SGG-Mod-Format/wiki/Import-Type:-SJSON
"""
Path can either be a direct path to a file, or (if selector is defined) a path to a directory
""" 
def get_dialogues_from_file(path, selector=""):
    if selector:
        path = glob(join(path, selector + "*"))[0]

    with open(path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    dialogues = dict()
    last_encountered_speaker = last_encountered_id = None
    
    for line in lines:

        if indicator_description in line:
            id = last_encountered_id = sanitize_json_value(line.replace(indicator_description, ""))

            if id not in dialogues:
                new_dialogue = Dialogue(id)
                dialogues[id] = new_dialogue
        
        elif indicator_speaker in line:
            last_encountered_speaker = sanitize_json_value(line.replace(indicator_speaker, ""))
        
        elif indicator_sentence in line:
            sentence_text = sanitize_json_value(line.replace(indicator_sentence, ""))
            sentence = "{0}: {1}".format(last_encountered_speaker, sentence_text)

            dialogues[last_encountered_id].sentences.append(sentence)

    # Convert dict to list
    dialogues_list = list()
    for id in dialogues:
        dialogues_list.append(dialogues[id])

    return dialogues_list
