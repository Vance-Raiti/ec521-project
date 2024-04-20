from sklearn.linear_model import LogisticRegression
from tokenizers import Tokenizer
from datasets import UrlDataset
from pickle import dump

X,y = UrlDataset().to_numpy()
clf = LogisticRegression().fit(X,y)

