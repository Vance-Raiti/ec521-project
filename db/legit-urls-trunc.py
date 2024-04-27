import random
urls = [url.strip() for url in open('legit-urls.txt') if len(url) > 4]
random.shuffle(urls)
fp = open('legit-urls-trunc.txt','w')
[print(urls[i],file=fp) for i in range(10000)]
