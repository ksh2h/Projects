import psycopg2

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
		x.append( str(year - int( y1 ) ) )


    '''for row in res:
        try:
            i=0
            row[1][0]=row[1][0].replace("_"," ")
            #print row[0],row[1][0]
            while i<1:
                    if row[0] in x:
                        if row[1][0] in y:
                            i=1
                            ind=int(row[0])-int(y1)
                            #print ind
                            #print len(y[row[1][0]])
                            if len(y[row[1][0]])<=ind:
                                for j in range(len(y[row[1][0]]),ind):
                                    y[row[1][0]].append(0)
                                y[row[1][0]].append(1)
                            else :
                                y[row[1][0]][ind]+=1
                        else :
                            y[row[1][0]]=[]
    #                else :
    #                    x.append(row[0])
        except:
            print "error occured"
            continue
    '''

    for row in res:
        for fld in row[1]:
            if fld in y:
                y[fld][ int(row[0]) - int(y1) ] = y[fld][ int(row[0]) - int(y1) ] + 1
            else:
                y[fld] = []
                for i in range(0, int(y2) - int(y1) + 1):
                    y[fld].append( 0 )

    result={'x':x, 'y':y, 'title':'Papers in year range '+y1+' to '+y2,'xlabel':'year','ylabel':'papers count'}
    #print time.time()-start
    return result

if __name__ == '__main__':
     y1='1900'
     y2='2010'
     print papersinrange(y1,y2)
