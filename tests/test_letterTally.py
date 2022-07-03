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
        lt.incLetter('a', 2)
        lt.incLetter('a', 2)
        lt.incLetter('a', 2)
        lt.incLetter('b', 2)
        lt.incLetter('b', 2)
        lt.incLetter('b', 2)
        lt.incLetter('c', 2)
        lt.incLetter('c', 2)


        lt.incLetter('b', 3)
        lt.incLetter('b', 4)
        lt.incLetter('b', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 5)
        lt.incLetter('c', 1)


        tc= lt._findHighestOccrrance([1,2,3,4,5])
        self.assertEqual(str(tc), "a,slot=2,freq=6")
        tc = lt._findHighestOccrrance([1, 3, 4, 5])
        self.assertEqual(str(tc), "c,slot=5,freq=3")





        letterList = lt._findLettersWithFrequencyAtPosition(2, 3)

        self.assertEqual(len(letterList),1)
        tc1 = letterList[0]

        self.assertEqual(str(tc1),"b,slot=2,freq=3")


    def test_findMaxInDict(self):
        dict = {
            'a' : 15,
            'b' : 3,
            'c' : 212,
            'd': 3
         }

        lt = letterTally()
        f,l = lt._findMaxInDict(dict)
        self.assertEqual(f,212)
        self.assertEqual(l,'c')



    def test_chooseTopLetterChoices(self):
        lt = letterTally()

        lt.incLetter('a', 1)
        lt.incLetter('a', 1)
        lt.incLetter('a', 1)
        lt.incLetter('a', 1)
        lt.incLetter('b', 1)
        lt.incLetter('b', 1)
        lt.incLetter('b', 1)
        lt.incLetter('b', 1)
        lt.incLetter('c', 1)
        lt.incLetter('c', 1)
        lt.incLetter('c', 1)
        lt.incLetter('c', 1)

        letterList = lt.chooseTopLetterChoices(1,2)

        tc1 = letterList[0]
        tc2 = letterList[1]

        self.assertEqual(str(tc1), "a,slot=1,freq=4")
        self.assertEqual(str(tc2), "b,slot=1,freq=4")

        # now make c the most occuring letter and therefore the top choice
        lt.incLetter('c', 1)
        letterList = lt.chooseTopLetterChoices(1,1)

        self.assertEqual(len(letterList), 1,1)

        tc2 = letterList[0]
        self.assertEqual(str(tc2), "c,slot=1,freq=5")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()