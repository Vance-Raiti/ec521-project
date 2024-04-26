import requests
from bs4 import BeautifulSoup as bs
import sys
import multiprocessing as mp
import os
import queue
import requests
import time
from parse import parse
from scrape import scrape, accept, LEGIT, PHISH

NUM_WORKERS = 256
TARGET_SIZE = 20000
Q_MAXSIZE = 2**14

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

seed = "https://moz.com/top500"

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
while i < TARGET_SIZE:
	url, html = accept(qout,LEGIT)
	if html is None:
		print('GET failed')
		continue
	i += 1
	print(f'{i:5} urls acquired',flush=True)
	if qin.qsize() > Q_MAXSIZE:
		continue
	for url in scrape_urls(url,html)[:64]:
		if url in unique_urls:
			continue
		unique_urls.update(url)
		qin.put(url)

for _ in range(NUM_WORKERS):
	qin.put("END")

while qout.qsize():
	qout.get()

for worker in workers:
	worker.join()

html_cache.close()
hmtl_cache_table.close()
