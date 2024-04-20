from tokenizers import Tokenizer
import numpy

class UrlTokenizer:
	def __init__(self):
		self.tokenizer = Tokenizer.from_file('url_tokenizer/url-tokenizer.json')
	
	def encode(self,string):
		string = string.split(":")
		print(string)
		string = string[1]
		string = string.replace("/"," ")
		ids = self.tokenizer.encode(string).ids
		x = numpy.zeros((1,30000))
		for i in ids:
			x[0,i] = 1
		return x
