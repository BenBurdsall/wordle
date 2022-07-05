import logging
from letterTally import letterTally
from Dictionary import dictionary
from slotContainer import slotContainer
from DictionaryFactory import dictionaryFactory
from tupleCount import tupleCount
from minMaxStrategy import minMaxStrategy


class AI:

    BB  ="BB"
    AB = "AB"
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    GREY = "GREY"

    def __init__(self):
        self.logger  =logging.getLogger(__name__)
        self.slotcon  = slotContainer()
        self.df  = dictionaryFactory()
        self.dictionary = None
        self.masterDictionary = None



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

        # update the dictionary based on the feedback given
        self.dictionary = self.df.filterCurrentDictionary(self.dictionary, self.slotcon)


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
    def nextWord(self, strategy=AB):


        # The filteredDictionary Now only contains the WordContains information - so this can be removed from slotContainer for LETTERS that are fixed
        self.slotcon.removedFixedWordContains()

        if self.dictionary.isOutofWords():
            self.logger.warning("Dictionary is out of words - no more guesses")
            return None

        word  = self.dictionary.isOnlyWord()
        if word is not None:
            self.logger.info(f"There is only 1 word left in the dictionary it must be: {word}")
            return word, True

        # choose which stratey to use: clear-and-vebose or terse!
        if strategy ==AI.BB:
            wordguess = self._chooseRemainingLetters(self.dictionary,self.slotcon)
        else:
            minMax = minMaxStrategy(self.masterDictionary)
            wordguess = minMax._chooseMinMax(self.dictionary)

        return wordguess, False # False means you can keep on guessing, there are words left













