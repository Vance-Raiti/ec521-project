import whois
from datetime import datetime

def ageofdomain(html,url):
    try:
        domain_info = whois.whois(url)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            current_date = datetime.now()
            age = current_date - creation_date
            return age.days
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

