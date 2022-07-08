import logging
from DictionaryFactory import dictionaryFactory
from localWordleSimulator import localWordleSimulator
from Dictionary import dictionary
from AI import AI
from stats import stats



class backTest:


    #dictfile = "./dictionary/2of12-81k.txt"
    dictfile = "./dictionary/usabt.txt"

    NOGUESSES = 6

    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def loadBacktest(self):
        backList =[]

        backtestfile = "./tests/backtestcomplete.txt"
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
                guess = "tares"
                guessCount =1
                done = False
                noWords = False
                statkeeper.startClock("BB")
                while guessCount <=self.NOGUESSES and not done and not noWords:

                    ai.enteredWord(guess)
                    feedback  = localws.produceFeedback(guess)
                    done,noWords = ai.enterWordleFeedback(feedback)
                    if not done:
                        guess = ai.nextWord()
                        print(f"next guess shall be {guess}")
                    else:
                        print(f"Word found {guess}={localws.word} found in {guessCount} guesses")
                        statkeeper.addGameResult("BB",True,guessCount)
                    if noWords:
                        print("Out of words ... giving up")
                    guessCount += 1

                statkeeper.stopClock("BB")
                if not done:
                    statkeeper.addGameResult("BB", False, 0)


            print(statkeeper)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bt = backTest()
    bt.performTest()
