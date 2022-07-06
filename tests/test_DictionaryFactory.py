import unittest
import logging
from DictionaryFactory import dictionaryFactory
from Dictionary import dictionary
from slotContainer import slotContainer
from localWordleSimulator import localWordleSimulator
import os
import random

import os

home = os.environ['HOME']

PWD = f"{home}/PycharmProjects/wordlebot"

logging.basicConfig(level=logging.INFO)

class test_DictionaryFactory(unittest.TestCase):


    def _loadDict(self):

        df = dictionaryFactory()
        filename = f"{PWD}/dictionary/master10000.txt"
        dict = df.createFromFile(filename)
        return dict




    def test_constructor(self):

        df= dictionaryFactory()
        filename = f"{PWD}/tests/testdict.txt"
        dict = df.createFromFile(filename)
        for w in dict.lexicon:
            if not len(w) == 5 :
                self.assertTrue(False,f"word was wrong length {w}")
                return


        self.assertEqual(len(dict.lexicon),4)

        cachedLines  = df._readWordsFromCacheCleanFile(filename)
        self.assertEqual(len(cachedLines),4,"the cached file should have the same number of rows as the clean file")
        for w in dict.lexicon:
          self.assertTrue((w in cachedLines),f" expecting {w} to be found in the cache file")

        self.assertTrue(df._useCachedDictionary(filename),"The stored cached value should equal the calculated hash value of the source file")

        # This should now read from the cached file
        dfc = dictionaryFactory()
        cachDict = dfc.createFromFile(filename)
        self.assertEqual(len(cachDict.lexicon), len(dict.lexicon),"the dictionary when loaded from the cache should contain the same number as the original dictionary")
        for w in dict.lexicon:
            self.assertTrue((w in cachDict.lexicon), f" expecting {w} to be found in the dictionary which was loaded from the cache")



     # checks to make sure there is no letter in the dictionary of words
    def _detectLetter(self,dict, letterList):
        for word in dict:
            for letter in letterList:
                if letter in word:
                    print(f"Hello, found letter {letter} in {word}")
                    return False

        return True


    def test_dictionaryfiltering(self):

        print("Testing filtering running")
        df = dictionaryFactory()
        filename = f"{PWD}/tests/testdict_large.txt"
        dict = df.createFromFile(filename)
        searchword = "whity"
        slc = slotContainer()

        slc.assignWord("whack")
        slc.setFeeback(1, True, False)  # word starts with w
        slc.setFeeback(2, True, False)  # 2nd letter starts with a h
        slc.setFeeback(3, False, False)  # there is no a
        slc.setFeeback(4, False, False)  # there is no c
        slc.setFeeback(5, False, False)  # there is no k
        fileredDictionary = df.filterCurrentDictionary(dict,slc)

        self.assertTrue(self._detectLetter(fileredDictionary.lexicon,['a','c','k']),"the lexicon should not contain these letters")
        slc.assignWord("whyte")
        slc.setFeeback(1, True, False)  # word starts with w
        slc.setFeeback(2, True, False)  # 2nd letter starts with a h
        slc.setFeeback(3, False, True)  # there is a y but not in 3rd position
        slc.setFeeback(4, True, False)  # there is a t is this place
        slc.setFeeback(5, False, False)  # there is no e
        fileredDictionary = df.filterCurrentDictionary(fileredDictionary, slc)
        self.assertTrue(self._detectLetter(fileredDictionary.lexicon, ['a', 'c', 'k','e']),
                        "the lexicon should not contain these letters")



    def test_andreError(self):


        print("Testing the Andre issue")
        df = dictionaryFactory()
        dict = self._loadDict()
        ls= localWordleSimulator(dict)
        ls.setSecretWord('rawly')
        self.assertTrue(dict.isPresent("rawly"))
        guessWord1 = 'oates'
        feedback = ls.produceFeedback(guessWord1)
        afeedback = ['GREY', 'GREEN', 'GREY', 'GREY', 'GREY']
        self.assertEqual(feedback,afeedback, "local simulator didnt return the correct list")
        slc = slotContainer()
        slc.assignWord('oates')
        slc.enterFeedback(afeedback)
        fileredDictionary = df.filterCurrentDictionary(dict, slc)
        self.assertFalse(fileredDictionary.isPresent('nirly'))
        self.assertTrue(fileredDictionary.isPresent("rawly"))


    def test_filterMethods(self):

        print("***********Testing Filter method comparison ************")
        for trial in range(0,200):

            df = dictionaryFactory()
            dict = self._loadDict()
            master = dict.clone()
            ls = localWordleSimulator(dict)

            wordsremaining  =5
            while(wordsremaining > 1):
                noItems = dict.wordCount() - 1
                index = random.randint(0, noItems)
                guessWord = dict.lexicon[index]
                print(f"Now guessing with : {guessWord} ")
                feedback = ls.produceFeedback(guessWord)
                slc = slotContainer()
                slc.assignWord(guessWord)
                slc.enterFeedback(feedback)
                BBdict = df.filterCurrentDictionary(dict, slc)

                ABdict = df.filterCurrentDictionaryOnFeedback(dict,guessWord,feedback)

                result = BBdict.isEqual(ABdict)

                wordsremaining = len(BBdict.lexicon)
                print(f"Master dictionary size {len(master.lexicon)}, Before filtering {len(dict.lexicon)}, then after filtering {wordsremaining}")
                self.assertTrue(result, f"The dictionaries diverged after filtering word {guessWord}")
                dict = BBdict
            print(f"Final word was {dict.lexicon[0]}")



    def test_cacheDict(self):

        print("comparing dictionary methods")
        df= dictionaryFactory()
        filename = f"{PWD}/tests/testdict.txt"
        cv = filename[:-3]+'val'
        if os.path.exists(cv):
            os.remove(cv)

        result = df._useCachedDictionary(filename)
        self.assertFalse(result,"the dictionary should not be cached")
        self.assertTrue(os.path.exists(cv),"an initialised cache file should exist")
        with open(cv, "r") as f:
            r = f.readline()

        content = str(r).strip()
        self.assertEqual(content,"0")






if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()