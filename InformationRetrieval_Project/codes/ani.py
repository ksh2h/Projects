import json
file = open("../paper_authors",'r')
l=[]
s=file.readline()
ani = dict()
i=0
while(s):
	if(i%1000==0):
		print i
	try:
		s=s[:-1]
		s = s.split('\t')
		s = s[1]
		s=s.split('[')
		ani[s[0]]=s[1][:-1]
		s=file.readline()
		i+=1
	except:
		pass
file = open("../output-files/ani_new.json",'w')
json.dump(ani,file)

#Checking the dumped file

file = open("../output-files/ani_new.json",'r')
data=json.load(file)
print data.keys()[0]
print data[data.keys()[0]]

