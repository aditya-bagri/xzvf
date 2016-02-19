### Author: 	Maanit Mehra
### Date:	18th Feb, 2016
###
###
### Code created for Assignment 1 of Advanced Big Data
###
###
### This code acquired data from a 100 random wikipedia pages 
### and saves this to a set of files stored separately.
### This is a precursor for TFIDF_Q2.py
### This program only prepares the files for the TF-IDF calculations later.

import requests
import os.path
from bs4 import BeautifulSoup as bs
import os

NUMBER_OF_PAGES = 100
WIKI_RANDOM="https://en.wikipedia.org/wiki/Special:Random"

def find_urls(i, page, filename):
        try:
                file = open (filename, 'a')
        except:
                file = open (filename, 'w')
		file.write("Doc_Num\tLink")
	with open(page, 'r+') as pag:
        	soup = bs(pag.read(),'html.parser')
        all_links = soup.find_all('link')
	dict_array=[]
	for link in all_links:
		dict={'rel':link.get('rel'),'href':link.get('href')}
		dict_array.append(dict)
	for dict in dict_array:
		if dict['rel'][0]==u'canonical':
			url= dict['href']
			file.write("%d\t%s\n"%(i+1,url))
	file.close()

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
        file.write(a.encode('utf-8'))
        file.truncate()
        file.close()

def main():
    path="./Q2_files/"
    url_files=path+"urlinks.txt"
    os.remove(url_files)
    open(url_files,'a').write("Doc_Num\tLink\n")
    for i in range (0,NUMBER_OF_PAGES):
	file=path+"Random_%d.html" %(i)
	snowball_links =path+"Random_%d_snowballed_links.txt"%(i)
	text_files=path+"Random_%d_text.txt"%(i)
	download_file(WIKI_RANDOM,file)
	find_Links(file, snowball_links)
	find_text(file, text_files)
	find_urls(i, file, url_files)	

main()
