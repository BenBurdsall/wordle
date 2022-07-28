import logging
import unittest

from AI import AI
from DictionaryFactory import dictionaryFactory
from Dictionary import dictionary
from localWordleSimulator import localWordleSimulator
from minMaxStrategy import minMaxStrategy

#PWD = "/Users/benburdsall/PycharmProjects/wordlebot"
PWD = '.'

logging.basicConfig(level=logging.INFO)

class test_minMaxStrategy(unittest.TestCase):

    def test_part(self):
        active = {'parly', 'rawly', 'marly', 'rally'}

        word = 'marly'
        letters = set(word)

        partitions = [0] * (3**5)
        for w in active:
            idx = 0
            for i, l in enumerate(word):
                idx *= 3
                if l in w:
                    idx += 2 if word[i] == l else 1
            partitions[idx] += 1

        # score a word based on how much it will reduce the active set size
        score = len(active) - max(partitions)
        print('{score}')


    def test_minMax(self):
        dictfile = f"{PWD}/dictionary/master10000.txt"

        df = dictionaryFactory()
        dict = df.createFromFile(dictfile)

        sim = localWordleSimulator(dict)
        solver = minMaxStrategy(dict)

        for n in range(10):
            print('Generating guess word #{}'.format(n+1))
            print('Possible words remaining: {}'.format(len(dict.lexicon)))
            word = solver.nextWord(dict)
            
            print('Guess word: {}'.format(word))
            feedback = sim.produceFeedback(word)
            print('Feedback received: {}'.format(feedback))

            green, yellow, grey = [' ']*5, list(), set()
            for i in range(5):
                if feedback[i] == AI.GREEN:
                    green[i] = word[i]
                elif feedback[i] == AI.YELLOW:
                    yellow.append(word[i])
                elif feedback[i] == AI.GREY:
                    grey.add(word[i])

            filtered = []
            for w in dict.lexicon:
                match = True
                for i,l in enumerate(w):
                    if (l in grey) or (green[i] != ' ' and green[i] != l):
                        match = False
                        break
                for l in yellow:
                    if l not in w:
                        match = False
                        break
                if match:
                    filtered.append(w)

            dict = dictionary()
            dict.setDictionary(filtered)

            if len(filtered) == 1:
                print('Solution found in {} guesses: {}'.format(n+1, filtered[0]))
                break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()