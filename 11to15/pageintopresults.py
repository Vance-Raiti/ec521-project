from googlesearch import search
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.parse import urlparse
import requests

def extract_top_k_words_from_url(url, k):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([page_content])
            feature_names = vectorizer.get_feature_names_out()
            dense = tfidf_matrix.todense()
            episode = dense.tolist()[0]
            phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
            sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)[:k]
            top_words = []
            for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores]:
                top_words.append(phrase)
            return top_words
        else:
            print("Failed to retrieve page content. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def is_legitimate_page(page_url, top_words, domain_keywords, n):
    page_domain = urlparse(page_url).netloc
    search_query = ' '.join(top_words + domain_keywords)
    search_results = search(search_query, num=n, stop=n, pause=2)
    for result_url in search_results:
        result_domain = urlparse(result_url).netloc
        if page_domain == result_domain:
            return True
    return False

def main():
    page_url = input("Enter the URL of the page to check: ")
    K = 5
    N = 30
    domain_keywords = ["domain", "keyword5"]  # Update with actual domain keywords
    top_words = extract_top_k_words_from_url(page_url, K)
    if top_words:
        is_legitimate = is_legitimate_page(page_url, top_words, domain_keywords, N)
        if is_legitimate:
            print("The page is deemed legitimate.")
        else:
            print("The page is regarded as being phishy.")
    else:
        print("Failed to extract top words.")

if __name__ == "__main__":
    main()
