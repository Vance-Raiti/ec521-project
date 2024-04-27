import torch
from torch.utils.data import IterableDataset
import os
from os.path import dirname,join,exists
from random import shuffle
import random
import requests
import numpy
from html2text import html2text

this = dirname(__file__)

EPS = 1e-5

# to ensure there's never any cross-contamination between train and valid on instantiations of GenericDataset
random.seed(0) 


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
			if len(row) != len(labels):
				return None
			d = {k:t(v) for k,v,t in zip(labels,row,types)}
			if len(d['url']) == 0:
				return None
			return d
		PHISH = 1
		LEGIT = 0	
		if use_eps:
			PHISH -= EPS
			LEGIT += EPS

		legit = [
			parse_row(row,LEGIT)
			for row in open(html_cache_table_of(legit_path))
		]
		self.legit_cache = open(html_cache_of(legit_path))
		phish = [
			parse_row(row,PHISH)
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

	def train_and_valid(self):
		self.data = self.train_data + self.valid_data

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

	def __getitem__(self,idx):
		d = self.data[idx]
		d['html'] = self.retrieve(d)
		return d
	
	def __iter__(self):
		for i in range(len(self)):
			yield self[i]

class WebFeaturesDataset(GenericDataset):
	def __iter__(self):
		for d in self.data:
			if d['url'] == '' or 'label' not in d:
				continue

			html = self.retrieve(d)
			features = []
			for fn in self.feature_functions:
				features += fn(html,d['url'])
			
			try:
				yield torch.tensor(features,dtype=torch.float), torch.tensor([d['label']],dtype=torch.float)
			except KeyError:
				continue

class PreprocessedDataset:
	def __init__(self):
		self.train_len = None
		self.test_len = None
		self.train()
	def train(self):
		self.path = 'features/features-train.txt'
		if self.train_len is None:
			self.train_len = 0
			for line in open(self.path):
				self.train_len += 1
		self.len = self.train_len

	def test(self):
		self.path = 'features/features-test.txt'
		if self.test_len is None:
			self.test_len = 0
			for line in open(self.path):
				self.test_len += 1
		self.len = self.test_len

	def __len__(self):
		return self.len

	def __iter__(self):
		tensorfy = lambda x: torch.tensor(x,dtype=torch.float)
		for line in open(self.path):
			features = line.split(',')
			features, label = features[:-1], features[-1]
			features = [
				float(feature.strip('[]')) 
				for feature in features
			]
			label = [float(label)]
			
			x,y= tensorfy(features), tensorfy(label)
			yield x,y
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

class HtmlDataset(GenericDataset):
	def __iter__(self):
		
		for i,d in enumerate(self.data):
			if self.length is not None and i > self.length:
				break
			try:
				html = self.retrieve(d)
			except (KeyError, ValueError):
				continue
			text = str(html.encode('ascii','ignore'))
			yield text	
