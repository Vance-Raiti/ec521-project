from tokenizers import Tokenizer
from os.path import exists
import numpy


from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from parse import parse

from datasets import HtmlDataset

from html2text import html2text

VOCAB_SIZE = 2000

class HtmlTokenizer:
	def __init__(self):
		if not exists('html-tokenizer.json'):
			self.train_tokenizer()	
		self.tokenizer = Tokenizer.from_file('html-tokenizer.json')

	def train_tokenizer(self):
		html = HtmlDataset(length = 7000)
		tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
		tokenizer.pre_tokenizer = Whitespace()
		trainer = BpeTrainer(vocab_size=VOCAB_SIZE,special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
		tokenizer.train_from_iterator(html,trainer)
		tokenizer.save("html-tokenizer.json")

	def encode(self,html):
		text = html2text(html)
		text = str(text.encode('ascii','ignore'))
		ids = self.tokenizer.encode(html).ids
		x = [0 for _ in range(VOCAB_SIZE)]
		for i in ids:
			x[i] = 1
		return x
	
	def __call__(self, html, url):
		x = self.encode(html)
		return x

if __name__ == "__main__":
	HtmlTokenizer()
