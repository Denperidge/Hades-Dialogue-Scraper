from os.path import join
from glob import glob
from re import match

from Dialogue import Dialogue, Sentence

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
The dialogue's ID is used to create a description in the Dialogue object.

So, when going through the file:
- Create a dialogues dict(id, dialogue)
- If encountering an event id, check if it exists in the dict
    - If it doesn't exist in the dict, add the currently being worked on Dialogue, create a new Dialogue object
    - If it does, pass
- If encountering a speaker, remember their name
- If encountering a sentence, add "{last_encountered_speaker}: {line_text}" to dialogues[last_encountered_id].sentences
"""

indicator_sentence_start = "  {"
indicator_description = "        Event: "
indicator_speaker = "      Speaker = "
indicator_sentence = "      DisplayName = "

indicator_en_end_dialogue = "      */"


def get_dialogues_from_folder(path, selector, en=False):
    files = glob(join(path, selector))
    dialogues = []
    for file in files:
        dialogues += get_dialogues_from_file(file, en=en)
    
    return dialogues


def sanitize_json_value(value):
    return value.replace("\n", "").strip('"').strip()


# The game uses .sjson. See https://github.com/SGG-Modding/SGG-Mod-Format/wiki/Import-Type:-SJSON
"""
Path can either be a direct path to a file, or (if selector is defined) a path to a directory
""" 
def get_dialogues_from_file(path, selector="", en=False):
    if selector:
        path = glob(join(path, selector + "*"))[0]

    with open(path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    if not en:
        dialogues = lines_to_dialogues(lines)
    else:
        dialogues = en_lines_to_dialogues(lines)

    return dialogues


def lines_to_dialogues(lines):
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
            sentence = Sentence(last_encountered_speaker, sentence_text)

            dialogues[last_encountered_id].sentences.append(sentence)

        # Convert dict to list
    dialogues_list = list()
    for id in dialogues:
        dialogues_list.append(dialogues[id])

    return dialogues_list

"""
But if you wanna get the `en` dialogue you can throw a bit of that out of the window
Okay so this is a bit wonky. 
- The English dialogue is hardcoded in the games LUA files.
- All the translations are added in subfolders in `Content/Game/Text/{lang}/_*.sjson`. 
- However, the devs added comments into these sjson files of the corresponding English dialogue, in the right order.
- So instead of extracting from the .lua files, I chose to extract from one of the languages .sjson.

So why use `de` specifically to get the `en` values? A nice combination of being able to read it a bit, and it being the first alphabetically. 

So, when going through the file for English translations:
- Create a dialogues list (id, dialogue)
- If encountering an event id, add the currently worked on Dialogue object to the dict (if any)



So, when going through the file:
- Create a dialogues list
- If encountering a event id
    - Set adding_sentences to true
- If encountering the end of the comment (and thus dialogue)
    - Add the dialogue to the list
    - Set adding_sentences to false
- If encountering any line besides the above
    - If adding_sentences is True, add to the currently worked on dialogue
    - If adding_sentences if False, pass
"""


def en_lines_to_dialogues(lines):
    dialogues = list()

    current_dialogue = None
    adding_sentences = False

    for line in lines:
        if indicator_description in line:
            id = sanitize_json_value(line.replace(indicator_description, ""))
            current_dialogue = Dialogue(id)
            adding_sentences = True

        elif indicator_en_end_dialogue in line and current_dialogue is not None:
            dialogues.append(current_dialogue)
            adding_sentences = False
        
        elif adding_sentences:
            value = sanitize_json_value(line)
            current_dialogue.sentences.append(Sentence.from_comment(value))
    
    return dialogues


