import logging
from Dictionary import dictionary
import hashlib
from os.path import exists

class dictionaryFactory:

    WORDLEWORDLENGTH = 5

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def createFromFile(self, filename="./dictionary/master10000.txt"):
        dict = dictionary()
        dict.setFileName(filename)

        if self._useCachedDictionary(filename):
            self.logger.info("Loading from Cached version of the file")
            cleanWordList = self._readWordsFromCacheCleanFile(filename)
            dict.setDictionary(cleanWordList)
            return dict


        self.logger.info(f" Loading lexicon from {filename}")

        # read the entire file
        with open(filename) as f:
            lines = f.readlines()

        linedRead = len(lines)
        # now filter down the list to choose only 5 letter words

        for word in lines:
            # remove any white space or commas or comments in the text file
            if not "#" in word:
                cleanWord = word.replace(',',"").replace(" ","").strip()
                if len(cleanWord) == dictionaryFactory.WORDLEWORDLENGTH:
                    dict.addWord(cleanWord)

        # now write a stripped down version file with only the clean 5 letter words
        self._writeCleanDictionaryAsCache(dict)
        return dict

    # reads the words from a cached file, returns a list of words or None if the file does not exist
    def _readWordsFromCacheCleanFile(self,filename):
        cachevaluefile = filename[:-3] + 'clean'
        if not exists(cachevaluefile):
            return None

        with open(cachevaluefile) as f:
            lines = f.read().splitlines()

        return lines

    # writes the current cleanr dictionary as a cached file - so only contains 5 letters words etc...
    def _writeCleanDictionaryAsCache(self, dictionary):

        dictname = dictionary.filename

        cachevaluefile = dictname[:-3] + 'clean'
        with open(cachevaluefile, "w") as f:
            for word  in dictionary.lexicon:
                f.write(f"{word}\n")

        # calculate hash of current dictionary SOURCE file
        dictionary.hashValue = self._calculateHash(dictname)
        self._writeCacheValue(dictname,dictionary.hashValue)



    # Writes the the hex cache value of the soruce dictionary file
    def _writeCacheValue(self,filename, hashValue):
        cachevaluefile = filename[:-3]+  'val'


        with open(cachevaluefile, "w") as f:
            f.write(hashValue)


    def _calculateHash(self,filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        h = str(hash_md5.hexdigest())
        return h

    def _useCachedDictionary(self, filename):

        cachevaluefile = filename[:-3] + 'val'

        h = self._calculateHash(filename)


        # check to see if the cache file exists - if not create a blank one

        file_exists = exists(cachevaluefile)
        if not file_exists:
            self._writeCacheValue(filename,"0")
            return False

        with open(cachevaluefile, "r") as f:
            cachehash = f.readline()

        self.logger.info(f"dictionary seen before cached value was {cachehash}, current hash value of dictionary is {h}")

        if cachehash == h:
            return True

        return False









