import urllib2
import csv
fin = urllib2.urlopen('http://www.lonelyplanet.com/austria/places.json?page=1')
fin = open ('sitehtml.txt')
fout = open('austrialist.txt', 'a')
searchstr = "<h2 class='card__name js-card-name'>\\n"
searchstrend = "\\n</h2>"

html = fin.read()
nPage = int(html[-3]) # finds the total number of pages to be crawled

for i in range(2, nPage + 1):
	fin = urllib2.urlopen('http://www.lonelyplanet.com/austria/places.json?page=' + str(i))
	html = fin.read()
	indd = 0
	while (indd != -1):
		indd = html.find(searchstr, indd + 1)
		endd = html.find(searchstrend, indd + 1)
		dest = str(html[indd + len(searchstr):endd]).decode('unicode-escape').encode('utf-8').strip()
		if indd != -1:
			fout.write(dest + '\n')
			print dest + '\n'


fout.close()
