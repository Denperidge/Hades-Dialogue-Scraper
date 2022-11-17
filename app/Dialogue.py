from re import findall

class Dialogue():

    def __init__(self, id):
        self.id = id
        self.sentences = []
    
    @property
    def description(self):
        return " ".join(split_camelcase_into_array(self.id))

    def readable(self):
        joined_sentences = "\n".join(self.sentences)
        return "--- {0} ---\n{1}".format(self.description, joined_sentences)
    
    def __str__(self):
        return self.readable()
    
    def __repr__(self):
        return self.readable()

class Sentence():
    def __init__(self, speaker="", sentence=""):
        self.speaker = speaker
        self.sentence = sentence
    
    # Create Sentence object from a string "Speaker: sentence"
    @classmethod
    def from_comment(cls, comment):
        [speaker, sentence] = comment.split(": ", 1)
        return cls(speaker, sentence)
    
    def readable(self):
        return "{0.speaker}: {0.sentence}".format(self)
    
    def __str__(self):
        return self.readable()
    
    def __repr__(self):
        return self.readable()


def split_camelcase_into_array(string):
    return findall(r"[A-Z][a-z0-9]*", string)