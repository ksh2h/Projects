import rake
from rake import *
file = open("../paper_abstract",'r')
for i in range(5):
	x=file.readline()
	
	rake_object = rake.Rake("SmartStoplist.txt", 5, 3, 4)
	x=x.split('\t')
	#print x
	keywords = rake_object.run(x[1])
	print "Keywords:", keywords
	print 
	print
