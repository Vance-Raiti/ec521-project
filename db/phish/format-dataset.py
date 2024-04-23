#!/usr/bin/python

# sort by submission time

from csv import parse, pack

import datetime

key = lambda entry: datetime.datetime.fromisoformat(entry['submission_time']).timestamp()

data = parse('urls.txt')
fp = open('phish-urls.txt','w')
for datum in data:
	print(datum['url'],file=fp)
fp.close()
