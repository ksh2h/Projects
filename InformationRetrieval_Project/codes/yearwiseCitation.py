import psycopg2
import time
def yearwiseCitation(a,y1,y2):
	conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
	cur = conn.cursor()

	cur.execute("SELECT \"papers\" FROM \"authors\" WHERE '" + a + "' = ANY (\"name\");")
	x=cur.fetchall()

	lst = '('
	flag = False
	for row in x:
		for pid in row[0]:
			lst = lst + '\'' + pid + '\', '
			flag = True
	if flag:
		lst = lst[:-2]
	lst = lst+')'
	cur.execute("SELECT \"citers\" FROM \"papers\" WHERE \"id\" IN " + lst + ";")
	result = cur.fetchall()

	lst = '('
	flag = False
	print result
	for row in result:
		try:
			for ctr in row[0]:
				lst = lst + '\'' + ctr + '\', '
				flag = True
		except:
			pass
	if flag:
		lst = lst[:-2]
	lst = lst+')'
	cur.execute("SELECT \"field\", \"year\" FROM \"papers\" WHERE \"id\" IN " + lst + " AND \"year\" BETWEEN '" + y1 + "' AND '" + y2 +"';")
	result = cur.fetchall()
	print lst

	xd = []
	yd = {}
	for i in range( int(y1), int(y2) + 1 ):
		xd.append( str(i) )

	for row in result:
		for fld in row[0]:
			if fld in yd:
				yd[fld][ int(row[1]) - int(y1) ] = yd[fld][ int(row[1]) - int(y1) ] + 1
			else:
				yd[fld] = []
				for i in range(0, int(y2) - int(y1) + 1):
					yd[fld].append( 0 )
				yd[fld][ int(row[1]) - int(y1) ] = 1


	return {'x' : xd, 'y' : yd, 'title' : 'Yearwise Citation', 'xlabel' : 'year', 'ylabel' : 'count', 'type' : 'stacked'}

if __name__=="__main__":
	c="Combinatorics, Probability & Computing - CPC[87], vol. 2, pp. 211-220"
	a="287144"
	a="Thomas S. Huang"
	y1="1900"
	y2="2010"
	print yearwiseCitation(a,y1,y2)
