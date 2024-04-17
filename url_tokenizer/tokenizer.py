from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import torch

tokenizer = Tokenizer.from_file("url-tokenizer.json")

with open(
