import psycopg2


def metapathapc(a,c):
	result = []
	conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )

	cur = conn.cursor()

	cur.execute("SELECT \"papers\" FROM \"authors\" WHERE '" + a + "' = ANY (\"name\");")
	rows = cur.fetchall()
	res_list = '('
	flag = False
	for row in rows:
		r = row[0]
		for x in r:
			#y = (x,)
			#print type(y)
			res_list = res_list+ '\'' + x+'\', '
			flag = True
	if flag:
		res_list = res_list[:-2]
	res_list = res_list+')'
	cur.execute("SELECT * FROM \"papers\" WHERE \"id\" IN "+res_list+" and \"venue\"  LIKE '%"+c+"%' and \"citers\" IS NOT NULL ORDER BY array_length(\"citers\",1) DESC ;")
	papers = cur.fetchall()
	for paper in papers:
				try:
					temp = {}
					temp['ID']=paper[0]
					temp['Title']=paper[1]
					temp['Venue']=paper[2]
					temp['Field']=paper[3]
					temp['Year']=paper[4]
					temp['Authors']=paper[5]
					temp['Citing Papers']=paper[6]
					temp['Keywords']=paper[7]
					temp['no of citers']=len(paper[8])
					result.append(temp)
				except:
					pass
	cur.execute("SELECT * FROM \"papers\" WHERE \"id\" IN "+res_list+" and \"venue\"  LIKE '%"+c+"%' and \"citers\" IS NULL;")
	papers = cur.fetchall()
	for paper in papers:
				try:
					temp = {}
					temp['ID']=paper[0]
					temp['Title']=paper[1]
					temp['Venue']=paper[2]
					temp['Field']=paper[3]
					temp['Year']=paper[4]
					temp['Authors']=paper[5]
					temp['Citing Papers']=paper[6]
					temp['Keywords']=paper[7]
					temp['no of citers']=len(paper[8])
					result.append(temp)
				except:
					pass
	return result

def aco_apc_metapath(a,c):

    conn = psycopg2.connect( database= "ir_group7" ,user = "ir7_user", password = "grp7", host = "localhost" , port = "5432" )

    cur = conn.cursor()

    cur.execute("SELECT \"id\" FROM \"authors\" WHERE '" + a + "' = ANY(\"name\");")

    rows = cur.fetchall()

    result = []



    for row in rows:
    	aid = row[0]
    	cur.execute("SELECT \"co_author\" FROM \"co_author_network\" WHERE \"id\" = '" + aid + "';")
    	coids = cur.fetchall()
        #print coids
        res_list = '('
        for co_row in coids:
            #print co_row
            coid = co_row[0]
            cur.execute("SELECT \"papers\" FROM \"authors\" WHERE  \"id\" = '" + coid+ "';")
            paperids = cur.fetchall()
            #print paperids
            for paperidrow in paperids:
                paperid = paperidrow[0]
                flag = False
                for x in paperid:
                    #y = (x,)
                    #print type(y)
                    res_list = res_list+ '\'' + x+'\', '
                    flag = True
        if flag:
                res_list = res_list[:-2]
        res_list = res_list+')'
        #print res_list
        cur.execute("SELECT * FROM \"papers\" WHERE \"id\" IN "+res_list+" and \"venue\" LIKE '%"+c+"%' and \"citers\" IS NOT NULL ORDER BY array_length(\"citers\",1) DESC ;")
        papers = cur.fetchall()
        for paper in papers:
            try:
                temp={}
                temp['ID']=paper[0]
                temp['Title']=paper[1]
                temp['Venue']=paper[2]
                temp['Field']=paper[3]
                temp['Year']=paper[4]
                temp['Authors']=paper[5]
                temp['Keywords']=paper[7]
                temp['no of citers']=len(paper[8])
                temp['Co Authors']=[]
                for z in paper[5]:
                    for ap in coids:
                        if ap[0] in z:
                            temp['Co Authors'].append(z)
                result.append(temp)
            except:
                pass
		cur.execute("SELECT * FROM \"papers\" WHERE \"id\" IN "+res_list+" and \"venue\" LIKE '%"+c+"%' and \"citers\" IS NULL;")
        papers = cur.fetchall()
        for paper in papers:
            try:
                temp={}
                temp['ID']=paper[0]
                temp['Title']=paper[1]
                temp['Venue']=paper[2]
                temp['Field']=paper[3]
                temp['Year']=paper[4]
                temp['Authors']=paper[5]
                temp['Keywords']=paper[7]
                temp['no of citers']=0
                temp['Co Authors']=[]
                for z in paper[5]:
                    for ap in coids:
                        if ap[0] in z:
                            temp['Co Authors'].append(z)
                result.append(temp)
            except:
                pass

    return result

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
	return {'x' : xd, 'y' : yd, 'title' : 'Yearwise Citation of ' + a + ' between '+ y1 + ' and ' + y2, 'xlabel' : 'year', 'ylabel' : 'count', 'type' : 'stacked'}

