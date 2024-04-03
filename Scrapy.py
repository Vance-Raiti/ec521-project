import requests
from bs4 import BeautifulSoup

def retrieve_html(url):
    # try:
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
            print("Failed to retrieve HTML from:", url)
    # except requests.exceptions.RequestException as e:
    #     print("Exception occurred:", e)
    return None

def convert_to_dom(html):
    if html:
        return BeautifulSoup(html, 'html.parser')
    return None
def WebsiteTextToPart3(url):
        #Sends Text of a Webstie to 3 Send a file that they want to part 3
        html_content = retrieve_html(url)
        Part3 = html_content
        print(Part3)
def main():
    url = "https://stackoverflow.com/questions/68879326/dom-tree-travesal-in-beautifulsoup-python"
    html_content = retrieve_html(url)
    if html_content:
        print("HTML content retrieved successfully:")
        print(html_content)  
        dom_tree = convert_to_dom(html_content)
        #Sends DOM Tree to 1
        if dom_tree:
            print("DOM tree:")
            print(dom_tree.prettify())
            # links = dom_tree.find_all('a')
            # for link in links:
            #     print("Link:", link.get('href'))
        else:
            print("Failed to convert HTML to DOM tree.")

    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    main()
