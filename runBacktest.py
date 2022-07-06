import logging
from DictionaryFactory import dictionaryFactory
from localWordleSimulator import localWordleSimulator
from Dictionary import dictionary
from AI import AI
from stats import stats



class backTest:


    dictfile = "./dictionary/master10000.txt"


    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def loadBacktest(self):
        backList =[]

        backtestfile = "./tests/backtest.txt"
        with open(backtestfile, "r") as f:
            lines = f.readlines()
        count = 0
        for line in lines:
            backList.append(line.strip())
            count +=1
        self.logger.info(f"Back list contains {count} words")
        return  backList

    def performTest(self):

            backList = self.loadBacktest()
            df = dictionaryFactory()
            dict = df.createFromFile(self.dictfile)
            print(f"Dictionary 5-letter word count  = {dict.wordCount()}")
            localws = localWordleSimulator(dict)
            statkeeper = stats()
            statkeeper.registerStrategy("BB")
            statkeeper.registerStrategy("AB")

            for secretWord in backList:
                #secretWord='rebut'
                localws.setSecretWord(secretWord)

                # Play a single game
                ai = AI()
                ai.setDictionary(dict)
                print(f"******Starting new game - Trying to find secret word {localws.word} with a dictionary of {dict.wordCount()} words *********")
                guess = "stair"
                guessCount = 6
                done = False
                noWords = False
                while guessCount > 0 and not done and not noWords:
                    ai.enteredWord(guess)
                    guessCount -= 1
                    feedback  = localws.produceFeedback(guess)
                    done,noWords = ai.enterWordleFeedback(feedback)
                    if not done:
                        guess = ai.nextWord()
                        print(f"next guess shall be {guess}")
                    else:
                        guesses = 5-guessCount
                        print(f"Word found {guess}={localws.word} found in {guesses} guesses")
                        statkeeper.addGameResult("BB",True,guesses)
                    if noWords:
                        print("Out of words ... giving up")

                if not done:
                    statkeeper.addGameResult("BB", False, 0)

            print(statkeeper)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bt = backTest()
    bt.performTest()
