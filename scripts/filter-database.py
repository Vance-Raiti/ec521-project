#!/bin/python

import os
import requests
import threading
import multiprocessing as mp

BATCH_SIZE = 256


def verify_urls(q,idx):
	fp = open(f'urls/urls{idx}.txt','w')
	while not q.empty():
		url = q.get()
		n = q.qsize()
		try:
			requests.get(url,timeout=3)
		except Exception as e:
			print(f'{n:5} FAIL {url}')
			continue
		print(url,file=fp)
		print(f'{n:5} SUCCESS {url}')
	fp.close()

def filter_database():
	with open('online-valid.csv') as fp:
		serial = fp.read()
	serial = serial.split('\n')	
	p = lambda s: s.split(',')
	keys = p(serial[0])
	i = 0
	while keys[i] != 'url':
		i += 1
	database = [
		p(line)[i]
		for line in serial[1:] if len(p(line)) == len(keys)
	]
	
	if not os.path.exists('urls'):
		os.mkdir('urls')
	
	q = mp.Queue()
	for entry in database:
		q.put(entry)

	workers = [
		mp.Process(
			target=verify_urls,
			args=(q,idx),
		)
		for idx in range(BATCH_SIZE)
	]
	
	for worker in workers:
		worker.start()
	for worker in workers:
		worker.join()	

filter_database()
