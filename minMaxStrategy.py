import logging
import sys
from Dictionary import dictionary
from DictionaryFactory import dictionaryFactory
from localWordleSimulator import localWordleSimulator

PWD = '.'


class minMaxStrategy:

    def __init__(self, masterdictionary):
        self.logger = logging.getLogger(__name__)
        self.master = masterdictionary.clone()

    def nextWord(self, filteredDictionary):

        master = self.master.lexicon
        active = set(filteredDictionary.lexicon)

        best_word, best_score = '', 0
        for p, word in enumerate(master):
            letters = set(word)
            partitions = [0] * (3**5)
            for w in active:
                idx = 0
                for i, l in enumerate(w):
                    idx *= 3
                    if l in letters:
                        idx += 2 if word[i] == l else 1
                partitions[idx] += 1

            # score a word based on how much it will reduce the active set size
            score = len(active) - max(partitions)
            # prefer words in active set in case score is tied
            if score + (1 if word in active else 0) > best_score: 
                best_word, best_score = word, score

            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" % ('='*int((20*p)/(len(master)-1)), (100*p)/(len(master)-1)))
            sys.stdout.flush()

        sys.stdout.write('\n')
        return best_word

if __name__ == '__main__':
    dictfile = f"{PWD}/dictionary/master10000.txt"
    backtestfile= f"{PWD}/tests/backtest.txt"    

    df = dictionaryFactory()
    dict = df.createFromFile(dictfile)

    sim = localWordleSimulator(dict)
    solver = minMaxStrategy(dict)

    for guess in range(10):
        print('Generating guess word #{}'.format(guess+1))
        print('Possible words remaining: {}'.format(len(dict)))
        word = solver.nextWord(dict)
        print('Submitting guess word: {}'.format(word))


        guess = "range"
        guessCount = 10
        while guessCount > 0:
            ai.enteredWord(guess)
            feedback  = localws.produceFeedback(guess)
            ai.enterWordleFeedback(feedback)
            guess, lastword = ai.nextWord()
            if lastword:
                print("Out of words")
                guessCount=0
