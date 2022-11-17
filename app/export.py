from os.path import join

def export_dialogues(dialogues, output_dir, output_format="csv"):
    output_format = output_format.lower().strip()

    filename_all = join(output_dir, "all." + output_format)

    # Get all speakers
    #all_sentences = [dialogue.sentences for dialogue in dialogues]
    #speakers = set([sentence[0] for sentence in all_sentences])
    #print(speakers.pop().speaker)
    #exit()


    if output_format == "csv":
        to_string = to_string_csv


    with open(filename_all, "w") as file:
        file.write(to_string(dialogues))

def to_string_csv(dialogues):
    string = "Id|Description|Speaker|Text\n"
    

    for dialogue in dialogues:
        for sentence in dialogue.sentences:
            string += "{0.id}|{0.description}|{1.speaker}|{1.text}\n".format(dialogue, sentence)
    
    return string

        