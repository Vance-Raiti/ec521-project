#!/bin/python

import os
import threading
import multiprocessing as mp
import requests
from scrape import scrape, accept, LEGIT, PHISH

NUM_WORKERS = 256
p = lambda s: s.split(',')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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
		target=scrape,
		args=(qin,qout,),
	)
	for _ in range(NUM_WORKERS)
]

for worker in workers:
	worker.start()


success = 0
fail = 0
for i in range(len(urls)):
	url, html = accept(qout,PHISH)
	if html is None:
		fail += 1
	else:
		success += 1
	projected = int( len(urls) * success / (success+fail) )
	print(f'{success:5} succeeded, {fail:5} failed of {len(urls)} total (projected {projected:5} successful urls)')

while qout.qsize():
	qout.get()
html_cache.close()
html_cache_table.close()
