import unittest
import logging
from DictionaryFactory import dictionaryFactory
from slot import slot
from slotContainer import slotContainer

class test_slotContainer(unittest.TestCase):

    def test_constructor(self):

        slc  = slotContainer()

        slotList = slc.createSlots()

        self.assertEqual(len(slotList),5)

        slot1 = slotList[0]
        self.assertEqual(slot1.position,1)
        slot5  = slotList[4]
        self.assertEqual(slot5.position,5)

    def test_slotAssign(self):

        sl = slot(1)
        sl.assignLetter('a')
        sl.wrongLetter()
        sl.assignLetter('b')
        sl.wrongLetter()
        self.assertEqual(len(sl.cannotContainer),2)
        sl.assignLetter('c')
        sl.correctLetter()
        self.assertTrue(sl.fixed)

    def test_setFeeback(self):
        slc =slotContainer()

        slc.assignWord("voice")
        slc.setFeeback(1,True,False)  # word starts with v
        slc.setFeeback(2,False,False) # word does not contain an o
        slc.setFeeback(3,False,True,) # word does contain an i but not in 3rd position
        slc.setFeeback(4,False,False) # word does not contain a c
        slc.setFeeback(5,True,False)  # word does contain an e in the last position
        slot1 = slc.slotList[0]
        slot2 = slc.slotList[1]
        slot3 = slc.slotList[2]
        slot4= slc.slotList[3]
        slot5 = slc.slotList[4]
        self.assertTrue(slot1.fixed,"word starts with a v")
        self.assertEqual(slot1.currentLetter,'v')

        # check that o is not in the slotContainer and also not in the word
        self.assertFalse(slot2.fixed)
        self.assertTrue('o' in  slot2.cannotContainer)
        self.assertTrue('o' in slc.wordDoesNotContain)

        # check that i is not in the 3rd position but does exist in the word
        self.assertFalse(slot3.fixed)
        self.assertTrue('i' in slc.wordContains)
        self.assertTrue('i' in  slot3.cannotContainer)

        # check that slot 4 is not C anywhere
        self.assertFalse(slot4.fixed)
        self.assertTrue('c' in  slot4.cannotContainer)
        self.assertTrue('c' in slc.wordDoesNotContain)

        # check that word ends in an E
        self.assertTrue(slot5.fixed,"word ends with an e")
        self.assertEqual(slot5.currentLetter,'e')
        self.assertTrue('e' in slc.wordContains)
        self.assertEqual(len(slc.wordContains) , 3 )
        self.assertEqual(len(slc.wordDoesNotContain), 2)










if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()