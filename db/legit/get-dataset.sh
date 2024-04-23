#!/bin/sh

# sorry this is whack
sudo prlimit -n4096 python crawler.py
sudo chown -R vraiti:vraiti cache

python filter-dataset.py
cp legit-urls.txt ..
