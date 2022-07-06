from Dictionary import dictionary
from DictionaryFactory import dictionaryFactory
import logging

logging.basicConfig(level=logging.INFO)


# PWD = "/Users/benburdsall/PycharmProjects/wordlebot"
PWD = '.'

dictfile = f"{PWD}/dictionary/mit10000.txt"
backtestfile= f"{PWD}/tests/backtest.txt"

df = dictionaryFactory()
dict = df.createFromFile(dictfile)

print(f"Dictionary 5-letter word count  = {dict.wordCount()}")

with open(backtestfile,"r") as f:
    lines = f.readlines()

count =0
for line in lines:

    clean = line.strip()
    if not dict.isPresent(clean):
        print(f"missing {clean}")
        count +=1

print(f"Total missing words {count}")