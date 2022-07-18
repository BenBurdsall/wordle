from doctest import master
import logging
import sys
import math
import time

import numpy as np

from functools import reduce
from enum import Enum

from Dictionary import dictionary
from DictionaryFactory import dictionaryFactory as df
from localWordleSimulator import localWordleSimulator as sim

PWD = '.'

class OptimisationFunction(Enum):
    MAX_PARTITION_SIZE = 1
    INFORMATION_GAIN = 2

class minMaxStrategy:

    def __init__(self, masterdictionary, optimisation_function=OptimisationFunction.INFORMATION_GAIN):
        self.logger = logging.getLogger(__name__)
        self.master = masterdictionary.clone()
        self.opt = optimisation_function

        # set up letter mapping and index all words
        words = masterdictionary.lexicon
        letters = reduce(lambda s,w: s | set(w), words, set())
        self.idx_letter = list(map(lambda l: ord(l), letters))
        self.letter_idx = dict((l, i) for i, l in enumerate(self.idx_letter))
        self.index = dict((w, self.indexWord(w)) for w in words)


    # def indexWord(self, word):
    #     w = np.array([self.letter_idx[ord(word[i])] for i in range(5)], np.uint8)
    #     m = np.zeros((5, len(self.idx_letter)), np.uint16)
    #     for i in range(5):
    #         l = w[i]
    #         m[i,l] = 2*(3**i)
    #         for j in range(5):
    #             m[j,l] = max((3**j), m[j,l])
    #     return (w,m)


    def indexWord(self, word):
        w = [self.letter_idx[ord(word[i])] for i in range(5)]
        m = [[0 for _ in range(len(self.idx_letter))] for _ in range (5)]
        for i in range(5):
            l = w[i]
            m[i][l] = 2*(3**i)
            for j in range(5):
                m[j][l] = max((3**j), m[j][l])
        return (w, m)
    

    # def mapWord(self, word):
    #     return [self.letter_idx[ord(word[i])] for i in range(5)]
    

    # def scoreWord(self, word, active_idx, active_set):
    #     query_word = self.mapWord(word)
    #     partitions = [0] * (3**5)

    #     for active_word in active_idx:
    #         idx = 0
    #         idx += active_word[0][query_word[0]]
    #         idx += active_word[1][query_word[1]]
    #         idx += active_word[2][query_word[2]]
    #         idx += active_word[3][query_word[3]]
    #         idx += active_word[4][query_word[4]]
    #         partitions[idx] += 1

    #     # score a word based on how much it will reduce the active set size
    #     if self.opt == OptimisationFunction.MAX_PARTITION_SIZE:
    #         score = len(active_set) - max(partitions) 
    #     elif self.opt == OptimisationFunction.INFORMATION_GAIN:
    #         t = float(sum(partitions))
    #         f = filter(lambda x: x>0, partitions)
    #         score = reduce(lambda h,n: h - (float(n)/t)*math.log2(float(n)/t), f, 0)
    #     return float(score) + (0.1**(6) if word in active_set else 0)
    

    def nextWord3(self, filteredDictionary, show_progress=False):
        master = self.master.lexicon
        active_idx = list(map(lambda x: self.index[x][1], filteredDictionary.lexicon))
        active_set = set(filteredDictionary.lexicon)

        best_word, best_score = '', 0
        # scores = map(lambda w: self.scoreWord(w, active_idx, active_set), master)
        for p, word in enumerate(master):
            q = self.index[word][0]
            partitions = np.array([a[0,q[0]] + a[1,q[1]] + a[2,q[2]] + a[3,q[3]] + a[4,q[4]] for a in active_idx], np.uint16)
            partitions = np.bincount(partitions, minlength=(3**5))

            # score a word based on how much it will reduce the active set size
            if self.opt == OptimisationFunction.MAX_PARTITION_SIZE:
                score = len(active_set) - np.amax(partitions) 
            elif self.opt == OptimisationFunction.INFORMATION_GAIN:
                t = float(np.sum(partitions))
                score = reduce(lambda h,n: h - (float(n)/t)*math.log2(float(n)/t), partitions[partitions>0], 0)

            # prefer words in active set in case score is tied
            if (score > best_score) or (score == best_score and word in active_set): 
                best_word, best_score = word, score

            if show_progress:
                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%%" % ('='*int((20*p)/(len(master)-1)), (100*p)/(len(master)-1)))
                sys.stdout.flush()

        if show_progress:
            sys.stdout.write('\n')
            print('Best word: {}'.format(best_word))
            print('Best score: {}'.format(best_score))
        return best_word


    def nextWord2(self, filteredDictionary, show_progress=False):
        active_idx = list(map(lambda x: self.index[x][1], filteredDictionary.lexicon))
        active_set = set(filteredDictionary.lexicon)

        best_word, best_score = '', 0
        for p, (word, (query_word, _)) in enumerate(self.index.items()):
            # query_word = self.index[word][0] 
            # query_word = self.mapWord(word)
            partitions = [0] * (3**5)
            for active_word in active_idx:
                idx = (active_word[0][query_word[0]] +
                       active_word[1][query_word[1]] +
                       active_word[2][query_word[2]] +
                       active_word[3][query_word[3]] +
                       active_word[4][query_word[4]])
                partitions[idx] += 1

            # score a word based on how much it will reduce the active set size
            if self.opt == OptimisationFunction.MAX_PARTITION_SIZE:
                score = len(active_set) - max(partitions) 
            elif self.opt == OptimisationFunction.INFORMATION_GAIN:
                t = float(sum(partitions))
                f = filter(lambda x: x>0, partitions)
                score = reduce(lambda h,n: h - (float(n)/t)*math.log2(float(n)/t), f, 0)

            # prefer words in active set in case score is tied
            if (score > best_score) or (score == best_score and word in active_set): 
                best_word, best_score = word, score

            if show_progress:
                sys.stdout.write('\r')
                sys.stdout.write("[%-20s] %d%%" % ('='*int((20*p)/(len(self.index)-1)), (100*p)/(len(self.index)-1)))
                sys.stdout.flush()

        if show_progress:
            sys.stdout.write('\n')
            print('Best word: {}'.format(best_word))
            print('Best score: {}'.format(best_score))
        return best_word


    def nextWord1(self, filteredDictionary, show_progress=False):

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
            if self.opt == OptimisationFunction.MAX_PARTITION_SIZE:
                score = len(active) - max(partitions) 
            elif self.opt == OptimisationFunction.INFORMATION_GAIN:
                t = float(sum(partitions))
                f = filter(lambda x: x>0, partitions)
                score = reduce(lambda h,n: h - (float(n)/t)*math.log2(float(n)/t), f, 0)

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
    dictfile = f"{PWD}/dictionary/collins279k.txt"
    testfile = f"{PWD}/tests/backtest.txt"

    df = df()
    lexicon = df.createFromFile(dictfile)

    sim = sim(lexicon)
    solver = minMaxStrategy(lexicon)
    
    f = open(testfile, "r")
    test = f.readlines()
    f.close()

    print('Dictionary size = {}'.format(len(lexicon.lexicon)))
    print('Back testing dataset size = {}'.format(len(test)))

    start = time.perf_counter()

    # we always have the same first guess
    print('Searching for best starting word...')
    start_word = solver.nextWord2(lexicon, show_progress=True) 
    print('Starting word: {}'.format(start_word))

    solved, unsolved, min_guesses, max_guesses, total_guesses = 0,0,0,0,0
    for solution in test:
        solution = solution.strip().lower()
        print('Searching for solution {}'.format(solution))
        
        lexicon = solver.master
        if not lexicon.isPresent(solution):
            print('Skipping solution {} - missing from dictionary'.format(solution))
            continue

        sim.setSecretWord(solution)
        word = start_word

        for n in range(6):

            print('Guess word number {}: {}'.format(n+1, word))
            feedback = sim.produceFeedback(word)
            print('Feedback received: {}'.format(feedback))

            if feedback == [sim.GREEN] * 5:
                print('*** Solution found in {} guesses: {} ***'.format(n+1, word))
                solved += 1
                total_guesses += n+1
                min_guesses = n+1 if min_guesses == 0 else min(min_guesses, n+1)
                max_guesses = n+1 if max_guesses == 0 else max(max_guesses, n+1)
                break

            prev_dict_size = lexicon.wordCount()
            lexicon = df.filterCurrentDictionaryOnFeedback(lexicon, word, feedback)
            new_dict_size = lexicon.wordCount()

            print('Generating guess word with {} possible words remaining...'.format(len(lexicon.lexicon)))
            word = solver.nextWord2(lexicon)

        if word != solution:
            print('*** Could not find solution for secred word: {} ***'.format(solution))
            unsolved += 1
        
    end = time.perf_counter()

    print('Backtest results summary...')
    print('\tSolved: {}'.format(solved))
    print('\tUnsolved: {}'.format(unsolved))
    print('\tMin guesses: {}'.format(min_guesses))
    print('\tMax guesses: {}'.format(max_guesses))
    print('\tAvg guesses: {}'.format(float(total_guesses) / float(solved)))
    print('\tTotal time (seconds): {:0.4f}'.format(end - start))
