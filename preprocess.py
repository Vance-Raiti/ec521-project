from datasets import GenericDataset
import multiprocessing as mp
import torch
import url_features
import sys
from html_tokenizer import HtmlTokenizer
#from test import SearchDuckDuck
import test
import Scrapy
RANGE = 2000


html_tokenizer = HtmlTokenizer()

get_age = lambda html,url,ddg,pr,age: [age]

feature_functions = [
	url_features.get_features,
	html_tokenizer,
	test.SearchDuckDuck,
	Scrapy.main,
	get_age,
]


def process(data):
	features = []
	html = data['html']
	ddg = data['ddg']
	page_rank = data['page_rank']
	url = data['url']
	age = data['age']
	label = data['label']
	for fn in feature_functions:
		features += fn(html,url,ddg,page_rank,age)
	features += [label]
	return features

def consume(features):
	output = open("features.txt","a")
	features = [str(feature) for feature in features]
	print(','.join(features),file=output)	

if __name__ == '__main__':	
	start = int(sys.argv[1])
	dataset = GenericDataset()
	dataset.train_and_valid()
	stop = min(start+RANGE,len(dataset))

	for i in range(start,stop):
		data = dataset[i]
		features = process(data)
		consume(features)
		print(f"{i:5} of {len(dataset)}")
	print(start,stop)
