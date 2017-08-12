import time

def checkintrie(t,word):
	cur=t
	for letter in word:
		#print "letter is ",letter
		if letter in cur:
			cur=cur[letter]
		else:
			return False
		#print cur
	if "_end_" in cur:
		return True
	else:
		return False

if __name__ =="__main__":
	t=dict()
	file=open("../paper_authors",'r')
	i=0
	w=file.readline()
	start_time=time.time()
	while(w):
		i+=1
		if(i%1000==0):
			print i
		w=w.split('\t')[1]
		w=w.split('[')[0]
		cur = t
		for letter in w:
			cur=cur.setdefault(letter,{})
		cur["_end_"]="_end_"
		w=file.readline()	
	print len(t.keys())
	print t.keys()
	print time.time()-start_time
	start_time=time.time()	
	print checkintrie(t,"Ning Cai")
	print time.time()-start_time
	#print checkintrie(t,"hel")
