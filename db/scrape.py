import requests

LEGIT = 0
PHISH = 1

DEBUG = False

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

html_cache = open("html_cache.txt","a")
html_cache_table = open("html_cache_table.csv","a")

def debug(*args,**kwargs):
	if DEBUG:
		print(*args,**kwargs)

def scrape(*args,**kwargs):
	try:
		scrape_(*args,**kwargs)
	except KeyboardInterrupt:
		pass

def scrape_(qin,qout):
	while qin.qsize():
		url = qin.get()
		if url == "END":
			exit()
		try:
			html = requests.get(url,headers=headers,timeout=5).text
			debug(f'SUCCESS {url}')
		except requests.exceptions.RequestException:
			html = None
			debug(f'FAILED  {url}')
		qout.put((url,html))

def accept(qout,label):
	url, html = qout.get()
	if html is None:
		return url, html
	offset = html_cache.tell()
	print(html,file=html_cache)
	print(f"{url},{offset},{len(html)},{label}",file=html_cache_table)
	return url, html
