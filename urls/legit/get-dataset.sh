#!/bin/sh
sudo prlimit -n4096 python crawler.py
python filter-dataset.py
cp legit-urls.txt ..
