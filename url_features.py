import re
from parse import parse

from url_token_clf import UrlTokenClassifier
token_classifier = UrlTokenClassifier()

s = r"[\d\w]{2,}"
embedded_domain = re.compile(
	f"{s}\.{s}\.{s}"
)


# Regex to match ipv4 courtesy of Danail Gabenski on Stack Overflow
ipv4_address = re.compile(
	"((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}"
)

top_level_domains = [
	"com",
	"org",
	"net",
	"int",
	"edu",
	"gov",
	"mil",
]

def get_features(html,url,*args):
	features = []
	features.append(
		token_classifier(url)
	)
	return features
