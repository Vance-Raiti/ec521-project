import re
from parse import parse

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

def get_features(html,url):
	protocol, domain, path = parse("{}://{}/{}",url)

	features = []

	# does this url contain something that looks like a domain in the path?
	features.append(
		1 if embedded_domain.match(path) is not None else 0
	)

	# does this url con
	features.append(
		1 if ipv4_address.match(url) is not None else 0
	)

	features.append(
		url.count('.')
	)

	# decided to split feature 4 into 2 separate features
	features.append(
		1 if "@" in url else 0
	)

	features.append(
		1 if "-" in domain else 0
	)

	features.append(
		0
	)
	
	features.append(
		1 if any([
			segment in top_level_domains for segment in url.split('.')[3:]
		]) else 0
	)
	
	return features
