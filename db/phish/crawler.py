#!/bin/python

import os
import threading
import multiprocessing as mp
import requests


NUM_WORKERS = 256
p = lambda s: s.split(',')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def verify_urls(*args,**kwargs):
	try:
		verify_urls_(*args,**kwargs)
	except KeyboardInterrupt:
		pass

def verify_urls_(qin,qout):
	while qin.qsize():
		url = qin.get()
		if url == "END":
			exit()
		n = qin.qsize()
		try:
			html = requests.get(url,headers=headers,timeout=10).text
			print(f'{n:5} SUCCESS {url}')
		except requests.exceptions.RequestException:
			html = None
			print(f'{n:5} FAIL {url}')
		qout.put((url,html))

with open('online-valid.csv') as fp:
	serial = fp.read()
serial = serial.split('\n')	

i = 0
while p(serial[0])[i] != 'url':
	i += 1

urls = [
	line.split(',')[i]
	for line in serial[1:] if len(p(line)) == len(p(serial[0]))
]

qin, qout = mp.Queue(), mp.Queue()


for url in urls:
	qin.put(url)

for _ in range(NUM_WORKERS):
	qin.put("END")

workers = [
	mp.Process(
		target=verify_urls,
		args=(qin,qout,),
	)
	for _ in range(NUM_WORKERS)
]

for worker in workers:
	worker.start()

html_cache = open("cache/html_cache.txt","w")
html_cache_table = open("cache/html_cache_table.csv","w")

for _ in range(len(urls)):
	url,html = qout.get()
	if html is None:
		continue
	print(f"{url},{html_cache.tell()},{len(html)}",file=html_cache_table)
	print(html,file=html_cache)
while qout.qsize():
	qout.get()
html_cache.close()
html_cache_table.close()
