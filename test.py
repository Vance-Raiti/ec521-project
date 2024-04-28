from duckduckgo_search import DDGS
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from tldextract import extract

def SearchDuckDuck(html,url,ddg,page_rank):
    
    original_domain = extract(url).registered_domain
    TArray = []
    Number11 = 1
    if page_rank == '':
        TArray.append(1)
    else:
        TArray.append(0)
    for result in ddg:
        result_domain = extract(result['href']).registered_domain
        if result_domain == original_domain:
            Number11 = 0
            break
    TArray.append(Number11)
   # print(TArray)
    return TArray
