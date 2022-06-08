import logging
from Dictionary import dictionary

class dictionaryFactory:

    WORDLEWORDLENGTH = 5

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def createFromFile(self, filename="./dictionary/master10000.txt"):
        self.logger.info(f" Loading lexicon from {filename}")

        # read the entire file
        with open(filename) as f:
            lines = f.readlines()

        linedRead = len(lines)
        # now filter down the list to choose only 5 letter words
        dict = dictionary()
        for word in lines:
            # remove any white space or commas or comments in the text file
            if not "#" in word:
                cleanWord = word.replace(',',"").replace(" ","").strip()
                if len(cleanWord) == dictionaryFactory.WORDLEWORDLENGTH:
                    dict.addWord(cleanWord)


        return dict