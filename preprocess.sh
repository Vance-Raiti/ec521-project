#!/bin/bash

for (( N=0; N<=10000; N+=2000 )); do
	python preprocess.py $N
done
