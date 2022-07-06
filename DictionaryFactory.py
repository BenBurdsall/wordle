import logging
from Dictionary import dictionary
import hashlib
from os.path import exists
from slotContainer import slotContainer

class dictionaryFactory:

    WORDLEWORDLENGTH = 5



    def __init__(self):
        self.logger = logging.getLogger(__name__)


    # Andre Feeeback routine based on current dictionary, last guessed word and feedback from wordle
    def filterCurrentDictionaryOnFeedback(self,currentdictionary,word,feedback):

        green, yellow, grey = [False] * 5, list(), set()
        for i in range(5):
            if feedback[i] == slotContainer.GREEN:
                green[i] = True
            elif feedback[i] == slotContainer.YELLOW:
                yellow.append(word[i])
            elif feedback[i] == slotContainer.GREY:
                grey.add(word[i])

        filtered = []
        for w in currentdictionary.lexicon:
            match = True
            for i, l in enumerate(w):
                if (l in grey) or (green[i] == True and word[i] != l) or (green[i] == False and word[i] == l):
                    match = False
                    break
            for l in yellow:
                if l not in w:
                    match = False
                    break
            if match:
                filtered.append(w)

        filerereddict = dictionary()
        filerereddict.setDictionary(filtered)
        return filerereddict

    # Applies the hard constraints in the dictionary to filter out words that break the constraints
    def filterCurrentDictionary(self,currentDictionary, slotcontainer):
        filterDict = dictionary()

        # for each word
        for word in currentDictionary.lexicon:
            keep = True
            # First check the slot level constaints
            for slot in slotcontainer.slotList:
                position = slot.position
                wordLetter = word[position-1] #letter under test
                letter = slot.currentLetter # letter in the slot
                # if  the letter in the slot is fixed - and the letter matches the slot then keep it, otherwise drop it
                if slot.fixed:

                    if not letter  == wordLetter:
                        keep = False # essentially if the letter is a GREEN - and doesnot match then drop the letter
                        break
                else:
                    # check to see that the letter has not been marked as a Yellow in this position before
                    if wordLetter in slot.cannotContainer:
                        keep = False
                        break



            # if the word is still ok to keep for now - do more checks
            if keep:
                # Process the gray letter words - if there is a letter that has been marked gray then drop it.
                for letter in slotcontainer.wordDoesNotContain:
                    if letter in word:
                        keep = False
                        break

                # check that all YELLOW letters are present in the word
                for letter in slotcontainer.wordContains:
                    if not letter in word:
                        keep = False
                        break


                # if the word passes all the checks then keep it
                if keep:
                    filterDict.addWord(word)


        return filterDict

    def createFromFile(self, filename="./dictionary/master10000.txt"):
        dict = dictionary()
        dict.setFileName(filename)

        if self._useCachedDictionary(filename):

            cleanWordList = self._readWordsFromCacheCleanFile(filename)
            self.logger.info(f"Loading from Cached version of the file  -containing {len(cleanWordList)} 5-letter words")
            dict.setDictionary(cleanWordList)
            return dict


        self.logger.info(f" Loading lexicon from {filename}")

        # read the entire file
        with open(filename) as f:
            lines = f.readlines()

        linedRead = len(lines)
        # now filter down the list to choose only 5 letter words
        count = 0
        for word in lines:
            # remove any white space or commas or comments in the text file
            if not "#" in word:
                cleanWord = word.replace(',',"").replace(" ","").replace("+","").replace(">","").replace("'","").replace(";","").replace(" ","").strip()
                if len(cleanWord) == dictionaryFactory.WORDLEWORDLENGTH:
                    dict.addWord(cleanWord)
                count += 1

        self.logger.info(f"Total words read form file {count} of which {dict.wordCount()} are 5-letter ones")
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