def papersinrange(y1,y2):
    #start=time.time()
    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )

    cur = conn.cursor()

    if int(y2) < int(y1):
        temp=y1
        y1=y2
        y2=temp
    cur.execute("SELECT \"year\",\"field\" FROM \"papers\" WHERE \"year\" BETWEEN '" +y1+ "' AND '" +y2+ "' ;")
    res=cur.fetchall()
    x=[]
    y={}
    for year in range( int(y1), int(y2) ):
		x.append( str( year ) )

    for row in res:
        for fld in row[1]:
            if fld in y:
                y[fld][ int(row[0]) - int(y1) ] = y[fld][ int(row[0]) - int(y1) ] + 1
            else:
                y[fld] = []
                for i in range(0, int(y2) - int(y1) + 1):
                    y[fld].append( 0 )
				#y[fld][ int(row[0]) - int(y1) ] = 1

    result={'x':x, 'y':y, 'title':'Papers in year range '+y1+' to '+y2,'xlabel':'year','ylabel':'papers count', 'type':'stacked'}
    #print time.time()-start
    return result


def numberofPublications(z,y1):
	#	start_time=time.time()
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

	cur.execute("SELECT \"field\" FROM \"papers\" WHERE \"venue\" LIKE '%"+ z +"%' AND \"year\" < '"+y1+"';")
	x=cur.fetchall()
	#papers werent fetched in an appropriate format, so a little processing has been done here
	for row in x:
		try:
			for f in row[0]:
				f = f.replace("_", " ")
				yd[f] = yd[f] + 1
		except:
			pass

	x = []
	y = []
	for k in yd.keys():
		if(yd[k]>0):  # Just adding the non-zero values
			x.append(k)
			y.append(yd[k])

	return {'x' : x, 'y' : y, 'title' : 'number of publications upto ' + y1 +' in various fields at '+ z, 'xlabel' : 'Field', 'ylabel' : 'number of publications', 'type':'pie'}




def yearwisePublication(a,y1,y2):
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

	cur.execute("SELECT \"field\", \"year\" FROM \"papers\" WHERE \"id\" IN " + lst + " AND \"year\" BETWEEN '" + y1 + "' AND '" + y2 +"';")
	result = cur.fetchall()

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


	return {'x' : xd, 'y' : yd, 'title' : 'Yearwise Publication of ' + a + ' between '+ y1 + ' and ' + y2, 'xlabel' : 'year', 'ylabel' : 'count', 'type' : 'stacked'}

def metapathay(a,c):
	conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )

	cur = conn.cursor()

	cur.execute("SELECT \"papers\" FROM \"authors\" WHERE '" + a + "' = ANY (\"name\");")
	rows = cur.fetchall()
	result = {}
	for row in rows:
		r = row[0]
		for x in r:
			cur.execute("SELECT * FROM \"papers\" WHERE \"id\" = '" + x + "'")
			papers = cur.fetchall()
			for paper in papers:
				try:
					if(c.decode()>=paper[4]):
						for fld in paper[3]:
							if fld not in result:
								result[ fld ] = 1
							else:
								result[ fld ] = result[ fld ] + 1
				except:
					pass
	x = []
	y = []
	for key in result:
		x.append(key)
		y.append(result[key])
	result = { 'x' : x, 'y' : y, 'title' : 'Paper vs Field distribution for '+ a +' till ' + c, 'xlabel' : 'Field', 'ylabel' : 'No. of papers', 'type':'pie'}
	return result

if __name__ == '__main__':
	a="Rudolf Ahlwede"
	y2='2016'
	print numberofPublications('IEEE', '1970')
