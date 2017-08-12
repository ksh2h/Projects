import psycopg2

def yearwisePublication(a,y1,y2):
    #start=time.time()
    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )

    cur = conn.cursor()
    cur.execute("SELECT \"id\" FROM \"authors\" WHERE '"+ a +"' = ANY(\"name\") ;")
    res3=cur.fetchall()
    a1=a
    a=a+"["+res3[0][0]+"]"
    if int(y2) < int(y1):
        temp=y1
        y1=y2
        y2=temp
    cur.execute("SELECT \"year\",\"field\" FROM \"papers\" WHERE \"year\" BETWEEN '" +y1+ "' AND '" +y2+ "'AND '"+ a +"'=ANY(\"authors\") ORDER BY \"year\" ;")
    res=cur.fetchall()
    x=[]
    y={}
    for row in res:
        try:
            i=0
            row[1][0]=row[1][0].replace("_"," ")
            while i<1:
                    if row[0] in x:
                        if row[1][0] in y:
                            i=1
                            ind=int(row[0])-int(y1)

                            if len(y[row[1][0]])<=ind:
                                for j in range(len(y[row[1][0]]),ind):
                                    y[row[1][0]].append(0)
                                y[row[1][0]].append(1)
                            else :
                                y[row[1][0]][ind]+=1
                        else :
                            y[row[1][0]]=[]
                    else :
                        x.append(row[0])
        except:
            print "Error"
            continue
    result={'x':x, 'y':y, 'title':'Papers by ' + a1 + 'in year range '+y1+' to '+y2,'xlabel':'year','ylabel':'papers count', 'type' : 'stacked'}
    #print time.time()-start
    return result

if __name__ == '__main__':
     a="Mohan Kamath"
     y1='1900'
     y2='2000'
     print yearwisePublication(a,y1,y2)
