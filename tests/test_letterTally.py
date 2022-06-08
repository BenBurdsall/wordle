import unittest
import logging
from DictionaryFactory import dictionaryFactory
from slot import slot
from slotContainer import slotContainer
from letterTally import letterTally


class test_letterTally(unittest.TestCase):

    def test_incLetter(self):

        lt = letterTally()

        lt.incLetter('a',1)
        lt.incLetter('a', 2)
        lt.incLetter('a', 2)
        lt.incLetter('a', 2)
        lt.incLetter('b', 2)
        lt.incLetter('b', 3)
        lt.incLetter('b', 4)
        lt.incLetter('b', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 1)


        freq= lt._findHighestOccrrance()
        self.assertEqual(freq, 3,"There are a total of 3 a in position 2 and 3 of c in 5")

        letterList = lt._findLettersWithFrequency(3)

        self.assertEqual(len(letterList),2)
        tc1 = letterList[0]
        tc2 = letterList[1]

        self.assertEqual(str(tc1),"a,slot=2,freq=3")
        self.assertEqual(str(tc2),"c,slot=5,freq=3")


    def test_chooseTopLetterChoices(self):
        lt = letterTally()

        lt.incLetter('a', 1)
        lt.incLetter('a', 2)
        lt.incLetter('a', 2)
        lt.incLetter('a', 2)
        lt.incLetter('b', 2)
        lt.incLetter('b', 3)
        lt.incLetter('b', 4)
        lt.incLetter('b', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 1)

        letterList = lt.chooseTopLetterChoices(1)

        self.assertEqual(len(letterList),2)

        tc1 = letterList[0]
        tc2 = letterList[1]

        self.assertEqual(str(tc1), "a,slot=2,freq=3")
        self.assertEqual(str(tc2), "c,slot=5,freq=3")

        # now make c the most occuring letter and therefore the top choice
        lt.incLetter('c', 5)
        letterList = lt.chooseTopLetterChoices(1)

        self.assertEqual(len(letterList), 1)

        tc2 = letterList[0]
        self.assertEqual(str(tc2), "c,slot=5,freq=4")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()