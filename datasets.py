import torch
from torch.utils.data import Dataset
import os
from os.path import dirname,join
from random import shuffle
import requests

import url_features

this = dirname(__file__)

DEFAULT_LEGITIMATE = join(this,'legitimate-urls.txt')
DEFAULT_PHISH = join(this,'phish-urls.txt')

feature_functions = [
	url_features.get_features
]

class GenericDataset(Dataset):
	def __init__(
			self,
			legitimate_path=DEFAULT_LEGITIMATE,
			phish_path=DEFAULT_PHISH,
			percent_valid=0.2,
		):
		with open(legitimate_path) as fp:
			legitimate = fp.readlines()
		with open(phish_path) as fp:
			phish = fp.readlines()

		phish = [(url,1) for url in phish]
		legitimate = [(url,0) for url in legitimate]

		self.data = phish + legitimate
		shuffle(self.data)

	def __len__(self):
		return len(self.data)
	

class WebFeaturesDataset(GenericDataset):
	def __getitem__(self,idx):
		url,label = self.data[idx]
		http = requests.get(url).text
		
		features = []
		for fn in feature_functions:
			features += fn(http,url)
		
		return torch.tensor(features), torch.tensor([label])
		
class UrlDataset(GenericDataset):
	def __getitiem__(self,idx):
		return self.data[idx]
			
