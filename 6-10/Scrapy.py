import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
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
        print("Failed to retrieve HTML from:", url)
        return None

def Check_BadActionFields(html_content, webpage_url):
    #This is Question number 8
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = soup.find_all('form')
    for form in forms:
        action_url = form.get('action', '').lower()
        print("NetLock: ",urlparse(action_url).netloc,action_url)
        if not action_url or action_url.startswith('http'):
            #or action_url.startswith('/') or action_url.startswith('http'):
            #Need to fix it where it Potental bad action field. 
            print("Potential bad action field detected:", action_url)
            return 1
        if webpage_url and urlparse(action_url).netloc != urlparse(webpage_url).netloc:
                
            print("Cross-domain scripting detected:", action_url)
            return 1
def Check_NonMatchingURLs(html_content, webpage_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    domain_counts = {}
    total_links = len(links)
    similar_links_threshold = 0.5  # Define a threshold for determining highly similar links
    empty_links_threshold = 0.1

    for link in links:
        href = link.get('href')
        if href:
            parsed_href = urlparse(href)
            domain = extract(parsed_href.netloc).registered_domain
            if domain:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1

    if domain_counts:
        print(domain_counts)
        most_common_domain = max(domain_counts, key=domain_counts.get)
        if most_common_domain != extract(urlparse(webpage_url).netloc).registered_domain:
            print("Most frequent domain doesn't match page domain.")
            print("Most frequent domain:", most_common_domain)
            return 1
    similar_links_count = sum(count for count in domain_counts.values() if count > 1)
    similar_links_percentage = similar_links_count / total_links
    if similar_links_percentage > similar_links_threshold:
        print("Highly similar links detected:", similar_links_percentage)
        return 1
    empty_links_count = sum(1 for link in links if not link.get('href'))
    empty_links_percentage = empty_links_count / total_links
    if empty_links_percentage > empty_links_threshold:
        print("Empty or ill-formed links detected:", empty_links_percentage)
        return 1
    return 0
def Check_OutOfPositionBrandName(html_content, webpage_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    domain_counts = {}
    for link in links:
        href = link.get('href')
        if href:
            parsed_href = urlparse(href)
            domain = parsed_href.netloc
            if domain:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
    print(domain_counts)
    if domain_counts:
        most_common_domain = max(domain_counts, key=domain_counts.get)
        print(most_common_domain,urlparse(webpage_url).netloc)
        if most_common_domain != urlparse(webpage_url).netloc:
            # Extract brand name more accurately
            url_components = urlparse(webpage_url)
            brand_name = url_components.netloc.split('.')[0]  # Extract brand name from the first part of the domain
            brand_name = brand_name.lower()  # Convert to lowercase for case-insensitive comparison
            remaining_url = url_components.path + url_components.query  # Combine path and query for comparison
            remaining_url = remaining_url.lower()  # Convert to lowercase for case-insensitive comparison
            print(brand_name, remaining_url)
            if brand_name in remaining_url:
                print("Suspicious out-of-position brand name detected:", brand_name)
                return 1
    return 0

def Check_LoginForm(html_content, url):
    # This form will Check if there is a login form through four methods:
    # 1) It will find if there a form tag
    # 2) It will find if there are input tags
    # 3) It will find if these input tags corrilate with any of the login_keywords as defined above:
    # 4) If the Action form is empty:it will check if the URL or the action URL is Not HTTPs
    CheckConditions = [False, False,False,False]
    soup = BeautifulSoup(html_content, 'html.parser')
    form = soup.find('form')
    print(form)
    if form:
        CheckConditions[0] = True
        action_url = form.get('action', '').lower()
        webpage_url = soup.find('meta', property='og:url')
        print("actionurl",action_url,)
        CheckActionWebURl = [False,False]
        if action_url == "":
            CheckActionWebURl[0] = action_url.startswith('https')
        else:
            CheckActionWebURl[0] = True
        if webpage_url:
            webpage_url = webpage_url.get('content', '').lower()
            print("Webpage url", webpage_url.startswith('https'))
            CheckActionWebURl[1] = webpage_url.startswith('https')
        if all(CheckConditions):
            CheckConditions[1] = True
        print(CheckActionWebURl,"AFter 1")
        input_tags = form.find_all('input')
        if input_tags:
            CheckConditions[2] = True
        for input_tag in input_tags:
            attributes = [input_tag.get(attr, '').lower() for attr in ['name', 'id', 'placeholder', 'title', 'value']]
            for keyword in login_keywords:
                if keyword.lower() in attributes:
                    CheckConditions[3] = True
                    print(CheckConditions)
        print(CheckConditions)
        if all(CheckConditions):
            print("Website Contains a Login form with a URL/ActionURl that is not HTTPS")
            return 1
        elif CheckConditions == [True,False,True,True]:
            print("Website Contains a Login form the URL/ActionURL is HTTPS")
            return 0 
        else:
            print("Not all conditions are true")

# def CheckFormAction(html_content):
#     html_content = ""
#     soup = BeautifulSoup(html_content, 'html.parser')
#     form = soup.find('form')
#    # print(form)
#     if form:
#         input_tags = form.find_all('actions')
#         print(input_tags)
                           
def main():
   # url = "https://www.tiktok.com/login/phone-or-email"
  #  url = "https://www.reddit.com/login"
  #  url = "https://www.facebook.com/"
    url = "https://www.linkedin.com/login"
    url = "https://github.com/login"
    url = "https://github.com/chathurangasineth/Phishing/blob/master/login.html"
    html_content = Retrieve_Html(url)
    urls = ["https://github.com/login","https://www.linkedin.com/login","https://www.facebook.com/"]
    for url1 in urls:
        print(url1)
        content = Retrieve_Html(url1)
        print(Check_LoginForm(content))
        print(Check_BadActionFields(content, url1))
        print(Check_NonMatchingURLs(content,url1))
        print(Check_OutOfPositionBrandName(content, url1))
    if html_content:
        print("HTML content retrieved successfully:")
      #  Check_LoginForm(html_content)
       # Check_BadActionFields(html_content, url)
    #    Check_NonMatchingURLs(html_content,url)
        Check_OutOfPositionBrandName(html_content, url)
    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    main()