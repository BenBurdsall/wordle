import logging
from letterTally import letterTally
from Dictionary import dictionary
from slotContainer import slotContainer
from DictionaryFactory import dictionaryFactory
from tupleCount import tupleCount


class AI:

    BB  ="BB"
    AB = "AB"

    def __init__(self):
        self.logger  =logging.getLogger(__name__)
        self.slotcon  = slotContainer()
        self.df  = dictionaryFactory()
        self.dictionary = None
        self.masterDictionary = None
        self.done =[slotContainer.GREEN] *5



    def setDictionary(self, dictionary):
        self.dictionary = dictionary
        self.masterDictionary = dictionary.clone()

    # This is the word typed into wordle on each attempt. Returns True or False
    def enteredWord(self,guess):
        if self.dictionary is None:
            self.logger.error("entered word has been called before set dictionary")
            raise Exception("You forgot to call setDictionary")

        if not self.dictionary.isPresent(guess):
            self.logger.warning(f"entered word {guess} is not known in the dictionary")


        self.slotcon.assignWord(guess)
        return True

    # enter the feedback recived from wordle from the last guess [GREEN, GREY, GREEN, YELLOW,GREEN]
    # returns double boolean First Boolean if the word has been found, Second Boolean True if you have exhuasted the dictionary.
    def enterWordleFeedback(self,feedbackColours):

        #check for all Greens
        if feedbackColours == self.done:
            return True, False

        self.slotcon.enterFeedback(feedbackColours)

        # update the dictionary based on the feedback given
        self.dictionary = self.df.filterCurrentDictionary(self.dictionary, self.slotcon)
        noword = self.dictionary.isOutofWords()

        return False, noword


    # Choose the best remaining letters are the candidate has been fixed and updated in the cloned slotcontainer passed here
    def _chooseRemainingLetters(self,dictionary, slotcontain):
        cloneSlotContainer = slotcontain.clone()
        cloneDictionary= dictionary
        lt = dictionary.lt
        needToFind=1 # just start with a dummy value to enter the loop
        while needToFind > 0:
            # Find the most occuring letter in the free slots for the new dictionary
            freeSlots = cloneSlotContainer.freeSlots()
            tc = lt._findHighestOccrrance(freeSlots)
            needToFind = len(freeSlots) - 1
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

    # Returns the next word to try to send to Wordle. Returns nextWord , boolean. True when run out of words.
    def nextWord(self, strategy=BB):


        # The filteredDictionary Now only contains the WordContains information - so this can be removed from slotContainer for LETTERS that are fixed
        self.slotcon.removedFixedWordContains()

        if self.dictionary.isOutofWords():
            self.logger.warning("Dictionary is out of words - no more guesses")
            return None


        # choose which stratey to use: clear-and-vebose or terse!
        wordguess = self._chooseRemainingLetters(self.dictionary,self.slotcon)

        return wordguess  # False means you can keep on guessing, there are words left













