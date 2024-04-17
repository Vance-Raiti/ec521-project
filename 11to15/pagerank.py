import requests
from bs4 import BeautifulSoup

def get_page_rank(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get("https://www.google.com/search?q=info:" + url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        rank_str = soup.find("div", {"class": "BNeawe UPmit AP7Wnd"}).text
        rank = int(rank_str.split()[1].replace(',', ''))
        return rank
    except Exception as e:
        print("An error occurred:", e)
        return None

url = input("Enter the URL: ")
page_rank = get_page_rank(url)
if page_rank is not None:
    print(f"The estimated PageRank of {url} is {page_rank}")
else:
    print("Failed to retrieve PageRank.")
