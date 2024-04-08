def parse(path):
	with open(path) as fp:
		data = fp.read()
	data = data.split('\n')
	header, data = data[0], data[1:]
	p = lambda s: s.split(',')
	data = [
		{
			k:v
			for k,v in zip( p(header), p(entry) )
		}
		for entry in data if len(p(header)) == len(p(entry))
	]
	return data

def pack(data,path):
	header = ','.join(data[0].keys())
	with open(path,'w') as fp:
		print(header,file=fp)
		for entry in data:
			print(
				','.join(entry.values()),
				file=fp
			)
