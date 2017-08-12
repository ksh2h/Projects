import json
from global_variable_def import *
import psycopg2

def metapathapc(a,c):
	conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )

	cur = conn.cursor()

	cur.execute("SELECT \"papers\" FROM \"authors\" WHERE '" + a + "' = ANY (\"name\");")
	rows = cur.fetchall()
	for row in rows:
		r = row[0]
		result = {}
		for x in r:
			cur.execute("SELECT * FROM \"papers\" WHERE \"id\" = '" + x + "' and \"venue\"  LIKE '%"+c+"%';")
			print cur.mogrify("SELECT * FROM \"papers\" WHERE \"id\" = '" + x + "' and \"venue\"  LIKE '%"+c+"%';")
			papers = cur.fetchall()
			for paper in papers:
				try:
					result[x] = {}
					result[x]['Title']=paper[1]
					result[x]['Venue']=paper[2]
					result[x]['Field']=paper[3]
					result[x]['Year']=paper[4]
					result[x]['Authors']=paper[5]
					result[x]['Citing Papers']=paper[6]
					result[x]['Keywords']=paper[7]
				except:
					pass
	return result

if __name__=="__main__":
	#c="Combinatorics, Probability & Computing - CPC[87], vol. 2, pp. 211-220"
	c="IEEE"
	a="287144"
	a="Xiaojie Wang"
	print metapathapc(a,c)
