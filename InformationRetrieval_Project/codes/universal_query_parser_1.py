import re
import sys
'''
... author <author_name>
... by <author_name>
... author is <author_name>
... author name <author_name>

... at <venue>
... venue <venue>
... conference <venue>
... venue is <venue>
... conference is <venue>

... between <year> and <year>
... from <year> to <year>
... till <year>

... in <field>
... based on <field>
... field is <field>
... field <field>

... <author>'s coauth
... coauth of <author>

'''

'''
query 1 : a, c
query 2 : a, c
query 3 : c, y1, y2
query 4 : a, y
query 5 : y1, y2
query 6 : a, y1
query 7 : a, y2
'''

def universal_parser( query ):
    possibilities = dict()
    possibilities["author"] = [' author is (.+?) ', ' author name (.+?) ', ' author (.+?) ',
    ' by (.+?) ']
    possibilities["venue"] = [' at (.+?) ', ' venue is (.+?) ', ' conference is (.+?) ',
    ' venue (.+?) ', ' conference (.+?) ']
    possibilities["field"] = [ ' based on (.+?) ', ' field is (.+?) ', ' field (.+?) ' ]
    possibilities["coauth"] = [ ' (.+?)\'s coauth ', ' coauth of (.+?) ' ]
    '''
    for ap in auth_possib:
        for vp in venue_possib:
            possibilities.append( ap+'(.+?)'+vp+'(.+?)#' )

    for psb in possibilities:
        try:
            author = re.search(psb, query).group(1)
            venue = re.search(psb, query).group(2)
            return [True, author.strip(), venue.strip()]
        except:
            for ap in auth_possib:
            continue

    possibilities = []
        for vp in venue_possib:
            possibilities.append( vp+'(.+?)'+ap+'(.+?)#' )

    for psb in possibilities:
        try:
            author = re.search(psb, query).group(2)
            venue = re.search(psb, query).group(1)
            return [True, author.strip(), venue.strip()]
        except:
            continue
    return [False]
'''
    content = dict()
'''
    try:
        year1 = re.search( 'between (.+?) and (.+?) (&|#)', query ).group(1)
        year2 = re.search( 'between (.+?) and (.+?) (&|#)', query ).group(2)
        content["year1"] = year1
        content["year2"] = year2
    except:
        try:
            year1 = re.search( 'from (.+?) to (.+?) (&|#)', query ).group(1)
            year2 = re.search( 'from (.+?) to (.+?) (&|#)', query ).group(2)
            content["year1"] = year1
            content["year2"] = year2
        except:
            try:
                year = re.search( 'till (.+?) (&|#)', query ).group(1)
                content["year"] = year
            except:
                pass


    for key in possibilities:
        for possib in possibilities[key]:
            try:
                value = re.search( possib, query ).group(1)
                content[key] = value
                break
            except:
                continue
    print content
    if "author" in content and "venue" in content:
        return [1, content["author"], content["venue"] ]
    elif "coauth" in content and "venue" in content:
        return [2, content["coauth"], content["venue"] ]
    elif "venue" in content and "year" in content:
        return [3, content["venue"], content["year"] ]
    elif "author" in content and "year" in content:
            return [4, content["author"], content["year"] ]
    elif "author" in content and "year1" in content and "year2" in content:
        if "publication" in query:
            return [6, content["author"], content["year1"], content["year2"] ]
        elif "citation" in query:
            return [7, content["author"], content["year1"], content["year2"] ]
    elif "year1" in content and "year2" in content:
        return [5, content["year1"], content["year2"] ]
    return content
'''

    query_1_possib = []
    for 



if __name__ == '__main__':
    #query = 'author Rudolf Ahlswede (&|#)venue IEEE'
    print universal_parser( sys.argv[1] )
