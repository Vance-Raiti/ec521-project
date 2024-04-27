import torch

from datasets import PreprocessedDataset
from model import MultiLayerPerceptron
import url_features
from html_tokenizer import HtmlTokenizer

N_EPOCHS = 3
EPS = 1e-7


data = PreprocessedDataset()
for x,y in data:
	in_features = x.shape[0]
	break
net = MultiLayerPerceptron(in_features=in_features)
loss_fn = torch.nn.BCELoss()
optimizer = torch.optim.SGD(net.parameters(),lr=1e-4)

class Evaluator():
	def __init__(self):
		self.FP = 0
		self.TP = 0
		self.FN = 0
		self.TN = 0
		self.P = 0
		self.N = 0
		self.correct = 0
		self.i = 0
	def update(self,pred,label):
		self.correct += pred == label
		self.i += 1
		if label:
			self.P += 1
			if pred:
				self.TP += 1
			else:
				self.FN += 1
		else:
			self.N += 1
			if pred:
				self.FP += 1
			else:
				self.TN += 1
		
		print(f"accuracy: {self.correct/(self.i+EPS):.2}\n\
\tTP: {self.TP/(self.P+EPS):.2}\
\tFP: {self.FP/(self.P+EPS):.2}\
\tTN: {self.TN/(self.N+EPS):.2}\
\tFN: {self.FN/(self.N+EPS):.2}")



for epoch in range(N_EPOCHS):
	evaluator = Evaluator()
	data.train()
	for i,(x,y) in enumerate(data):
		y_hat = net(x)
		loss_fn(y,y_hat).backward()
		optimizer.step()
		optimizer.zero_grad()
		
		pred_phish = y_hat.item() > 0.5
		is_phish = y.item() > 0.5
		print(f"Epoch {epoch}, it {i} of {len(data)}. Predictied {round(y_hat.item(),2)} (actual {round(y.item())})")
		evaluator.update(pred_phish,is_phish)
	
	with torch.no_grad():
		data.test()
		evaluator = Evaluator()	
		for i,(x,y) in enumerate(data):
			y_hat = net(x)
			pred_phish = y_hat.item() > 0.5
			is_phish = y.item() > 0.5
			print(f"Epoch {epoch}, it {i} of {len(data)}")
			evaluator.update(pred_phish,is_phish)
torch.save(net,"model.pt")
