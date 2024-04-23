#!/bin/sh

if [ ! -f online-valid.csv ]; then
	wget http://data.phishtank.com/data/online-valid.csv.gz
	gzip -d online-valid.csv.gz
fi

python filter-dataset.py
cat urls/header.txt urls/urls*.txt > urls.txt
python format-dataset.py

cp phish-urls.txt ..
