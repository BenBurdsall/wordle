import logging
import sys

from Dictionary import dictionary
from DictionaryFactory import dictionaryFactory as df
from localWordleSimulator import localWordleSimulator as sim

PWD = '.'

class minMaxStrategy:

    def __init__(self, masterdictionary):
        self.logger = logging.getLogger(__name__)
        self.master = masterdictionary.clone()

    def nextWord(self, filteredDictionary, show_progress=False):

        master = self.master.lexicon
        active = set(filteredDictionary.lexicon)

        best_word, best_score = '', 0
        for p, word in enumerate(master):
            partitions = [0] * (3**5)
            for w in active:
                idx = 0
                for i, l in enumerate(word):
                    idx *= 3
                    idx += 2 if w[i] == l else 1 if l in w else 0
                partitions[idx] += 1

            # score a word based on how much it will reduce the active set size
            score = len(active) - max(partitions)
            # prefer words in active set in case score is tied
            if (score > best_score) or (score == best_score and word in active): 
                best_word, best_score = word, score

            if show_progress:
                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%%" % ('='*int((20*p)/(len(master)-1)), (100*p)/(len(master)-1)))
                sys.stdout.flush()

        if show_progress:
            sys.stdout.write('\n')
        return best_word


if __name__ == '__main__':
    dictfile = f"{PWD}/dictionary/master10000.txt"
    testfile = f"{PWD}/tests/backtest.txt"

    df = df()
    dict = df.createFromFile(dictfile)

    sim = sim(dict)
    solver = minMaxStrategy(dict)
    
    f = open(testfile, "r")
    test = f.readlines()
    f.close()

    print('Dictionary size = {}'.format(len(dict.lexicon)))
    print('Back testing dataset size = {}'.format(len(test)))

    # we always have the same first guess
    print('Searching for best starting word...')
    start_word = solver.nextWord(dict, show_progress=True) 
    print('Starting word: {}'.format(start_word))

    for solution in test:
        solution = solution.strip().lower()
        print('Searching for solution {}'.format(solution))
        
        dict = solver.master
        if not dict.isPresent(solution):
            print('Skipping solution {} - missing from dictionary'.format(solution))
            continue

        sim.setSecretWord(solution)
        word = start_word

        for n in range(10):

            print('Guess word number {}: {}'.format(n+1, word))
            feedback = sim.produceFeedback(word)
            print('Feedback received: {}'.format(feedback))

            if feedback == [sim.GREEN] * 5:
                print('*** Solution found in {} guesses: {} ***'.format(n+1, word))
                break

            dict = df.filterCurrentDictionaryOnFeedback(dict,word,feedback)

            print('Generating guess word with {} possible words remaining...'.format(len(dict.lexicon)))
            word = solver.nextWord(dict)

        if word != solution:
            print('*** Could not find solution for secred word: {} ***'.format(solution))
