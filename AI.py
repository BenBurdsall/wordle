import logging
from letterTally import letterTally
from Dictionary import dictionary
from slotContainer import slotContainer
from DictionaryFactory import dictionaryFactory


class AI:

    GREEN = "GREEN"
    YELLOW = "YELLOW"
    "GREY" = "GREY"

    def __init__(self,slotcon):
        self.logger  =logging.getLogger(__name__)
        self.slotcon  = slotcon
        self.df  = dictionaryFactory()


    def setDictionary(self, dictionary):
        self.dictionary = dictionary

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

        oldMustContains = self.slotcon.wordContains

        fileredDictionary = self.df.filterCurrentDictionary(self.dictionary, self.slotcon)

        # The filteredDictionary Now only contains the WordContains information - so this can be removed from slotContainer for LETTERS that are fixed
        self.slotcon.removedFixedWordContains()

        if fileredDictionary.isOutofWords():
            self.logger.warning("Dictionary is out of words - no more guesses")
            return False

        self.dictionary  =fileredDictionary



        return True

    # Returns the next word to try to send to Wordle
    def nextWord(self):
        ltally = self.dictionary.lt

        assignedWord = self.slotcon.assignedWord
        if not self.dictionary.isPresent(assignedWord):
            self.logger.warning("The current assigned word: {assignedWord} is not in the current dictionary")

        onlyWord=  self.dictionary.isOnlyWord()
        if onlyWord is not None:
            self.logger.info(f"According to dictionary the word must be: {onlyWord}")
            return onlyWord


