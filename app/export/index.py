from os.path import join

from export.csv import to_string_csv
from export.txt import to_string_txt
from export.wikitext import to_string_wikitext_table

def export_dialogues(dialogues, output_dir, output_format="csv"):
    output_format = output_format.lower().strip()

    filename_all = join(output_dir, "@All." + output_format)

    # I'll be honest, this one's not for readability. I just wanted to see if I could
    speakers =  set([sentence.speaker for dialogue in dialogues for sentence in dialogue.sentences])

    if output_format == "csv":
        to_string = to_string_csv
    elif output_format == "txt":
        to_string = to_string_txt
    elif output_format == "wikitext":
        to_string = to_string_wikitext_table


    with open(filename_all, "w", encoding="UTF-8") as file:
        file.write(to_string(dialogues))
    
    for speaker in speakers:
        filename_speaker = join(output_dir, "{0}.{1}".format(speaker, output_format))
        # Same her as above. I just wanted to practice list comprehension. I'm so sorry
        dialogues_speaker = [dialogue for dialogue in dialogues if speaker in [sentence.speaker for sentence in dialogue.sentences]]
        with open(filename_speaker, "w", encoding="UTF-8") as file:
            file.write(to_string(dialogues_speaker))
