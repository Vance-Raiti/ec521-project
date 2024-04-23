import torch

class MultiLayerPerceptron(torch.nn.Module):
	def __init__(self,in_features=15, width=20, depth=3):
		super().__init__()
		self.layers = torch.nn.Sequential(*[
			torch.nn.Linear(in_features,width),
			torch.nn.ReLU(),
			torch.nn.Sequential(*[
					torch.nn.Sequential(*[
						torch.nn.Linear(width,width),
						torch.nn.ReLU(),
					])
					for _ in range(depth)
			]),
			torch.nn.Linear(width,1),
			torch.nn.Sigmoid(),
		])

	def forward(self,x):
		return self.layers(x)
