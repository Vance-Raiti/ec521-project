from tokenizers import Tokenizer
from os.path import exists
import numpy


from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from parse import parse

from sklearn.linear_model import LogisticRegression
from tokenizers import Tokenizer
from datasets import UrlDataset
import pickle

VOCAB_SIZE = 200

class UrlTokenClassifier:
	def __init__(self):
		if not exists('url-tokenizer.json'):
			self.train_tokenizer()	
		self.tokenizer = Tokenizer.from_file('url-tokenizer.json')

		if not exists('url-classifier.pkl'):
			self.train_classifier()
		with open("url-classifier.pkl","rb") as fp:
			self.classifier = pickle.load(fp)


	def train_tokenizer(self):
		urls = [url for url,label in UrlDataset()]
		tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
		tokenizer.pre_tokenizer = Whitespace()
		trainer = BpeTrainer(vocab_size=VOCAB_SIZE,special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
		tokenizer.train_from_iterator(urls,trainer)
		tokenizer.save("url-tokenizer.json")

	def block(self,data):
		X = numpy.concatenate(
			[
				self.encode(url)
				for url,_ in data
			]
		)
		y = numpy.array([ label for _,label in data]) 
		return X, y
			
		
	def train_classifier(self):
		data = UrlDataset(use_eps=False)
		self.classifier = LogisticRegression()
		print("training token classifier...")
		self.classifier.fit(*self.block(data))
		print("scoring token classifier...")
		data.valid()
		score = self.classifier.score(*self.block(data))
		print(f"url classifier has mean score {score}")
		with open("url-classifier.pkl","wb") as fp:
			pickle.dump(self.classifier,fp)

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
