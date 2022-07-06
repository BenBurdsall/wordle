from letterTally import letterTally


class dictionary:

    WORDLEWORDLENGTH = 5
    def __init__(self):
        self.lexicon = []
        self.filename = None
        self.lt = letterTally()
        self.hashValue = 0

    def clone(self):
        cloneDict = dictionary()
        cloneDict.lexicon = self.lexicon.copy()
        return cloneDict

    def isEqual(self,otherDict):
        n1 = len(self.lexicon)
        n2 = len(otherDict.lexicon)
        if not n1 == n2:
            return False
        for word in self.lexicon:
            if word not in otherDict.lexicon:
                return False
        return True


    # loads the passed list of words as the lexicon
    def setDictionary(self, wordlist):
        self.lexicon = wordlist

    def setFileName(self,file):
        self.filename = file

    def isPresent(self,wordin):
        word = wordin.lower()
        return word in self.lexicon

    def addWord(self, wordin):
        word = wordin.lower()

        if not len(word) == dictionary.WORDLEWORDLENGTH:
            raise Exception(f"A word with the wrong legnth was added to the dictionary {word}")
        # dont let any duplicates in
        if word not in self.lexicon:
            # for each new word in dictionary - add the tally of the letter
            for position in range(1,6):
                letter = word[position -1]
                self.lt.incLetter(letter,position)
            self.lexicon.append(word)

    # returns True if there are no words in the dictionary
    def isOutofWords(self):
        return len(self.lexicon)==0

    def isOnlyWord(self):
        if len(self.lexicon) == 1:
            return self.lexicon[0]
        return None

    def wordCount(self):
        return len(self.lexicon)