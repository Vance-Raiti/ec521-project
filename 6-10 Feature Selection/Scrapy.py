import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
import subprocess

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
def Check_LoginForm(html_content):
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
            CheckActionWebURl[1] = webpage_url.startswith('https')
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
                    print(CheckConditions)
        
    if all(CheckConditions):
        print("Website Contains a Login form with a URL/ActionURl that is not HTTPS")
    elif CheckConditions == [True,False,True,True]:
         print("Website Contains a Login form the URL/ActionURL is HTTPS") 
    else:
        print("Not all conditions are true")
    
                        
def main():
    url = "https://www.reddit.com/login"
  #  url = "https://www.facebook.com/"
  #  url = "https://github.com/login"
    html_content = Retrieve_Html(url)
    if html_content:
        print("HTML content retrieved successfully:")
        Check_LoginForm(html_content)
        

    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    main()