import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def pageintopresults(url, html):
    K = 5  #top words to consider
    N = 30  #top search results to check

    def extract_text(html):
        soup = BeautifulSoup(html, 'html.parser')
        #Extract text from paragraphs, remove extra whitespaces
        return ' '.join(paragraph.get_text(strip=True) for paragraph in soup.find_all('p'))

    text = extract_text(html)

    def preprocess_text(text):
        #Remove non-alphanumeric characters and convert to lowercase
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return text

    preprocessed_text = preprocess_text(text)

    #function to get TF-IDF scores
    def get_tfidf_scores(text):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()
        return tfidf_matrix, feature_names

    #get TF-IDF scores
    tfidf_matrix, feature_names = get_tfidf_scores(preprocessed_text)

    #get top K words
    top_indices = tfidf_matrix.argsort(axis=1)[:, -K:].flatten()
    top_words = [feature_names[i] for i in top_indices]

    #search query
    query = ' '.join(top_words) + ' ' + url.split('//')[-1].split('/')[0]

    #google search
    search_results = requests.get(f"https://www.google.com/search?q={query}").text

    #Check if the URL domain is in the top N search results
    if url.split('//')[-1].split('/')[0] in search_results:
        return 1  #legit
    else:
        return 0  #phishy
