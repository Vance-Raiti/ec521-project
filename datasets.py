import torch
from torch.utils.data import IterableDataset
import os
from os.path import dirname,join,exists
from random import shuffle
import requests
import numpy
from urltokenizer import UrlTokenizer
import url_features
from Scrapy import Retrieve_Html, Check_BadActionFields, Check_NonMatchingURLs, Check_OutOfPositionBrandName, Check_LoginForm



this = dirname(__file__)

EPS = 1e-5

DEFAULT_LEGITIMATE = join(this,'db/legit')
DEFAULT_PHISH = join(this,'db/phish')

DEFAULT_FEATURE_FUNCTIONS = [
	url_features.get_features
]
i = 0
class GenericDataset(IterableDataset):
	def __init__(
			self,
			legit_path=DEFAULT_LEGITIMATE,
			phish_path=DEFAULT_PHISH,
			feature_functions=DEFAULT_FEATURE_FUNCTIONS,
			percent_valid=0.2,
		):
		
		html_cache_of = lambda prefix: join(prefix,"cache/html_cache.txt")
		html_cache_table_of = lambda prefix: join(prefix,"cache/html_cache_table.csv")
		def parse_row(row,label):
			row = row.strip().split(',') + [label]
			labels = ['url','offset','len','label']
			types = [str,int,int,float]
			try:
				return {k:t(v) for k,v,t in zip(labels,row,types)}
			except ValueError:
				return None

		legit = [
			parse_row(row,1-EPS)
			for row in open(html_cache_table_of(legit_path))
		]
		self.legit_cache = open(html_cache_of(legit_path))
		if False:
			phish = [
				parse_row(row,0+EPS)
				for row in open(html_cache_table_of(phish_path))
			]
			self.phish_cache = open(html_cache_of(phish_path))
		else:
			self.phish_cache = open("/dev/null")
			phish = []
		self.data = phish + legit
		self.data = [d for d in self.data if d is not None]
		shuffle(self.data)
		self.feature_functions = feature_functions

	def retrieve(self,d):
		if d['label'] > 0.5:
			fp = self.phish_cache
		else:
			fp = self.legit_cache
		fp.seek(d['offset'])
		html = fp.read(d['len'])
		return html

	def __len__(self):
		return len(self.data)
	

class WebFeaturesDataset(GenericDataset):
	def __iter__(self):
		for d in self.data:
			if d['url'] == '':
				continue
			try:
				html = self.retrieve(d)
			except (ValueError, KeyError):
				continue
			features = []
			for fn in self.feature_functions:
				features += fn(html,d['url'])
			try:
				yield torch.tensor(features,dtype=torch.float), torch.tensor([d['label']],dtype=torch.float)
			except KeyError:
				continue

class UrlDataset(GenericDataset):
	def __iter__(self):
		for url,label in self.data:
			if ":" not in url:
				continue
			yield url,label
	def to_numpy(self):
		'''
			return data as a (X,y) data matrix for logistic regression computation
		'''
		tokenizer = UrlTokenizer()
		
		arr = [tokenizer.encode(url) for url, _ in self]
		X = numpy.concatenate(
			arr,
		)

		y = numpy.array([label for url, label in self])
		return X,y
	
