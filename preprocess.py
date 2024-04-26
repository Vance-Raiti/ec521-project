from datasets import GenericDataset
import multiprocessing as mp
import torch
import url_features
import sys

NUM_WORKERS = 1
Q_MAXSIZE = 64

start = int(sys.argv[1])

feature_functions = [url_features.get_features]


def int2bytes(n,size):
	out = b''
	

def process(*args,**kwargs):
	try:
		process_(*args,**kwargs)
	except KeyboardInterrupt:
		return

def process_(qin,qout):
	while True:
		data = qin.get()
		if data == 'END':
			break
		features = []
		html = data['html']
		url = data['url']
		label = data['label']
		for fn in feature_functions:
			features += fn(html,url)
		features += [label]
		qout.put(features)

def consume(qout):
	output = open("features.txt","a")
	while True:
		features = qout.get()
		if features == "END":
			break
		features = [str(feature) for feature in features]
		print(','.join(features),file=output)	
		
dataset = GenericDataset()
stop = min(start+10000,len(dataset))

qin, qout = mp.Queue(Q_MAXSIZE), mp.Queue(Q_MAXSIZE)

workers = [
	mp.Process(
		target = process,
		args = (qin,qout,),
	)
	for _ in range(NUM_WORKERS)
]

for worker in workers:
	worker.start()

consumer = mp.Process(
	target = consume,
	args = (qout,),
)

consumer.start()

dataset.train_and_valid()
for i in range(start,stop):
	qin.put(dataset[i])
	print(f"{i:5} of {len(dataset)}. {qin.qsize()} {qout.qsize()}")

for _ in range(NUM_WORKERS):
	qin.put("END")

for worker in workers:
	worker.join()

qout.put("END")
consumer.join()
