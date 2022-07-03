# container for all the typleCount objects - keeps the total count of all letters that can be used in different positions from the current dictionary
import logging
from tupleCount import tupleCount


class letterTally:

    def __init__(self):
        self.logger  = logging.getLogger(__name__)
        self.letterPosition = {}
        self.letterTotal = {}

    # increments the count of a letter in a given poistion by 1
    def incLetter(self,letter,position):

        if not position in self.letterPosition:
            self.letterPosition[position]={}

        if not letter in  self.letterPosition[position]:
            self.letterPosition[position][letter]=1
        else:
            self.letterPosition[position][letter]+=1







    # Finds the highest occurring frequency of letters in a given position
    # returns  the frequency and the letter
    def _findHighestOccrranceAtPosition(self,position):
        keys = list(self.letterPosition[position])
        firstKey = keys[0]
        # assume the first key has highest frequency
        hf  = self.letterPosition[position][firstKey]
        letter= firstKey
        for key in keys:
            cf = self.letterPosition[position][key]
            # if the cf frequency has higher than the recorded highest  -record a new highest and key
            if cf > hf:
                hf =cf
                letter =key
        return hf,letter


    # finds the highest value in a dictionry, returns both value followed by name
    def _findMaxInDict(self,dict):
        keys = list(dict)
        firstKey = keys[0]
        hf = dict[firstKey]
        letter = firstKey
        for key in keys:
            cf = dict[key]
            # if the cf frequency has higher than the recorded highest  -record a new highest and key
            if cf > hf:
                hf =cf
                letter =key
        return hf,letter


    # Finds the highest occurring/ frequency letter aggregated across all  free slots. This works by going through each of the remaining free slots.
    # freeSlotIndexes = [1,4,5]
    # returns the tuple count consisting of the Slot position, the frequency of letter in THAT POSITION
    def _findHighestOccrrance(self,freeSlotIndexes):

        self.letterTotal = {}
        # build the letter total index
        position = 0
        hf = 0
        for si in freeSlotIndexes:
            f,l  = self._findHighestOccrranceAtPosition(si)
            # record the position where the highest letter occurred
            if f > hf:
                position  = si
                hf = f
            current = self.letterTotal.get(l,0)
            self.letterTotal[l] = current +f
        # now find most often occuring letter and frequency

        totalf,letter = self._findMaxInDict(self.letterTotal)

        # find the frequency of that letter in that position
        slotf = self.letterPosition[position][letter]

        tc = tupleCount(letter,position,slotf)

        return tc



    # finds all letters with a given frequency in a specific slot . Returns a list of  tupleCountObject
    def _findLettersWithFrequencyAtPosition(self, position, freq):
        letterList = []
        for key in self.letterPosition[position]:
            cf = self.letterPosition[position][key]
            if cf == freq:
                letter = key
                tc = tupleCount(letter,position,cf)
                letterList.append(tc)
        return letterList


    # selectes the best guesses (the most frequently occuring leters in the same position). Returns at least noChoices - but possibly more.
    # returns a list of tupleCountObjects
    def chooseTopLetterChoices(self,position, nochoices):
        topChoices = []
        found = 0
        hf,letter = self._findHighestOccrranceAtPosition(position)

        while found < nochoices:
            if hf == 0:
                raise Exception("There was no occurance of any letter")
            # get the single tuple or multiple tupples that make the best choices
            commonLetterList = self._findLettersWithFrequencyAtPosition(position, hf)
            noChoices = len(commonLetterList)
            if noChoices > 0:
                topChoices += commonLetterList
                found += noChoices
            hf -=1

        return topChoices









