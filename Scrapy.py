import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin
from tldextract import extract

login_keywords = [
    "password", "username", "email", "login", "sign in", "log in", "sign up", "register", 
    "forgot password", "remember me", "authentication", "access code", "security question", 
    "pin", "account number", "customer id", "member id", "passphrase", "secret key", 
    "login id", "user id", "login name", "passcode", "client id", "login code", 
    "verification code", "identity code", "account login", "account access", 
    "account sign in", "logon", "auth", "user", "pass", "access", "entry", 
    "secure login", "login details", "login credentials", "account information", 
    "account access", "authorized access", "user authentication", "member login", 
    "login form", "login page", "access portal", "user panel", "login account", 
    "member login", "client login", "employee login", "staff login", "customer login", 
    "partner login", "vendor login", "agent login", "administrator login", 
    "manager login", "subscriber login", "guest login", "session login", 
    "session id", "login token", "login key", "login link", "secure access", 
    "access token", "access key", "secure sign in", "secure account", 
    "secure authentication", "secure entry", "secure portal", "secure user", 
    "secure member", "secure client", "secure employee", "secure staff", 
    "secure customer", "secure partner", "secure vendor", "secure agent", 
    "secure administrator", "secure manager", "secure subscriber", 
    "secure guest", "secure session", "secure login session", 
    "secure login token", "secure login key", "secure login link", 
    "secure login form",
    "username-field", "password-field"  
]

def Retrieve_Html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return 0

def Check_BadActionFields(html, url):
    #This is Question number 8
    soup = BeautifulSoup(html, 'html.parser')
    forms = soup.find_all('form')
    for form in forms:
        action_url = form.get('action', '').lower()
        action_url = urljoin(url, action_url)
        if not action_url or not action_url.startswith('https'):
            return 1
        if url and urlparse(action_url).netloc != urlparse(url).netloc:
            return 1
    return 0
def Check_NonMatchingURLs(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    domain_counts = {}
    total_links = len(links)
    similar_links_threshold = 0.5  
    empty_links_threshold = 0.1

    for link in links:
        href = link.get('href')
        if href:
            parsed_href = urlparse(href)
            domain = extract(parsed_href.netloc).registered_domain
            if domain:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1

    if domain_counts:
        most_common_domain = max(domain_counts, key=domain_counts.get)
        if most_common_domain != extract(urlparse(url).netloc).registered_domain:

            return 1
    
    similar_links_count = sum(count for count in domain_counts.values() if count > 1)
    if total_links > 0:
        similar_links_percentage = (similar_links_count + 0.1) / (total_links + 0.1)
    else:
        similar_links_percentage = 0.0

    if similar_links_percentage > similar_links_threshold:
        return 1
    
    empty_links_count = sum(1 for link in links if not link.get('href'))
    if total_links > 0:
        empty_links_percentage = (empty_links_count + 0.1) / (total_links + 0.1)
    else:
        empty_links_percentage = 0.0

    if empty_links_percentage > empty_links_threshold:
        return 1
    
    return 0
def Check_OutOfPositionBrandName(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    domain_counts = {}
    for link in links:
        href = link.get('href')
        if href:
            parsed_href = urlparse(href)
            domain = parsed_href.netloc
            if domain:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
    if domain_counts:
        most_common_domain = max(domain_counts, key=domain_counts.get)
        if most_common_domain != urlparse(url).netloc:
            url_components = urlparse(url)
            brand_name = url_components.netloc.split('.')[0] 
            brand_name = brand_name.lower()  
            remaining_url = url_components.path + url_components.query 
            remaining_url = remaining_url.lower()  
            if brand_name in remaining_url:
                return 1
    return 0

def Check_LoginForm(html, url):
    # This form will Check if there is a login form through four methods:
    # 1) It will find if there a form tag
    # 2) It will find if there are input tags
    # 3) It will find if these input tags corrilate with any of the login_keywords as defined above:
    # 4) If the Action form is empty:it will check if the URL or the action URL is Not HTTPs
    CheckConditions = [False, False,False,False]
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form')
    if form:
        CheckConditions[0] = True
        action_url = form.get('action', '').lower()
        url = soup.find('meta', property='og:url')
        CheckActionWebURl = [False,False]
        if action_url == "":
            CheckActionWebURl[0] = action_url.startswith('https')
        else:
            CheckActionWebURl[0] = True
        if url:
            url = url.get('content', '').lower()
            CheckActionWebURl[1] = url.startswith('https')
        if all(CheckConditions):
            CheckConditions[1] = True
        input_tags = form.find_all('input')
        if input_tags:
            CheckConditions[2] = True
        for input_tag in input_tags:
            attributes = [input_tag.get(attr, '').lower() for attr in ['name', 'id', 'placeholder', 'title', 'value']]
            for keyword in login_keywords:
                if keyword.lower() in attributes:
                    CheckConditions[3] = True
        if all(CheckConditions):
            return 1
        elif CheckConditions == [True,False,True,True]:
            return 0
        else:
            return 0

                           
def main(html, url,ddg,page_rank):

    features = []
    features.append(Check_LoginForm(html,url))
    features.append(Check_BadActionFields(html, url))
    features.append(Check_NonMatchingURLs(html,url))
    features.append(Check_OutOfPositionBrandName(html, url))
    if features[0] == None:
        features[0] = 0
    #print(features)
    return features
#main("hello","hello")