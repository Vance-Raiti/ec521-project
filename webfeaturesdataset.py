from datasets import GenericDataset
import torch
import url_features

DEFAULT_FEATURE_FUNCTIONS = [
	url_features.get_features
]


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


