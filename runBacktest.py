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
        #backtestfile = "./tests/backlistrecent.txt"

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
            statkeeper.registerStrategy("BB1")
            statkeeper.registerStrategy("BB2")
            statkeeper.registerStrategy("AB")

            strategyList = ["BB1","BB2"]
            for strategy in strategyList:

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

                    statkeeper.startClock(strategy)
                    while guessCount <=self.NOGUESSES and not done and not noWords:

                        ai.enteredWord(guess)
                        feedback  = localws.produceFeedback(guess)
                        done,noWords = ai.enterWordleFeedback(feedback)
                        if not done:
                            guess = ai.nextWord(strategy)
                            print(f"next guess shall be {guess}")
                        else:
                            print(f"Word found {guess}={localws.word} found in {guessCount} guesses")
                            statkeeper.addGameResult(strategy,True,guessCount)
                        if noWords:
                            print("Out of words ... giving up")
                        guessCount += 1

                    statkeeper.stopClock(strategy)
                    if not done:
                        print(f"** Failed to find word in 6 guesses: {secretWord} ")
                        statkeeper.addGameResult(strategy, False, 0)


            print(statkeeper)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bt = backTest()
    bt.performTest()
