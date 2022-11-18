from export.replace import parse_formatting_in_sentence

def to_string_csv(dialogues):
    string = "Id|Description|Speaker|Text\n"

    for dialogue in dialogues:
        for sentence in dialogue.sentences:
            sentence = parse_formatting_in_sentence(sentence, "*", "*")
            string += "{0.id}|{0.description}|{1.speaker}|{1.text}\n".format(dialogue, sentence)
    
    return string
