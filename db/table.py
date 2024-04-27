import csv
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
    try:
        response = requests.get(url, timeout=10)  # Set a timeout of 10 seconds for the entire request
        if response.status_code == 200:
            return response.text
        else:
            return "Nothing"
    except requests.RequestException as e:
        print("Exception occurred while retrieving HTML:", e)
        return "Nothing"

def main(url):
    k = 5
    html = retrieve_html(url)
    if html:
        webpage_text = extract_text_from_webpage(html)
        if webpage_text == "Nothing":
            return "Nothing"
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([webpage_text])
        tfidf_scores = tfidf_matrix.toarray()[0]
        feature_names = tfidf_vectorizer.get_feature_names_out()
        top_k_words = extract_top_k_words(tfidf_scores, k, feature_names)

        domain = extract(url).domain

        query = " ".join(word for word, _ in top_k_words)
        query += f" {domain}"

        try:
            with DDGS(timeout=5) as ddgs:  # Set a timeout of 5 seconds for the DDGS request
                results = ddgs.text(query, max_results=30)
        except requests.Timeout:
            print("DuckDuckGo search request timed out")
            results = "Nothing"
        return results
    else:
        return "Nothing"

# Path to the input text file containing URLs
input_txt_path = 'legit-urls.txt'
# Path to the output CSV file where results will be saved
output_csv_path = 'results.csv'

def process_urls(input_file, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'duckduckgo_search_result'])  # Write header row

        with open(input_file, 'r') as input_file:
            for line in input_file:
                url = line.strip()
                # Call the main function to get the DuckDuckGo search results
                print('beforehi')
                results = main(url)
                print('hi')
                # Write the URL and DuckDuckGo search result to the output CSV file
                writer.writerow([url, results])

# Process URLs synchronously
process_urls(input_txt_path, output_csv_path)

print("Results saved to:", output_csv_path)
