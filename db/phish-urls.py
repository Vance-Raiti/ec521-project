#!/bin/python

import os
import threading
import multiprocessing as mp
import requests

NUM_WORKERS = 256
TARGET_SIZE = 10000

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
phish_urls = open("phish-urls.txt","w")
for url in urls:
	print(url,file=phish_urls)

