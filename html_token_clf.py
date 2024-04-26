from tokenizers import Tokenizer
from os.path import exists
import numpy


from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from parse import parse

from bs4 import BeautifulSoup as bs

VOCAB_SIZE = 200

class UrlTokenClassifier:
	def __init__(self):
		if not exists('html-tokenizer.json'):
			self.train_tokenizer()	
		self.tokenizer = Tokenizer.from_file('html-tokenizer.json')

	def train_tokenizer(self):
		htmls = [html for html,label in HtmlDataset()]
		tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
		tokenizer.pre_tokenizer = Whitespace()
		trainer = BpeTrainer(vocab_size=VOCAB_SIZE,special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
		tokenizer.train_from_iterator(htmls,trainer)
		tokenizer.save("html-tokenizer.json")

	def encode(self,string):
		string = string.split(":")
		string = string[1]
		string = string.replace("/"," ")
		ids = self.tokenizer.encode(string).ids
		x = numpy.zeros((1,VOCAB_SIZE))
		for i in ids:
			x[0,i] = 1
		return x
	
	def __call__(self,string):
		x = self.encode(string)
		y_hat = self.classifier.predict(x)
		return y_hat

if __name__ == "__main__":
	UrlTokenClassifier()
