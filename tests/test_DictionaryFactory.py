import unittest
import logging
from DictionaryFactory import dictionaryFactory


class test_DictionaryFactory(unittest.TestCase):

    def test_constructor(self):

        df= dictionaryFactory()
        filename = "./tests/testdict.txt"
        dict = df.createFromFile(filename)
        for w in dict.lexicon:
            if not len(w) == 5 :
                self.assertTrue(False,f"word was wrong length {w}")
                return


        self.assertEqual(len(dict.lexicon),4)





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()