import logging
from slot import slot
import copy



class slotContainer:

    WORDLEWORDLENGTH = 5

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.wordDoesNotContain =[]
        # used to store letter that are present in word and it may have a repeated letter too!
        self.wordContains = []
        self.feedbackedExpected = False
        self.createSlots()
        self.assignedWord = ""

    # if the slots have been fixed these letters can be removed from wordContains information
    def removedFixedWordContains(self):
        for slot in self.slotList:
            if slot.fixed:
                letter = slot.currentLetter
                if letter in self.wordContains:
                    self.wordContains.remove(letter)

    # returns an ordered list [1..5] of slots positions that are not FIXED
    def freeSlots(self):
        fsList = []
        for slot in self.slotList:
            if not slot.fixed:
                position= slot.position
                fsList.append(position)
        return fsList

    # forms a five letter word based on current slotcontainer
    def makeWordFromSlots(self):
        word =""
        for slot in self.slotList:
            word = word + slot.currentLetter
        return word

    # creates a new copy of itself
    def clone(self):
        cl = slotContainer()
        cl.wordContains = self.wordContains.copy()
        cl.wordDoesNotContain =self.wordDoesNotContain.copy()
        cl.assignedWord = self.assignedWord
        cl.slotList = []
        for slot in self.slotList:
            cloneSlot = slot.clone()
            cl.slotList.append(cloneSlot)

        return cl


        # initiates a blank word of slots
    def createSlots(self):
        self.slotList = []
        for count in range(1,slotContainer.WORDLEWORDLENGTH+1):
            s = slot(count)
            self.slotList.append(s)
        return self.slotList

    # Assigns a new trial word to the slot container, this will fill each of the slot in turn.  You must call setFeedback method before calling this again
    def assignWord(self,wordInput):
        word = wordInput.lower()
        # Eveery time you assign a word - it clears the memory, as you need to provide feedback after
        self.createSlots()
        if not len(word) == slotContainer.WORDLEWORDLENGTH:
            raise Exception(f"You cannot assignword {word} as it is not right length ")

        if self.feedbackedExpected:
            raise Exception("You cannot assignWord a second time without calling setFeedback inbetween")

        self.feedbackedExpected = True

        self.assignedWord = word

        # as we dealing with list positions index starts at 0 and not at 1
        for index in range(0,slotContainer.WORDLEWORDLENGTH):
            slo = self.slotList[index]
            if not slo.fixed:
                slo.assignLetter(word[index])

    # sets a letter to a given slot position [1..5]
    def assignLetterToSlot(self,position, letter):
        slo = self.slotList[position - 1]
        slo.assignLetter(letter)

    # used to temporary to fix a letter to a given slot - in cloning
    def setCandidate(self,position,letter):
        slot = self.slotList[position-1]
        if not slot.position == position:
            self.logger.error("SetCandidate was changing a slot in the wrong position")
            raise  Exception("SetCandidate and SlotList is out of sync")
        slot.fixed=True
        slot.currentLetter =letter


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




