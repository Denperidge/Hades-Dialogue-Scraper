from export.replace import parse_formatting_in_sentence

def to_string_txt(dialogues):
    string = ""
    for dialogue in dialogues:
        string += "---{}---\n".format(dialogue.description)

        for sentence in dialogue.sentences:
            sentence = parse_formatting_in_sentence(sentence, "*", "*")

            string += "{0.speaker}|{0.text}\n".format(sentence)
        
        string += "\n\n"
    
    return string
