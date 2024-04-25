from duckduckgo_search import DDGS
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from tldextract import extract

def extract_text_from_webpage(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()

def extract_top_k_words(tfidf_scores, k, feature_names):
    word_scores = list(zip(feature_names, tfidf_scores))
    sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
    return sorted_words[:k]

def retrieve_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve HTML from:", url)
        return None

def main(html, url, k=5):
    webpage_text = extract_text_from_webpage(html)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([webpage_text])
    tfidf_scores = tfidf_matrix.toarray()[0]
    feature_names = tfidf_vectorizer.get_feature_names_out()
    top_k_words = extract_top_k_words(tfidf_scores, k, feature_names)
    
    # Extract domain keyword from URL
    domain = extract(url).domain
    
    # Form search query including top words and domain keyword
    query = " ".join(word for word, _ in top_k_words)
    query += f" {domain}"
    
    # Perform search using DuckDuckGo
    results = DDGS().text(query, max_results=30)
    return results

# Example usage
html = retrieve_html("https://www.reddit.com/login")
url = "https://www.reddit.com/login"
search_results = main(html, url)
print(search_results)
