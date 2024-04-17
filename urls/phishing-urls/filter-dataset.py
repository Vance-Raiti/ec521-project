#!/bin/python

import os
import requests
import threading
import multiprocessing as mp

BATCH_SIZE = 256
p = lambda s: s.split(',')

def verify_urls(q,i,idx):
	fp = open(f'urls/urls{idx}.txt','w')
	while not q.empty():
		entry = q.get()
		url = p(entry)[i]
		n = q.qsize()
		try:
			requests.get(url,timeout=3)
		except Exception as e:
			print(f'{n:5} FAIL {url}')
			continue
		print(entry,file=fp)
		print(f'{n:5} SUCCESS {url}')
	fp.close()

def filter_database():
	with open('online-valid.csv') as fp:
		serial = fp.read()
	serial = serial.split('\n')	

	i = 0
	while p(serial[0])[i] != 'url':
		i += 1

	database = [
		line
		for line in serial[1:] if len(p(line)) == len(p(serial[0]))
	]
	
	if not os.path.exists('urls'):
		os.mkdir('urls')
	
	with open('urls/header.txt','w') as fp:
		print(serial[0],file=fp)

	q = mp.Queue()
	for entry in database:
		q.put(entry)

	workers = [
		mp.Process(
			target=verify_urls,
			args=(q,i,idx),
		)
		for idx in range(BATCH_SIZE)
	]
	
	for worker in workers:
		worker.start()
	for worker in workers:
		worker.join()	

filter_database()
