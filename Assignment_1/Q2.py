import requests
import os.path
from bs4 import BeautifulSoup as bs
import TFIDF_test

NUMBER_OF_PAGES = 100
WIKI_RANDOM="https://en.wikipedia.org/wiki/Special:Random"

def download_file(link, filename):
        try:
                file = open (filename, 'r+')
        except:
                file = open (filename, 'w')
    	r = requests.get(link)
    	file.write(r.text.encode('utf-8'))
    	file.truncate()
    	file.close()

def find_Links(page, filename):
	try:
		file = open (filename, 'r+')
	except:
		file = open (filename, 'w')
	with open(page) as pag: 
		soup = bs(pag.read(),'html.parser')
	all_anchors = soup.find_all('a')
	links=[]
	for link in all_anchors:
		list=link.get('href')
		if list:
			if 'html' in list:
				links.append(list.encode('utf-8'))
	file.write(str(links))
	file.truncate()
 	file.close()

def find_text(page, filename):
        try:
                file = open (filename, 'r+')
        except:
                file = open (filename, 'w')

        with open(page) as pag:
                soup = bs(pag,'xml')
	a=soup.get_text()
	start= a.find("From Wikipedia, the free encyclopedia")
	end= a.find("Retrieved fro")
	a = a[start:end]
#	print page_data
        file.write(a.encode('utf-8'))
        file.truncate()
        file.close()

### Pending: 	1. TF-IDF
###		2. Page --> Text


for i in range (0,NUMBER_OF_PAGES):
	path="./Q2_files/"
	file=path+"Random_%d.html" %(i)
	snowball_links =path+"Random_%d_snowballed_links.txt"%(i)
	text_files=path+"Random_%d_text.txt"%(i)
	download_file(WIKI_RANDOM,file)
	find_Links(file, snowball_links)
	find_text(file, text_files)
#	TFIDF_test.TFIDF("./Q2_files/Random_*text.txt", "./Q2_TFIDF")		
