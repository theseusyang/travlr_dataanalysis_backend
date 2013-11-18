import urllib2
import nltk

# fin = open ('chamonix1.txt')
# fout = open('chamoutput.txt', 'a')
# raw = fin.read()

raw = "(this is a test, European Europe Europe's skiing ski skis skied"
tokens = nltk.word_tokenize(raw)
porter = nltk.PorterStemmer()
tagged = nltk.pos_tag(tokens)
#NNP NN JJ (adj) 
tags = ['NNP', 'NN', "JJ"]
# result = []

for i in range (0, len(tagged)):
    # for j in range (0,2):
    print porter.stem(tagged[i][0])
