import json
from global_variable_def import *
import psycopg2

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
						if paper[3] not in result:
							result[ paper[3] ] = 1
						else
							result[ paper[3] ] = result[ paper[3] ] + 1
				except:
					pass
	x = []
	y = []
	for key in result:
		x.append(key)
		y.append(result[key])
	result = { 'x' = x, 'y' = y, 'title' : 'Paper vs Field distribution for '+ a +' till ' + c, 'xlabel' = 'Field', 'ylabel' = 'No. of papers'}
	return result
