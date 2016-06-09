import urllib2
from BeautifulSoup import BeautifulSoup

key = 'django'
location = 'San+Francisco%2C+CA'
url = 'https://www.dice.com/jobs?q=' +key + '&l=' + location + '&searchid=7665648499969'


def writehtml(a,string):
    fo = open(str(a) + '.html',"wb")
    fo.write(string)
    fo.close()

text = urllib2.urlopen(url).read()
soup = BeautifulSoup(text)
data = soup.findAll('div',attrs={'class':'serp-result-content'})
a = 1

page = url
html = urllib2.urlopen(page).read()
writehtml(a,html)

#for i in data:
    #page = str(i.h3.a.get('href'))
    #page = url
    #page = i.h3.a.get('href')
    #html = urllib2.urlopen(page).read()
    #writehtml(a,html)
    #a += 1

