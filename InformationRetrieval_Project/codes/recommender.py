import editdistance as ed
import psycopg2
import time
import operator

def func( f1, f2 ):
    return f1[0] < f2[0]

def author_recommend( auth, temp ):
    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
    cur = conn.cursor()
    cur.execute( 'SELECT \"name\" from \"authors\" ' )
    res = cur.fetchall()
    ed_arr = dict()
    for row in res:
        min_ed = 100
        for names in row[0]:
            curr_ed = ed.eval(names, auth)
            if curr_ed < min_ed:
                rslt = names
                min_ed = curr_ed
        ed_arr[rslt] = min_ed
    sorted_x = sorted(ed_arr.items(), key=operator.itemgetter(1))
    return sorted_x[0:10]

if __name__ == '__main__':
    st_time = time.time()
    ed_arr = author_recommend('Mohan Kamth', 'aaa')
    print ed_arr
    print time.time() - st_time
