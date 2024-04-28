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

class GenericDataset:
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
		def parse_row(row):
			row = row.strip().split(',')
			labels = [
				'url',
				'html_offset','html_len',
				'page_rank_offset','page_rank_len',
				'age',
				'label',
				'ddg_offset','ddg_len'
			]
			types = [
				str,
				int,int,
				int,int,
				int,
				float,
				int,int
			]
			if len(row) != len(labels):
				return None
			d = {k:t(v) for k,v,t in zip(labels,row,types)}
			if len(d['url']) == 0:
				return None
			return d

		data = [
			parse_row(row)
			for row in open('cache/cache_table.csv')
		]
		self.cache = open('cache/cache.txt')

		shuffle(data)
		split = int(len(data)*valid_split)
		self.valid_data = data[:split]
		self.train_data = data[split:]
		self.data = self.train_data
	
	def train(self):
		self.data = self.train_data
	
	def valid(self):
		self.data = self.valid_data

	def train_and_valid(self):
		self.data = self.train_data + self.valid_data

	def retrieve(self,d):
		fp = self.cache
	
		fp.seek(d['html_offset'])
		html = fp.read(d['html_len'])
		
		fp.seek(d['ddg_offset'])
		ddg = fp.read(d['ddg_len'])
		
		fp.seek(d['page_rank_offset'])
		page_rank = fp.read(d['page_rank_len'])
		return html, ddg, page_rank

	def __len__(self):
		return len(self.data)

	def __getitem__(self,idx):
		d = self.data[idx]
		d['html'], d['ddg'], d['page_rank'] = self.retrieve(d)
		return d
	
	def __iter__(self):
		for i in range(len(self)):
			yield self[i]


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
