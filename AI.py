import logging
from letterTally import letterTally
from Dictionary import dictionary
from slotContainer import slotContainer
from DictionaryFactory import dictionaryFactory
from tupleCount import tupleCount


class AI:

    GREEN = "GREEN"
    YELLOW = "YELLOW"
    GREY = "GREY"

    def __init__(self):
        self.logger  =logging.getLogger(__name__)
        self.slotcon  = slotContainer()
        self.df  = dictionaryFactory()
        self.dictionary = None



    def setDictionary(self, dictionary):
        self.dictionary = dictionary

    # This is the word typed into wordle on each attempt
    def enteredWord(self,guess):
        if self.dictionary is None:
            self.logger.error("entered word has been called before set dictionary")
            raise Exception("You forgot to call setDictionary")

        if not self.dictionary.isPresent(guess):
            self.logger.warning(f"enteered word {guess} is not known in the dictionary")

        self.slotcon.assignWord(guess)

    # enter the feedback recived from wordle from the last guess [GREEN, GREY, GREEN, YELLOW,GREEN]
    # returns False is out of words
    def enterWordleFeedback(self,feedbackColours):
        if not len(feedbackColours) == 5:
            self.logger.error(f"Feedback didnt contain all 5 answers:  received {len(feedbackColours)}")
            raise Exception("Feedback was not correct length")

        position = 1
        for entry  in feedbackColours:
            if entry == AI.GREEN:
                self.slotcon.setFeeback(position,True,False)
            elif entry ==AI.YELLOW:
                self.slotcon.setFeeback(position,False,True)
            else:
                self.slotcon.setFeeback(position,False,False)
            position +=1






    # Choose the best remaining letters are the candidate has been fixed and updated in the cloned slotcontainer passed here
    def _chooseRemainingLetters(self,dictionary, slotcontain,needToFind):
        cloneSlotContainer = slotcontain.clone()
        cloneDictionary= dictionary
        lt = dictionary.lt
        while needToFind > 0:
            # Find the most occuring letter in the free slots for the new dictionary
            freeSlots = cloneSlotContainer.freeSlots()
            tc = lt._findHighestOccrrance(freeSlots)
            needToFind = slotContainer.WORDLEWORDLENGTH - len(freeSlots) - 1
            self.logger.info(f"The most likely letter is {tc} . There are {needToFind} additional free letters")
            # Now the best letter has been chosen - remove that position from the free Slots
            cloneSlotContainer.setCandidate(tc.position, tc.letter)
            # generate a dictionary - assuming that are best guess letter is correct
            cloneDictionary = self.df.filterCurrentDictionary(cloneDictionary, cloneSlotContainer)
            onlyWord = cloneDictionary.isOnlyWord()
            if onlyWord is not None:
                self.logger.info(f"According to dictionary the word must be: {onlyWord}")
                return onlyWord
            lt = cloneDictionary.lt

        guess = cloneSlotContainer.makeWordFromSlots()
        return guess

    # Returns the next word to try to send to Wordle
    def nextWord(self):

        fileredDictionary = self.df.filterCurrentDictionary(self.dictionary, self.slotcon)

        # The filteredDictionary Now only contains the WordContains information - so this can be removed from slotContainer for LETTERS that are fixed
        self.slotcon.removedFixedWordContains()

        if fileredDictionary.isOutofWords():
            self.logger.warning("Dictionary is out of words - no more guesses")
            return False

        wordguess = self._chooseRemainingLetters(fileredDictionary,self.slotcon,needToFind)
        self.dictionary = fileredDictionary








