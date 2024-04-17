import multiprocessing as mp

N = 512
pipes = [
	mp.Pipe()
	for _ in range(N)
]

for pipe in pipes:
	print(pipe)
