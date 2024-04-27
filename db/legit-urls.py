import requests
from bs4 import BeautifulSoup as bs
import bs4
import sys
import multiprocessing as mp
import os
import queue
import requests
import time
from parse import parse
from random import shuffle

NUM_WORKERS = 256
TARGET_SIZE = 100000
Q_MAXSIZE = 2**14

DEBUG = False

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

seed = "https://moz.com/top500"

def scrape(*args,**kwargs):
	try:
		scrape_(*args,**kwargs)
	except KeyboardInterrupt:
		pass

def scrape_(qin,qout):
	while qin.qsize():
		url = qin.get()
		if url == "END":
			exit()
		try:
			html = requests.get(url,headers=headers,timeout=5).text
		except requests.exceptions.RequestException:
			html = None
		qout.put((url,html))

def accept(qout,label):
	url,html = qout.get()
	#url, html,pagerank,ducksearch = qout.get()
	if html is None:
		return url, html
	offset = html_cache.tell()
	print(html,file=html_cache)
	
	print(f"{url},{offset},{len(html)},{label}",file=html_cache_table)
	return url, html

def scrape_urls(url,html):
	if url[-1] == '/':
		url = url[:-1]
	doc = bs(html,'html.parser')
	urls = [ link.get('href') for link in doc.find_all('a') ]
	urls = [url for url in urls if url is not None and "://" in url]
	return urls

html = requests.get(seed,headers=headers).text
urls = scrape_urls(seed,html)
urls = [url for url in urls if "moz" not in url]
qin, qout = mp.Queue(), mp.Queue(NUM_WORKERS)
unique_urls = set()

for url in urls:
	unique_urls.update(url)
	qin.put(url)

workers = [
	mp.Process(
		target = scrape,
		args = (qin,qout,),
	)
	for i in range(NUM_WORKERS)
]

for worker in workers:
	worker.start()
i = 0

legit_urls = open("legit-urls.txt","w")
while i < TARGET_SIZE:
	url, html = qout.get()
	if html is None:
		continue
	i += 1
	print(f'{i:5} urls acquired',flush=True)
	print(url,file=legit_urls)
	if qin.qsize() > Q_MAXSIZE:
		continue
	try:
		urls = [url for url in scrape_urls(url,html) if url not in unique_urls]
	except bs4.builder.ParserRejectedMarkup:
		continue
	shuffle(urls)	
	for url in urls[:64]:
		unique_urls.update(url)
		qin.put(url)
legit_urls.close()

for _ in range(NUM_WORKERS):
	qin.put("END")

while qout.qsize():
	qout.get()

for worker in workers:
	worker.join()


