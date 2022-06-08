# container for all the typleCount objects - keeps the total count of all letters that can be used in different positions from the current dictionary
import logging
from tupleCount import tupleCount


class letterTally:

    def __init__(self):
        self.logger  = logging.getLogger(__name__)
        self.letterPosition = {}
        self.letterTotal = {}

    def incLetter(self,letter,position):

        key = f"{letter}-{position}"

        # check to see if letter has been seen before- if not initalise it
        if letter not in self.letterTotal:
            self.letterTotal[letter] =0
        else:
            # increment total occurance of a letter in any position - might be useful
            self.letterTotal[letter] = self.letterTotal[letter] +1

        if key not in self.letterPosition:
            self.letterPosition[key] = 1
        else:
            # increment usage of this letter at this position [1..5] in the word
            self.letterPosition[key] = self.letterPosition[key] +1


    # Finds the highest occurring frequency of letters in a given position
    # returns just the frequency
    def _findHighestOccrrance(self):
        keys = list(self.letterPosition.keys())
        firstKey = keys[0]
        # assume the first key has highest frequency
        hf  = self.letterPosition[firstKey]
        indexKey = firstKey
        for key in keys:
            cf = self.letterPosition[key]
            # if the cf frequency has higher than the recorded highest  -record a new highest and key
            if cf > hf:
                hf =cf
        return hf

    # finds all letters with a given frequency in a specific slot . Returns a list of  tupleCountObject
    def _findLettersWithFrequency(self,freq):
        letterList = []
        for key in self.letterPosition:
            cf = self.letterPosition[key]
            if cf == freq:
                split = key.split('-')
                letter = split[0]
                position = split[1]
                tc = tupleCount(letter,position,cf)
                letterList.append(tc)
        return letterList


    # selectes the best guesses (the most frequently occuring leters in the same position). Returns at least noChoices - but possibly more.
    # returns a list of tupleCountObjects
    def chooseTopLetterChoices(self, nochoices):
        topChoices = []
        found = 0
        hf = self._findHighestOccrrance()

        while found < nochoices:
            if hf == 0:
                raise Exception("There was no occurance of any letter")
            # get the single tuple or multiple tupples that make the best choices
            commonLetterList = self._findLettersWithFrequency(hf)
            noChoices = len(commonLetterList)
            if noChoices > 0:
                topChoices += commonLetterList
                found += noChoices
            hf -=1

        return topChoices









