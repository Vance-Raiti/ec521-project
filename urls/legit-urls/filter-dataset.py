import random

TARGET_SIZE = 10000

with open('legitimate-urls-full.txt') as fp:
	urls = fp.readlines()

random.shuffle(urls)
urls = urls[:TARGET_SIZE]

with open('legitimate-urls.txt','w') as fp:
	for url in urls:
		fp.write(url)
