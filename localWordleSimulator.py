from Dictionary import dictionary
import logging
import random
from AI import AI


class localWordleSimulator:

    GREEN = "GREEN"
    YELLOW = "YELLOW"
    GREY = "GREY"

    def __init__(self,dictionary):
        self.logger = logging.getLogger(__name__)
        lexicon = dictionary.lexicon
        noItems = len(lexicon) -1
        index = random.randint(0,noItems)
        self.word = lexicon[index].lower()
        print(f"Picking the Secret word: {self.word.upper()} ")
    
    def setSecretWord(self,word):
        self.word = word.lower()
        print(f"Secret word set to: {self.word.upper()} ")

    # produces a five letter [AI.Green, AI.YELLOW ...] feedback based on the guess closeness  to the secret word
    def produceFeedback(self,guessin):
        guess = guessin.lower()
        if not len(guess) == 5:
            raise Exception(f"Guessed word {guess} is not 5 characters long")
        feedback = []
        for position in range(0,5):
            if guess[position] == self.word[position]:
                feedback.append(localWordleSimulator.GREEN)
            elif guess[position] in self.word:
                feedback.append(localWordleSimulator.YELLOW)
            else:
                feedback.append(localWordleSimulator.GREY)
        return feedback
