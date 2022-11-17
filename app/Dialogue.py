from re import findall

class Dialogue():

    def __init__(self):
        self.sentences = []
        self.description = ""
    
    def get_description(self):
        return self._description
    
    def set_description(self, val):
        self._description = " ".join(split_camelcase_into_array(val))

    description = property(fget=get_description, fset=set_description)

    def readable(self):
        joined_sentences = "\n".join(self.sentences)
        return "{0}\n{1}".format(self.description, joined_sentences)
    
    def __str__(self):
        return self.readable()

    def __repr__(self):
        return self.readable()
        

def split_camelcase_into_array(string):
    return findall(r"[A-Z][a-z0-9]*", string)