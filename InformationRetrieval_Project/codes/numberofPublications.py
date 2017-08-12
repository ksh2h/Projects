import psycopg2
import time
def numberofPublications(z,y):
	start_time=time.time()
	conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
	cur = conn.cursor()

	yd=dict()
	cur.execute("SELECT \"field\" FROM \"fields\";")
	curs=cur.fetchall()
	for rw in curs:
		rw=list(rw)
        	rw[0]=rw[0].replace("_", " ")
		#print rw[0]
		yd[rw[0]]=0

	cur.execute("SELECT \"papers\" FROM \"venues\" WHERE \"venue\" = '"+ z +"';")
	x=cur.fetchall()

	#papers werent fetched in an appropriate format, so a little processing has been done here

	x= x[0][0][1:-1]
	x=x.split(',')
	y=[]
	for i in x:
		j=0
		while(i[j]!='"'):
			j+=1
		k=j+1
		while(i[k]!='"'):
			k+=1
		y.append(i[j+1:k])

	#Now y has all the ids of papers published in the conference in 'String' format

	for i in y:
		cur.execute("SELECT \"field\" FROM \"papers\" WHERE \"id\" = '"+ i +"';")
		z=cur.fetchall()
		try:
			#rw[0]=rw[0].replace("_", " ")
			m= z[0][0][0].replace("_"," ")
			#print m
			yd[m]+=1
		except:
			pass

	x = []
	y = []
	for k in yd.keys():
		if(yd[k]>0):  # Just adding the non-zero values
			x.append(k)
			y.append(yd[k])
	return {'x' : x, 'y' : y, 'title' : 'number of publications upto a year in various fields', 'xlabel' : 'Field', 'ylabel' : 'number of publications'}

if __name__=="__main__":
	z="Uncertainty in Artificial Intelligence - UAI[427], pp. 85-93"
	#a="287144"
	#a="Rudolf Ahlswede"
	#y1=1900
	y=2010
	print numberofPublications(z,y)
