#!/bin/python

import os
import threading
import multiprocessing as mp
import requests
from scrape import scrape, accept
import sys
from os.path import exists, join, dirname


NUM_WORKERS = 1
TARGET_SIZE = 10
qin, qout = mp.Queue(), mp.Queue()


if sys.argv[1] == 'phish':
	label = 1
	url_file = 'phish-urls.txt'
elif sys.argv[1] == 'legit':
	label = 0
	url_file = 'legit-urls.txt'
elif sys.argv[1] == 'test':
	label = 2
	url_file = 'test-urls.txt'
else:
	print(f"label {sys.argv[1]} not understood")
	exit()

urls = [url.strip() for url in open(url_file) if len(url) > 4]

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

if not exists('save'):
	os.mkdir('save')

i = 0
save_path = lambda i: f'save/successfully-scraped-{i}'

while exists(save_path(i)):
	i += 1

scraped = open(save_path(i),'w')

for i in range(len(urls)):
	url, html, _, __ = accept(qout,label)
	if html is None:
		fail += 1
	else:
		success += 1
	projected = int( len(urls) * success / (success+fail) )
	print(f'{success:5} succeeded, {fail:5} failed of {len(urls)} total (projected {projected:5} successful urls)')
	print(url,file=scraped)
	if success == TARGET_SIZE:
		break
	
while qout.qsize():
	qout.get()

for worker in workers:
	worker.join()
