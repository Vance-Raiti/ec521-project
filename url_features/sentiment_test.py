#!/bin/python
from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
data = ["ok, I don't know how I feel about that", "I hate you"]
y_hat = sentiment_pipeline(data)
print(y_hat)
