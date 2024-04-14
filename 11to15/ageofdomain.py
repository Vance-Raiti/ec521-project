import whois
from datetime import datetime

def get_domain_age(url):
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

def main():
    url = input("Enter the URL to lookup: ")
    age = get_domain_age(url)
    if age is not None:
        print(f"The domain '{url}' is {age} days old.")
        if age < 30:
            print("phishy")
        else:
            print("not phishy")
    else:
        print("Unable to retrieve domain age.")


if __name__ == "__main__":
    main()
