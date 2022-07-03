import unittest
from AI import AI
from slotContainer import slotContainer
from DictionaryFactory import dictionaryFactory
import logging

PWD = "/Users/benburdsall/PycharmProjects/wordlebot"

logging.basicConfig(level=logging.INFO)

class test_AI(unittest.TestCase):

    def test_constructor(self):

        slc = slotContainer()

        # search word is whity
        slc.assignWord("wack")
        df = dictionaryFactory()
        filename = f"{PWD}/tests/testdict_large.txt"
        dict = df.createFromFile(filename)
        slc.setFeeback(1, True, False)  # word starts with w
        slc.setFeeback(2, False, False)
        slc.setFeeback(3, False, False)
        slc.setFeeback(4, False, False)
        slc.setFeeback(5, False, False)
        fileredDictionary = df.filterCurrentDictionary(dict, slc)

        ai = AI(slc)
        nextguess = ai.nextWord()