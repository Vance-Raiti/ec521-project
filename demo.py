from db.scrape import scrape
from db.table import main as get_ddg
from collections import deque
import sys
from preprocess import feature_functions
import torch

from model import MultiLayerPerceptron

class queue:
	def __init__(self):
		self.q = deque()

	def put(self,x):
		self.q.append(x)
	
	def get(self):
		return self.q.popleft()
	
	def qsize(self):
		return len(self.q)	
	
tensorfy = lambda x: torch.tensor(x,dtype=torch.float)

qin, qout = queue(), queue()

qin.put(sys.argv[1])
scrape(qin,qout)
url, html, page_rank, age = qout.get()
ddg = get_ddg(url)

features = []
for fn in feature_functions:
	features += fn(html,url,ddg,page_rank,age)

net = MultiLayerPerceptron()
net.load_state_dict(torch.load('model.pt'))

x = tensorfy(features)
y_hat = net(x)

print(y_hat.item())
