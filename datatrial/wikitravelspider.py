import urllib2
import csv
cityname = 'Moscow'
fin = urllib2.urlopen('http://wikitravel.org/en/' + cityname)
# fin = open ('sitehtml.txt')
fout = open('desttxt/' + cityname + '1.txt', 'a')
searchstr = "<p>"
searchstrend = "</p>"

html = fin.read()
indd = 0

while (indd != -1):
	indd = html.find(searchstr, indd + 1)
	endd = html.find(searchstrend, indd + 1)
	dest = str(html[indd + len(searchstr):endd]).decode('unicode-escape').encode('utf-8').strip()
	if indd != -1:
		fout.write(dest + '\n')
		print dest + '\n'

print html
fout.close()