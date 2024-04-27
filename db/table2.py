import csv
from duckduckgo_search import AsyncDDGS
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from urllib.parse import urlparse
from tldextract import extract
import aiofiles

async def extract_text_from_webpage(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()

def extract_top_k_words(tfidf_scores, k, feature_names):
    word_scores = list(zip(feature_names, tfidf_scores))
    sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)
    return sorted_words[:k]

async def retrieve_html(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
    except aiohttp.ClientError as e:
        print("Exception occurred while retrieving HTML:", e)
        return None

async def main(url):
    k = 5
    html = await retrieve_html(url)
    if html:
        webpage_text = await extract_text_from_webpage(html)
        if webpage_text and len(webpage_text) > 10:  # Adjust the minimum length threshold as needed
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform([webpage_text])
            if tfidf_vectorizer.vocabulary_:  # Check if vocabulary is not empty
                tfidf_scores = tfidf_matrix.toarray()[0]
                feature_names = tfidf_vectorizer.get_feature_names_out()
                top_k_words = extract_top_k_words(tfidf_scores, k, feature_names)

                domain = extract(url).domain

                query = " ".join(word for word, _ in top_k_words)
                query += f" {domain}"

                async with AsyncDDGS() as ddgs:
                    try:
                        # Set a timeout of 10 seconds for the ddgs.text function
                        results = await asyncio.wait_for(ddgs.text(query, max_results=30), timeout=10)
                    except asyncio.TimeoutError:
                        # If the function exceeds the timeout, return "Nothing"
                        results = "Nothing"
                return results
        else:
            return "Nothing"
    else:
        return "Nothing"


# Path to the input text file containing URLs
input_txt_path = 'phish-urls.txt'
# Path to the output CSV file where results will be saved
output_csv_path = 'resultsPhish.csv'

async def process_urls(input_file, output_file):
    async with aiofiles.open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        await writer.writerow(['url', 'duckduckgo_search_result'])  # Write header row

        async with aiofiles.open(input_file, 'r') as input_file:
            async for line in input_file:
                url = line.strip()
                # Call the main function to get the DuckDuckGo search results
                results = await main(url)
                
                # Write the URL and DuckDuckGo search result to the output CSV file
                await writer.writerow([url, results])

# Run the asyncio event loop
asyncio.run(process_urls(input_txt_path, output_csv_path))

print("Results saved to:", output_csv_path)
