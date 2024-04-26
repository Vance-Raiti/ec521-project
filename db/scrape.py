import requests
from duckduckgo_search import DDGS
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from tldextract import extract

LEGIT = 0
PHISH = 1

DEBUG = False

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

html_cache = open("html_cache.txt","a")
html_cache_table = open("html_cache_table.csv","a")
DuckDuckGo_cache = open("DuckDuckGo_cache.txt","a")
DuckDuckGo_cache_table = open("DuckDuckGo_cache_table.csv","a")
PageRank_cache = open("PageRank_cache.txt","a")
PageRank_cache_table = open("PageRank_cache_table.csv","a")
def get_page_rank(domains):
	api_key = 'oc800w8s4444sw4gwkgos0go8k4kwo88ksskg0k0'
	url = 'https://openpagerank.com/api/v1.0/getPageRank'
	headers = {'API-OPR': api_key}
	params = {'domains[]': domains}
	response = requests.get(url, headers=headers, params=params)
	if response.status_code == 200:
		data = response.json()
	else:
		data = ''
	return data
def extract_text_from_webpage(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()
def ResultsFromDuckDuckGo(html,url):
	k = 5
	webpage_text = extract_text_from_webpage(html)
	tfidf_vectorizer = TfidfVectorizer()
	tfidf_matrix = tfidf_vectorizer.fit_transform([webpage_text])
	tfidf_scores = tfidf_matrix.toarray()[0]
	feature_names = tfidf_vectorizer.get_feature_names_out()
	top_k_words = extract_top_k_words(tfidf_scores, k, feature_names)
	domain = extract(url).domain
	query = " ".join(word for word, _ in top_k_words)
	query += f" {domain}"
	results = DDGS().text(query, max_results=30)
	return results
def extract_top_k_words(tfidf_scores, k, feature_names):
    word_scores = list(zip(feature_names, tfidf_scores))
    sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
    return sorted_words[:k]
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
			domain = extract(url).registered_domain
			domains = [domain]
			pagerank = get_page_rank(domains)
			ducksearch = ResultsFromDuckDuckGo(html,url)
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
def retrieve(row):
	row = row.strip().split(',')
	url, offset, length, label = row[0], int(row[1]), int(row[2]), int(row[3])
	html_cache.seek(offset)
	html = html_cache.read(length)
	return url, html, label