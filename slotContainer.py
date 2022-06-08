import logging
from slot import slot



class slotContainer:

    WORDLEWORDLENGTH = 5

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.wordDoesNotContain =[]
        # used to store letter that are present in word and it may have a repeated letter too!
        self.wordContains = []
        self.feedbackedExpected = False
        self.createSlots()

    # initiates a blank word of slots
    def createSlots(self):
        self.slotList = []
        for count in range(1,slotContainer.WORDLEWORDLENGTH+1):
            s = slot(count)
            self.slotList.append(s)
        return self.slotList

    # Assigns a new trial word to the slot container, this will fill each of the slot in turn.  You must call setFeedback method before calling this again
    def assignWord(self,word):
        if not len(word) == slotContainer.WORDLEWORDLENGTH:
            raise Exception(f"You cannot assignword {word} as it is not right length ")

        if self.feedbackedExpected:
            raise Exception("You cannot assignWord a second time without calling setFeedback inbetween")

        self.feedbackedExpected = True

        # as we dealing with list positions index starts at 0 and not at 1
        for index in range(0,slotContainer.WORDLEWORDLENGTH):
            slo = self.slotList[index]
            if not slo.fixed:
                slo.assignLetter(word[index])

    # sets a letter to a given slot position [1..5]
    def assignLetterToSlot(self,position, letter):
        slo = self.slotList[position - 1]
        slo.assignLetter(letter)


    # give feedback from the wordle app - for a given slot, indicating if the current slot position has the correct letter
    def setFeeback(self,position,correctLetterPlace, correctLetterWrongPlace):
        if correctLetterPlace and correctLetterWrongPlace:
            raise Exception(f"You cannot set slot position {position} as both being correct letter in the right and wrong place at the same time")

        slo = self.slotList[position - 1]
        self.feedbackedExpected = False

        # We have the correct letter in the right place.
        if correctLetterPlace:

            slo.correctLetter()
            # add the current corrfect letter to the word contains list - as it may be repeated
            if slo.currentLetter not in self.wordContains:
                self.wordContains.append(slo.currentLetter)
        elif correctLetterWrongPlace:
            # mark this letter as being correct in the slot position but add it in the wordContains list - to show that it is used somewhere
            slo.wrongLetter()
            if slo.currentLetter not in self.wordContains:
                self.wordContains.append(slo.currentLetter)
        else:
            # so this letter in the slot does not exist in the word at all
            slo.wrongLetter()
            if slo.currentLetter not in self.wordDoesNotContain:
                self.wordDoesNotContain.append(slo.currentLetter)




