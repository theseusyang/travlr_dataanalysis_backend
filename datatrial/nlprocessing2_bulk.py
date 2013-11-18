# export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
import urllib2
import nltk

# use these to control which processes to execute
bscrape = False
bnltk = False
bcount = True

# get a list of cities and their countries from this file
fin = open('cities_list.txt')
citycountrylist = fin.read().split('\n')
fin.close()

# get just the city name from the above list
citylist = []
for cityindexry in citycountrylist:
    citylist.append(cityindexry.split(',')[0]) #.decode('unicode-escape').encode('utf-8').strip())

# open the file that will contain all final output
foutputfinal = open('output/alloutput.txt', 'a')

cityindex = 0 # the index of the city for id purposes 
for city in citylist[cityindex: 99]:  ######## FOR EACH CITY IN LIST ######### [2,6] process 2,3,4,5

    city = city.replace(' ', '_')
    #-----------------------------------------------------------------------------------------------
    if bscrape:    ##scrape the web and output to desttxt/beijing1.txt
        print '--------------------------start scraping THE WEB '+city+'----------------------------------'
        try:
            fin = urllib2.urlopen('http://wikitravel.org/en/' + city)
        # fin = open ('sitehtml.txt')
        except (urllib2.URLError): # if cannot find it, log it onto urlopenexception.txt
            fout_exception = open('output/exceptions/urlopenexception.txt','w')
            fout_exception.write(city + '\n')
            print 'ERROR: cant find this website!!! ' + city
        else:
            fout = open('desttxt/' + city + '1.txt', 'a')
            searchstr = "<p>"
            searchstrend = "</p>"
            html = fin.read()
            fin.close()
            indd = 0

            while (indd != -1):
                indd = html.find(searchstr, indd + 1)
                endd = html.find(searchstrend, indd + 1)
                dest = str(html[indd + len(searchstr):endd]).decode('unicode-escape').encode('utf-8').strip()
                if indd != -1:
                    fout.write(dest + '\n')
            fout.close()
            print '--------------------------SCRAPED THE WEB '+city+'----------------------------------'
    # -----------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------
    if bnltk:      ##Natural language processing for the above text save to output/keyword/beijing_keyword.txt
        print '--------------------------Start processing NLTK '+city+'-------------------------------'
        dest = city
        finkey = open('desttxt/'+dest +'1.txt')
        raw = finkey.read().replace('.', ' .').lower()
        finkey.close
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
        resultstring = ''
        fwords = open('output/nltkprocessed/'+city+'_keyword.txt', 'w')
        for i in range(0,len(result)):
            resultstring += result[i]

            if i < len(result)-1:
                resultstring += ','

        fwords.write(resultstring)
        fwords.close()
        print '--------------------------Processed NLTK '+city+'----------------------------------'
    # -----------------------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------------------
    if bcount:
        print '--------------------------------Get categories----------------------------------------'
        ### snowsport,beach,nature,history,culture,food,shop, nightlife
        fincat = open('schema/categories.txt')  #get the list of categories from file
        categories = fincat.read().replace(' ', '').split(',')
        fincat.close()

        keywordlist = []
        catcount = []

        for cat in categories:  #got to each characteristics word file and put it into a list
            fin = open('keywordlist/'+cat+'.txt','r')
            keywordlist.append(fin.read().replace(' ', '').split(','))
            fin.close()
            catcount.append(0)

        print '--------------------------Finished getting categories----------------------------------'
    #-----------------------------------------------------------------------------------------------
    if bcount:
        print '--------------------------Start Calculate keyword hit rate '+city+'----------------------------------'
        result = open('output/nltkprocessed/'+city+'_keyword.txt', 'r').read().split(',')

        for word in result:     # count the number of keywords that appeared for each cat 
            for index, ilist in enumerate(keywordlist):
                for keyword in ilist:
                    if word == keyword:
                        catcount[index] += 1 

        foutputfinal.write('{\n')
        foutputfinal.write('  id:' + str(cityindex) + 
            ',\n  name: \''+citycountrylist[cityindex]+ '\'' +
            ',\n  photourl: \''+ city.lower()+'1.jpg\''+
            ',\n  weather: {0:[53,39],1:[44,33],2:[44,33],3:[48,33],4:[51,37],5:[57,41],6:[60,46],7:[64,50],8:[64,48],9:[60,44],10:[53,41],11:[48,35]}' +
            ',\n  flight_price: 1000' +
            ',\n  characteristics: {\n    '
            )
        for i in range(0, len(categories)):
            foutputfinal.write(categories[i] +':' + str(float(catcount[i])/float(len(result))))
            if i < len(categories) - 1:
                foutputfinal.write(',')
            print categories[i] +':' + str(float(catcount[i])/float(len(result))) + ','
        foutputfinal.write('\n  }\n},\n')
        cityindex += 1
        print '--------------------------Finish Calculate keyword hit rate '+city+'--------------------------------'
foutputfinal.close()
  # {
  #   id:1,
  #   name: 'Aberdeen, Scotland, UK',
  #   photourl: 'scotland1.jpg',
  #   weather: {0:[53,39],1:[44,33],2:[44,33],3:[48,33],4:[51,37],5:[57,41],6:[60,46],7:[64,50],8:[64,48],9:[60,44],10:[53,41],11:[48,35]},
  #   flight_price: 1000,
  #   characteristics: {
  #     snowsport:0.0,beach:0.0,nature:0.0434782608696,history:0.0144927536232,culture:0.0434782608696,food:0.0,shop:0.0048309178744
  #   }
  # },
