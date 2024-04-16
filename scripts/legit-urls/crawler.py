import requests
from bs4 import BeautifulSoup as bs
import sys
import multiprocessing as mp
import os
import re
from collections import deque
import queue

NUM_WORKERS = 256

TARGET_SIZE = 100000

url_queue = deque()
def push(x):
	url_queue.append(x)
def pop():
	return url_queue.popleft()

if len(sys.argv) > 1:
	seed = sys.argv[1]
else:
	seed = "https://moz.com/top500"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def crawl(qin,qout):
	while True:
		url = qin.get()
		assert type(url) is str
		try:
			http = requests.get(url,headers=headers,timeout=5)
		except Exception as E:
			print(E)
			qout.put(url)
			continue
		if http.status_code >= 300 or http.status_code < 200:
			qout.put(url)
			continue
		doc = bs(http.text,'html.parser')
		old_url = url	
		urls = []
		for link in doc.find_all('a'):
			url = link.get('href') 
			if url is not None and '://' in url:
				qout.put(url)
 
http = requests.get(seed,headers=headers)
print(http.status_code)
doc = bs(http.text,'html.parser')

for link in doc.find_all('a'):
	url = link.get('href')
	if url is None or 'moz.com' in url or '://' not in url:
		continue
	assert type(url) is str
	push(url)


workers = []
queues = []

for i in range(NUM_WORKERS):
	qin, qout = mp.Queue(), mp.Queue()
	workers.append(
		mp.Process(
			target = crawl,
			args = (qin,qout,),
		)
	)
	queues.append((qin,qout,))

for worker in workers:
	worker.start()

for qin,qout in queues:
	qin.put(pop())

n = 0
unique_urls = {}
while n < TARGET_SIZE:
	for qin,qout in queues:
		if qout.qsize() == 0:
			continue
		urls = []
		while True:
			try:
				url = qout.get(block=False)
				urls.append(
					url
				)
			except queue.Empty:
				break
		qin.put(pop())
		for url in urls:
			assert type(url) is str
			if url in unique_urls:
				continue
			unique_urls[url] = True
			push(url)
			n += 1
		print(f'{n} urls acquired...')
print('urls acquired! Killing children and saving results...')

for worker in workers:
	worker.kill()


with open('legitimate-urls.txt','w') as fp:
	while True:
		try:
			print(pop(),file=fp)
		except:
			break	
