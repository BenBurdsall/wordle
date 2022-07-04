import unittest
from AI import AI
from slotContainer import slotContainer
from DictionaryFactory import dictionaryFactory
import logging
from localWordleSimulator import localWordleSimulator

PWD = "/Users/benburdsall/PycharmProjects/wordlebot"

logging.basicConfig(level=logging.INFO)

class test_AI(unittest.TestCase):


    def _loadDict(self):

        df = dictionaryFactory()
        filename = f"{PWD}/tests/testdict_large.txt"
        dict = df.createFromFile(filename)
        return dict

    def test_constructor(self):


        # search word is whity


        ai = AI()
        ai.enteredWord("wacky")
        ai.enterWordleFeedback([ai.GREY,ai.YELLOW, ai.GREEN,ai.GREEN,ai.GREY])
        slc = ai.slotcon
        sl =slc.slotList
        s1 =sl[0]
        s2  =sl[1]
        s3 = sl[2]
        s4 = sl[3]
        s5 = sl[4]
        self.assertFalse(s1.fixed)
        self.assertFalse(s2.fixed)
        self.assertTrue(s3.fixed)
        self.assertTrue(s4.fixed)
        self.assertFalse(s5.fixed)
        containsl = slc.wordContains
        self.assertEqual(containsl,['a','c','k'])

    def test_nextWord(self):
        dict  =self._loadDict()

        # search word is wield
        ai = AI()
        ai.setDictionary(dict)
        ai.enteredWord("whity")
        ai.enterWordleFeedback([ai.GREEN,ai.GREY, ai.YELLOW, ai.GREY, ai.GREY])
        guess,lastword = ai.nextWord()
        self.assertEqual(guess,"widen")
        self.assertTrue(lastword)

    def test_simulator(self):

        dictfile = f"{PWD}/dictionary/master10000.txt"

        df = dictionaryFactory()
        dict = df.createFromFile(dictfile)
        localws = localWordleSimulator(dict)
        ai = AI()
        ai.setDictionary(dict)
        guess = "range"
        guessCount = 10
        while guessCount > 0:
            ai.enteredWord(guess)
            feedback  = localws.produceFeedback()
            ai.enterWordleFeedback(feedback)
            guess, lastword = ai.nextWord()
            if lastword:
                print("Out of words")
                guessCount=0

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()