

"""
Okay time for a bit more wacky stuff
Some text is written like "Words... {#DialogueItalicFormat}More words...{#PreviousFormat}. And more"
But sometimes it is just written as "{#DialogueItalicFormat}Words..."
"""

italic = "{#DialogueItalicFormat}"
previous = "{#PreviousFormat}"

#def parse_formatting_in_dialogues(dialogues):
    
def parse_formatting_in_sentence(unparsed_sentence, replacement_open, replacement_close):
    unparsed_sentence.text = parse_formatting_in_text(unparsed_sentence.text, replacement_open, replacement_close)
    return unparsed_sentence

def parse_formatting_in_text(unparsed_text, replacement_open, replacement_close):
    if italic not in unparsed_text:
        return unparsed_text

    elif italic in unparsed_text:
        if previous in unparsed_text:
            return unparsed_text.replace(italic, replacement_open).replace(previous, replacement_close)
        else:
            return (unparsed_text.replace(italic, replacement_open) + replacement_close)
        
    
    
