import requests
from duckduckgo_search import AsyncDDGS as DDGS
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from tldextract import extract

import whois
from datetime import datetime


LEGIT = 0
PHISH = 1

DEBUG = False

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

html_cache = open("html_cache.txt","a")
html_cache_table = open("html_cache_table.csv","a")

api_key = open(".api-key").read().strip()

def get_page_rank(domains):
	url = 'https://openpagerank.com/api/v1.0/getPageRank'
	headers = {'API-OPR': api_key}
	params = {'domains[]': domains}
	response = requests.get(url, headers=headers, params=params)
	if response.status_code == 200:
		return response.json()
	else:
		print('WARNING: pagerank failed')
		raise requests.exceptions.RequestException

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
	results = DDGS().text(query,max_results=30)
	return results

def extract_top_k_words(tfidf_scores, k, feature_names):
	word_scores = list(zip(feature_names, tfidf_scores))
	sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
	return sorted_words[:k]


def ageofdomain(html,url):
	try:
		domain_info = whois.whois(url)
		creation_date = domain_info.creation_date
		if isinstance(creation_date, list):
			creation_date = creation_date[0]
		if creation_date is None or type(creation_date) is str:
			creation_date = datetime.now()
	except Exception:
		creation_date = datetime.now()	
	current_date = datetime.now()
	age = current_date - creation_date
	return age.days


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
			age = ageofdomain(html,url)
			debug(f'SUCCESS {url}')
		except requests.exceptions.RequestException:
			html = None
			pagerank = None
			age = None
			debug(f'FAILED  {url}')
		qout.put((url,html,pagerank,age))

def accept(qout,label):
	url, html, pagerank, age = qout.get()
	if html is None:
		return url, html
	html_offset = html_cache.tell()
	print(html,file=html_cache)	
	page_rank_offset = html_cache.tell()
	print(pagerank,file=html_cache)
	print(f"{url},{html_offset},{len(html)},{page_rank_offset},{len(pagerank)},{age},{label}",file=html_cache_table)
	return url, html

def retrieve(row):
	row = row.strip().split(',')
	url, offset, length, label = row[0], int(row[1]), int(row[2]), int(row[3])
	html_cache.seek(offset)
	html = html_cache.read(length)
	return url, html, label
