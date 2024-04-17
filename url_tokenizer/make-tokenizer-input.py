#!/bin/python
from parse import *

first = True

fp = open("tokenizer-input.txt","w")

for line in open("online-valid.csv"):
	if first:
		i = line.split(',').index('url')
		first = False
		continue
	url = line.split(',')[i]
	url = url[url.find("://")+len("://"):] 
	url = url.replace("."," ")
	url = url.replace("/"," ")
	print(url)
	print(url,file=fp)
