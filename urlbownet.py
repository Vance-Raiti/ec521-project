import torch.nn as nn
from torch.nn import functional as F
from tokenizers import Tokenizer


class UrlBOWNet(nn.Module):
	def __init__(self):
		super().__init__()
		self.linear = nn.Linear(30000,1)
		self.tokenizer = Tokenizer.from_file("url_tokenizer/url-tokenizer.json")
	def forward(self,url):
		return F.sigmoid(self.layers(x))
