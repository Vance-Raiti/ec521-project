import torch
from torch.utils.data import IterableDataset
import os
from os.path import dirname,join,exists
from random import shuffle
import requests
import numpy
from Scrapy import Retrieve_Html, Check_BadActionFields, Check_NonMatchingURLs, Check_OutOfPositionBrandName, Check_LoginForm

this = dirname(__file__)

EPS = 1e-5

DEFAULT_LEGITIMATE = join(this,'db/legit')
DEFAULT_PHISH = join(this,'db/phish')
i = 0
class GenericDataset(IterableDataset):
	def __init__(
			self,
			feature_functions=None,
			legit_path=DEFAULT_LEGITIMATE,
			phish_path=DEFAULT_PHISH,
			valid_split=0.2,
			length=None,
			use_eps=True,
		):
		self.length = length		
		self.feature_functions = feature_functions
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
		
		if use_eps:
			POS = 1-EPS
			NEG = 0+EPS
		else:
			POS = 1
			NEG = 0 

		legit = [
			parse_row(row,NEG)
			for row in open(html_cache_table_of(legit_path))
		]
		self.legit_cache = open(html_cache_of(legit_path))
		phish = [
			parse_row(row,POS)
			for row in open(html_cache_table_of(phish_path))
		]
		self.phish_cache = open(html_cache_of(phish_path))
		
		data = phish + legit
		data = [d for d in data if d is not None]
		
		shuffle(data)
		split = int(len(data)*valid_split)
		self.valid_data = data[:split]
		self.train_data = data[split:]
		self.data = self.train_data
		self.feature_functions = feature_functions
	
	def train(self):
		self.data = self.train_data
	
	def valid(self):
		self.data = self.valid_data

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

			features = []
			for fn in self.feature_functions:
				features += fn(html,d['url'])
			try:
				yield torch.tensor(features,dtype=torch.float), torch.tensor([d['label']],dtype=torch.float)
			except KeyError:
				continue

			try:
				yield self.retrieve(d)
			except (ValueError, KeyError):
				continue


	
class UrlDataset(GenericDataset):
	def __iter__(self):
		for i,d in enumerate(self.data):
			if self.length is not None and i > self.length:
				break
			try:
				if ':' not in d['url']:
					continue
				yield d['url'],d['label']
			except KeyError:
				continue
