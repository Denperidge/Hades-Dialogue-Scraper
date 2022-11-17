from os.path import join

def export_dialogues(dialogues, output_dir, output_format="csv"):
    output_format = output_format.lower().strip()

    filename_all = join(output_dir, "all." + output_format)

    # I'll be honest, this one's not for readability. I just wanted to see if I could
    speakers =  set([sentence.speaker for dialogue in dialogues for sentence in dialogue.sentences])

    if output_format == "csv":
        to_string = to_string_csv


    with open(filename_all, "w") as file:
        file.write(to_string(dialogues))
    
    for speaker in speakers:
        filename_speaker = join(output_dir, "{0}.{1}".format(speaker, output_format))
        # Same her as above. I just wanted to practice list comprehension. I'm so sorry
        dialogues_speaker = [dialogue for dialogue in dialogues if speaker in [sentence.speaker for sentence in dialogue.sentences]]
        with open(filename_speaker, "w") as file:
            file.write(to_string(dialogues_speaker))

def to_string_csv(dialogues):
    string = "Id|Description|Speaker|Text\n"
    

    for dialogue in dialogues:
        for sentence in dialogue.sentences:
            string += "{0.id}|{0.description}|{1.speaker}|{1.text}\n".format(dialogue, sentence)
    
    return string

        