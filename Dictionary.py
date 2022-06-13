
class dictionary:

    WORDLEWORDLENGTH = 5
    def __init__(self):
        self.lexicon = []
        self.filename = None
        self.hashValue = 0

    # loads the passed list of words as the lexicon
    def setDictionary(self, wordlist):
        self.lexicon = wordlist

    def setFileName(self,file):
        self.filename = file

    def addWord(self, word):

        if not len(word) == dictionary.WORDLEWORDLENGTH:
            raise Exception(f"A word with the wrong legnth was added to the dictionary {word}")
        # dont let any duplicates in
        if word not in self.lexicon:
            self.lexicon.append(word)