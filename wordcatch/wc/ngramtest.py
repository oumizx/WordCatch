import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

text = "I need to write a program in NLTK that breaks a corpus (a large collection of txt files) into unigrams, bigrams, trigrams, fourgrams and fivegrams. I have already written code to input my files into the program."
token = nltk.word_tokenize(text)
bigrams = ngrams(token,2)
trigrams = ngrams(token,3)
fourgrams = ngrams(token,4)
fivegrams = ngrams(token,5)

print (Counter(trigrams))