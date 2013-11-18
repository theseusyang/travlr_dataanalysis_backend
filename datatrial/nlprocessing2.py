# export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
import urllib2
import nltk

dest = 'moscow'
fin = open('desttxt/'+dest +'1.txt')
fout = open('output/'+ dest +'output.txt', 'w')
raw = fin.read().replace('.', ' .').lower()
fin.close()
tokens = nltk.word_tokenize(raw)
porter = nltk.PorterStemmer()
tagged = nltk.pos_tag(tokens)

tags = ['NNP', 'NN', 'JJ'] # extract only meaningful words
result = []

for itagged in tagged:  #NLTK to get a list of nouns, cleaned up
    for itag in tags:
        if itagged[1] == itag:
            result.append(porter.stem(itagged[0]))

print result
#snowsport,beach,nature,history,culture,food,shop
fincat = open('schema/categories.txt')  #get the list of categories
categories = fincat.read().replace(' ', '').split(',')
fincat.close()

keywordlist = []
catcount = []

for cat in categories:  #got to each characteristics word file and put it into a list
    fin = open('keywordlist/'+cat+'.txt')
    keywordlist.append(fin.read().replace(' ', '').split(','))
    fin.close()
    catcount.append(0)


for word in result:		# count the number of keywords that appeared for each cat 
    for index, ilist in enumerate(keywordlist):
        for keyword in ilist:
            if word == keyword:
                catcount[index] += 1 

for i in range(0, len(categories)):
    fout.write(categories[i] +':' + str(float(catcount[i])/float(len(result))) + ',')
    print categories[i] +':' + str(float(catcount[i])/float(len(result))) + ','
# print float(skicount)/float(len(result))
