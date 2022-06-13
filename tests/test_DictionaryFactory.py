import unittest
import logging
from DictionaryFactory import dictionaryFactory
import os


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







    def test_cacheDict(self):

        df= dictionaryFactory()
        filename = "./tests/testdict.txt"
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