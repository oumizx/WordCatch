import nltk
from nltk.util import ngrams
f = open('test.txt')
raw = f.read()

tokens = nltk.word_tokenize(raw)

#Create your bigrams
bgs = nltk.bigrams(tokens)
trigrams = ngrams(tokens,3)

#compute frequency distribution for all the bigrams in the text
fdist = nltk.FreqDist(trigrams)
for k,v in fdist.items():
    if (v > 20):
        print (k,v)