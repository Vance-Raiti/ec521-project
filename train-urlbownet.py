from urlbownet import UrlBOWNet
from datasets import UrlDataset
import torch

N_EPOCHS = 10

data = UrlDataset()
net = UrlBOWNet()
bce = torch.nn.BCELoss()
optimizer = torch.optim.SGD(y_hat.params())

for _ in range(N_EPOCHS):
	for url,label in dataset:
		pred = net(url)
		loss = bce(pred,label)
		loss.backward()
		optimizer.step()
		print(loss.item())
			
