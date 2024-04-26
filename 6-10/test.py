from duckduckgo_search import DDGS
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from tldextract import extract

# def extract_text_from_webpage(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     for script in soup(["script", "style"]):
#         script.extract()
#     return soup.get_text()

# def extract_top_k_words(tfidf_scores, k, feature_names):
#     word_scores = list(zip(feature_names, tfidf_scores))
#     sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
#     return sorted_words[:k]

# def retrieve_html(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.text
#     else:
#         print("Failed to retrieve HTML from:", url)
#         return None
    
# def get_page_rank(domains):
#     api_key = 'oc800w8s4444sw4gwkgos0go8k4kwo88ksskg0k0'

#     url = 'https://openpagerank.com/api/v1.0/getPageRank'
#     headers = {'API-OPR': api_key}
#     params = {'domains[]': domains}
    
#     response = requests.get(url, headers=headers, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
#         print(data,"THIS IS DATA FROM PAGE RANK")

#         if 'response' in data:
#             page_ranks = []
#             for item in data['response']:
#                 domain = item['domain']
#                 page_rank_integer = item['page_rank_integer']
#                 if page_rank_integer == '':
#                     return 1
#                 elif 'error' in item and item['error'] != '':
#                     return 1
#     return 0
def main(Godaddyresult, SearchRankResult,url):
    # k=5
    # #12 and 13
    # webpage_text = extract_text_from_webpage(html)
    # tfidf_vectorizer = TfidfVectorizer()
    # tfidf_matrix = tfidf_vectorizer.fit_transform([webpage_text])
    # tfidf_scores = tfidf_matrix.toarray()[0]
    # feature_names = tfidf_vectorizer.get_feature_names_out()
    # top_k_words = extract_top_k_words(tfidf_scores, k, feature_names)
    
    # domain = extract(url).domain
    
    # query = " ".join(word for word, _ in top_k_words)
    # query += f" {domain}"
    
    # results = DDGS().text(query, max_results=30)
    # print(results,"THIS IS THE RESULT")
    original_domain = extract(url).registered_domain
    TArray = []
    Number11 = 1
    for result in Godaddyresult:
        result_domain = extract(result['href']).registered_domain
        if result_domain == original_domain:
            Number11 = 0
            break
    TArray.append(Number11)
    # domain = extract(url).registered_domain
    # domains = [domain]
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
