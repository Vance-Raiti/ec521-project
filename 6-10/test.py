from duckduckgo_search import DDGS
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from tldextract import extract
def main(Godaddyresult, SearchRankResult,url):
    original_domain = extract(url).registered_domain
    TArray = []
    Number11 = 1
    if SearchRankResult == "":
        TArray.append(1)
    else:
        TArray.append(0)
    for result in Godaddyresult:
        result_domain = extract(result['href']).registered_domain
        if result_domain == original_domain:
            Number11 = 0
            break
    TArray.append(Number11)
    TArray.append(SearchRankResult)
    return TArray


# # Example usage
# html = retrieve_html("https://www.reddit.com/login")
# url = "https://www.reddit.com/login"
# search_results = main(html, url)
# # domain = extract(url).registered_domain
# # page_ranks = get_page_rank(domains, api_key)
# # print(page_ranks)
# print(search_results)
