#!/usr/bin/python

# sort by submission time

from csv import parse, pack

import datetime

key = lambda entry: datetime.datetime.fromisoformat(entry['submission_time']).timestamp()

data = parse('urls.txt')
data = sorted(data,key=key,reverse=True)
pack(data,'urls.txt')
