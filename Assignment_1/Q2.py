import requests
import os.path
from bs4 import BeautifulSoup as bs

NUMBER_OF_PAGES = 10
WIKI_RANDOM="https://en.wikipedia.org/wiki/Special:Random"

def download_file(link, name):
    file = open(name, 'r+')
    r = requests.get(link)
    file.write(r.text.encode('utf-8'))
    file.truncate()
    file.close()

def find_Links(page, filename):
	file = open (filename, 'r+')
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

for i in range (0,NUMBER_OF_PAGES):
	path="./File_directory/"
	file=path+"Random_%d.html" %(i)
	snowball_links =path+"Random_%d_snowballed_links.txt"%(i)
	download_file(WIKI_RANDOM,file)
	find_Links(file, snowball_links)
	#print r.text
#	soup = bs(r,'html.parser')
		
