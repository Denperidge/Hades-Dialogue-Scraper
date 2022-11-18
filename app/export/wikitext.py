from export.replace import parse_formatting_in_sentence

# Reference: https://community.fandom.com/wiki/Help:Tables
# Based on https://hades.fandom.com/wiki/Zeus/Quotes?action=edit
def to_string_wikitext_table(dialogues):
    string = '{| class="wikitable"\n'
    string += '|+\n'
    for dialogue in dialogues:
        string += '! colspan="2" |{}\n'.format(dialogue.description)
        string += '|-\n'
        for sentence in dialogue.sentences:
            sentence = parse_formatting_in_sentence(sentence, "''", "''")
            string += "|'''{}'''\n".format(sentence.speaker)
            string += '|"{}"\n'.format(sentence.text)
            string += '|-\n'
    string += "|}"

    return string
    

