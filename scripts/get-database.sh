#!/bin/sh
if [ ! -f online-valid.csv ]; then
	wget http://data.phishtank.com/data/online-valid.csv.gz
	gzip -d online-valid.csv.gz
fi
./filter-dataset.py
cat urls/* > urls.txt
