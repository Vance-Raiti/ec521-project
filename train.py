import torch

from datasets import WebFeaturesDataset
from model import MultiLayerPerceptron
from torch.optim.lr_scheduler import LambdaLR
N_EPOCHS = 10
EPS = 1e-7


def linear_warmup_linear_decay(n):
	if n < 20000:
		return n/20000
	return 1 - ((n-20000)/10000)

data = WebFeaturesDataset()
net = MultiLayerPerceptron(in_features=7)
loss_fn = torch.nn.BCELoss()
optimizer = torch.optim.SGD(net.parameters())
for epoch in range(N_EPOCHS):
	FP = 0
	TP = 0
	FN = 0
	TN = 0
	P = 0
	N = 0
	correct = 0
	for i,(x,y) in enumerate(data):
		y_hat = net(x)
		loss_fn(y,y_hat).backward()
		optimizer.step()
		optimizer.zero_grad()
		
		pred_phish = y_hat.item() > 0.5
		is_phish = y.item() > 0.5
		correct = pred_phish == is_phish
		if is_phish:
			P += 1
			if pred_phish:
				TP += 1
			else:
				FN += 1
		else:
			N += 1
			if pred_phish:
				FP += 1
			else:
				TN += 1

		print(f"Epoch {epoch}, iteration {i}\n\
\taccuracy: {correct/(i+EPS)}\n\
\tTP: {TP/(P+EPS)}\n\
\tFP: {FP/(P+EPS)}\n\
\tTN: {TN/(N+EPS)}\n\
\tFN: {FN/(N+EPS)}\n")
		

torch.save(net,"model.pt")
