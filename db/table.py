import csv
from duckduckgo_search import DDGS
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from tldextract import extract
from nltk.corpus import words
import nltk

nltk.download('words')

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

english_vocab = set(words.words())

def main(url):
    k = 5  
    html = retrieve_html(url)
    if html:
        webpage_text = extract_text_from_webpage(html)
        if not webpage_text.strip():  # Check if webpage_text is empty or contains only whitespace
            print("Webpage text is empty")
            return "Nothing"
        
        english_words = [word for word in webpage_text.split() if word.lower() in english_vocab]
        webpage_text = ' '.join(english_words)
        
        if webpage_text.strip():
            try:
                tfidf_vectorizer = TfidfVectorizer()
                tfidf_matrix = tfidf_vectorizer.fit_transform([webpage_text])
            except ValueError:
                print("Empty vocabulary encountered, returning 'Nothing'")
                return "Nothing"
            
            if tfidf_vectorizer.vocabulary_:
                tfidf_scores = tfidf_matrix.toarray()[0]
                feature_names = tfidf_vectorizer.get_feature_names_out()
                top_k_words = extract_top_k_words(tfidf_scores, k, feature_names)

                domain = extract(url).domain

                query = " ".join(word for word, _ in top_k_words)
                query += f" {domain}"

                try:
                    with DDGS(timeout=5) as ddgs:  
                        results = ddgs.text(query, max_results=30)
                except requests.Timeout:
                    print("DuckDuckGo search request timed out")
                    results = "Nothing"
                except Exception as e:
                    print("An error occurred during DuckDuckGo search:", e)
                    results = "Nothing"
                return results
            else:
                print("Webpage text contains only stop words")
                return "Nothing"
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

        with open(input_file, 'r', encoding='utf-8') as input_file:  # Specify encoding
            for line in input_file:
                url = line.strip()
                # Call the main function to get the DuckDuckGo search results
                print('Processing URL:', url)
                results = main(url)
                # Write the URL and DuckDuckGo search result to the output CSV file
                writer.writerow([url, results])
if __name__ == "__main__":
	# Process URLs synchronously
	process_urls(input_txt_path, output_csv_path)


	print("Results saved to:", output_csv_path)
