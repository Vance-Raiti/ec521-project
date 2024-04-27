fp = open('features.txt')
train = open('features-train.txt','w')
test = open('features-test.txt','w')
for i,line in enumerate(fp):
	if i < 2000:
		test.write(line)
	else:
		train.write(line)
	
