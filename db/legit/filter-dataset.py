import random
from cache import html_get_flush

TARGET_SIZE = 10000

with open('legitimate-urls-full.txt') as fp:
	urls = fp.readlines()

random.shuffle(urls)

urls, to_flush = urls[:TARGET_SIZE], urls[TARGET_SIZE:]

for url in to_flush:
	html_get_flush(url)

with open('legit-urls.txt','w') as fp:
	for url in urls:
		fp.write(url)
