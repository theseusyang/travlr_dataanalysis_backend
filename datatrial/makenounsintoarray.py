import urllib2

fin = open('nature.txt')
words = fin.read().split(',')
fin.close()

print words
