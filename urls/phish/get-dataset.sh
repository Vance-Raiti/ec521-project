#!/bin/sh
if [ ! -f online-valid.csv ]; then
	wget http://data.phishtank.com/data/online-valid.csv.gz
	gzip -d online-valid.csv.gz
fi

./filter-dataset.py 2>/dev/null

cat urls/header.txt urls/urls*.txt > urls.txt

./format-dataset.py
cp phish-urls.txt ..
