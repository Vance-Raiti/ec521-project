import torch
from torch.utils.data import IterableDataset
import os
from os.path import dirname,join
from random import shuffle
import requests
import numpy
from urltokenizer import UrlTokenizer

import url_features


this = dirname(__file__)

EPS = 1e-5

DEFAULT_LEGITIMATE = join(this,'urls/legit-urls.txt')
DEFAULT_PHISH = join(this,'urls/phish-urls.txt')

DEFAULT_FEATURE_FUNCTIONS = [
	url_features.get_features
]

class GenericDataset(IterableDataset):
	def __init__(
			self,
			legitimate_path=DEFAULT_LEGITIMATE,
			phish_path=DEFAULT_PHISH,
			feature_functions= DEFAULT_FEATURE_FUNCTIONS,
			percent_valid=0.2,
		):
		with open(legitimate_path) as fp:
			legitimate = fp.readlines()
		with open(phish_path) as fp:
			phish = fp.readlines()

		phish = [(url,1-EPS) for url in phish]
		legitimate = [(url,0+EPS) for url in legitimate]

		self.data = phish + legitimate
		shuffle(self.data)

		self.feature_functions = feature_functions

	def __len__(self):
		return len(self.data)
	

class WebFeaturesDataset(GenericDataset):
	def __iter__(self):
		for url, label in self.data:
			if ":" not in url:
				continue

			try:
				html = requests.get(url,timeout=5).text
			except:
				continue


			features = []
			for fn in self.feature_functions:
				features += fn(html,url)
			
			yield torch.tensor(features,dtype=torch.float), torch.tensor([label],dtype=torch.float)
		
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
