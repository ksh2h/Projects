from global_variable_def import *
from util_classes import *
import json
import psycopg2
import sys

def string_cleaner(line):
    line = line[:-1]
    line = line.replace('"', '')
    try:
        line = line.encode('ascii')
    except ValueError:
        line = line
    return line

def is_pure_string( string ):
    for c in string:
        if( (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') ):
            continue
        else:
            return False
    return True

def create_paper_nodes(  ):
    citation_file_handle = open(citation_network, 'r')
    paper_author_file_handle = open(paper_authors, 'r')
    paper_venue_file_handle = open(paper_venue, 'r')
    paper_title_file_handle = open(paper_title, 'r')
    paper_year_file_handle = open(paper_year, 'r')
    paper_field_file_handle = open(paper_fields, 'r')

    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
    cur = conn.cursor()

    paper_node_dict = {}
    while True :
        line3 =  paper_venue_file_handle.readline()
        line3 = string_cleaner(line3)
        if(line3 == ''):
            break
        line_contents = line3.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        venue = line_contents[1]
        paper_node_dict[paper_id] = {}
        paper_node_dict[paper_id]["Venue"] = venue
        paper_node_dict[paper_id]["Citing Papers"] = []
        paper_node_dict[paper_id]["Authors"] = []
        paper_node_dict[paper_id]["Fields"] = []
        paper_node_dict[paper_id]["Keywords"] = []
    print 'venue done'

    while True :
        # for getting title

        line1 = paper_title_file_handle.readline()
        line1 = string_cleaner(line1)
        if( line1 == '' ):
            break
        line_contents = line1.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        title = line_contents[1]
        if paper_id in paper_node_dict:
            paper_node_dict[paper_id]["Title"] = title
    print 'title done'

        # for getting year

    while True:
        line4 =  paper_year_file_handle.readline()
        line4 = string_cleaner(line4)
        if( line4 == '' ):
            break
        line_contents = line4.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        year = line_contents[1]
        if paper_id in paper_node_dict:
            paper_node_dict[paper_id]["Year"] = year

        # for getting cited paper array
    print 'year done'
    while True:
        line5 = citation_file_handle.readline()
        line5 = string_cleaner(line5)
        if(line5 == ''):
            break
        line_contents = line5.split('\t')
        try:
            citer_id =  int( line_contents[0] )
        except ValueError:
            continue
        if citer_id not in paper_node_dict:
            continue
        try:
            cited_paper_id =  int( line_contents[1] )
        except ValueError:
            continue
        paper_node_dict[citer_id]["Citing Papers"].append( cited_paper_id )
    print 'ctation done'

        # for getting author array
    while True:
        line6 = paper_author_file_handle.readline()
        line6 = string_cleaner(line6)
        if(line6 == ''):
            break
        line_contents = line6.split('\t')
        try:
            temp_id = int( line_contents[0] )
        except ValueError:
            continue
        if temp_id not in paper_node_dict:
            continue
        paper_node_dict[temp_id]["Authors"].append( line_contents[1] )
    print 'author done'
    while True:
        line7 = paper_field_file_handle.readline()
        line7 = string_cleaner( line7 )
        if(line7 == ''):
            break
        line_contents = line7.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        if paper_id not in paper_node_dict:
            continue
        paper_node_dict[paper_id]["Fields"].append( line_contents[1] )

    print 'fields done'

    print len(paper_node_dict)

    for paper_id in paper_node_dict:
        node = paper_node_dict[paper_id]
        if "Year" not in node or "Title" not in node:
            continue
        fq = "{"
        for f in node["Fields"]:
            fq += "\"" + f + "\", "
        if len(node["Fields"]) > 0:
            fq = fq[:-2]
        fq += "}"

        aq = "{"
        for a in node["Authors"]:
            aq += "\"" + str(a) + "\", "
        if len(node["Authors"]) > 0:
            aq = aq[:-2]
        aq += "}"

        cpq = "{"
        for cp in node["Citing Papers"]:
            cpq += "\"" + str(cp) + "\", "
        if len(node["Citing Papers"]) > 0:
            cpq = cpq[:-2]
        cpq += "}"

        kq = "{}"

        cur.execute("""INSERT INTO PAPERS VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""", (str(paper_id), node["Title"], node["Venue"], fq, str(node["Year"]), aq, cpq, kq ))

        print 'paper id completed : '+str(paper_id)

    conn.commit()
    conn.close()
    citation_file_handle.close()
    paper_author_file_handle.close()
    paper_venue_file_handle.close()
    paper_title_file_handle.close()
    paper_year_file_handle.close()
    paper_field_file_handle.close()
    print 'files closed'


def add_keywords():
    paper_abstract_file_handle = open(paper_abstract, 'r')
    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
    cur = conn.cursor()
    cnt = 1763889
    while True:
        k_array = []
        line8 = paper_abstract_file_handle.readline()
        line8 = string_cleaner( line8 )
        if line8 == '':
            break;
        line_contents = line8.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        all_words = line_contents[1].split(' ')
        for i in all_words:
            if( len(i) > 3 and is_pure_string( i ) and i not in k_array ):
                k_array.append(i)
        kq = "{"
        for k in k_array:
            kq += "\"" + k + "\", "
        if len(k_array) > 0:
            kq = kq[:-2]
        kq += "}"
        cur.execute( """UPDATE papers SET keywords = %s WHERE id = %s;""", (kq, str(paper_id) ))
        cnt = cnt-1
        print str(cnt)
    #cur.execute( "DELETE FROM papers WHERE keywords = '{}'" )
    conn.commit()
    conn.close()

    paper_abstract_file_handle.close()


def create_author_nodes():
    paper_author_file_handle = open(paper_authors, 'r')
    author_dict = {}
    curr_authors = []
    prev_id = 15
    paper_id = 15
    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
    cur = conn.cursor()

    while prev_id == paper_id:
        line = paper_author_file_handle.readline()
        if(line == ''):
            break
        line = string_cleaner( line )
        line_contents = line.split('\t')
        prev_id = paper_id
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        try:
            open_bracket_pos = line_contents[1].index('[')
            close_bracket_pos = line_contents[1].index(']')
            author_id = line_contents[1][open_bracket_pos+1:close_bracket_pos]
            author_name = line_contents[1][:open_bracket_pos]
            author_id = int(author_id)
        except ValueError:
            author_id = -1
        if author_id in author_dict:
            author_dict[author_id]['Papers'].append( paper_id )
        elif( author_id != -1 ):
            author_dict[author_id] = {}
            author_dict[author_id]['Papers'] = [ paper_id ]
            author_dict[author_id]['Name'] = author_name
            author_dict[author_id]['Co Authors'] = {}
        if( paper_id == prev_id ):
            curr_authors.append( author_id )
        else:
            for i in range( 0, len( curr_authors ) ):
                if( curr_authors[i] == -1 ):
                    continue
                for j in range( 0, len( curr_authors ) ):
                    if( i == j or curr_authors[j] == -1 ):
                        continue
                    else:
                        if( curr_authors[j] in author_dict[curr_authors[i]]['Co Authors'] ):
                            author_dict[curr_authors[i]]['Co Authors'][curr_authors[j]] = author_dict[curr_authors[i]]['Co Authors'][curr_authors[j]] + 1
                        else:
                            author_dict[curr_authors[i]]['Co Authors'][curr_authors[j]] = 1
            curr_authors = [ author_id ]
            prev_id = paper_id
        print 'paper-author'+str( paper_id )
    paper_author_file_handle.close()

    for author in author_dict:
        ap = "{"
        for k in author_dict[author]["Papers"]:
            ap += "\"" + str(k) + "\", "
        if len(author_dict[author]) > 0:
            ap = ap[:-2]
        ap += "}"

        cur.execute( """INSERT INTO AUTHORS VALUES(%s, %s, %s);""", (str(author), ap, author_dict[author]["Name"] ))
        for co_auth in author_dict[author]["Co Authors"]:
            cur.execute( """INSERT INTO CO_AUTHOR_NETWORK VALUES(%s, %s, %s);""", (str(author), str(co_auth), author_dict[author]["Co Authors"][co_auth] ))
        print str(author)
    conn.commit()
    conn.close()

''' author_json_handle = open( author_nodes_json, 'w' )
    author_nodes_json_object = {}
    author_nodes_json_object['Authors'] = author_dict
    json.dump( author_nodes_json_object , author_json_handle )
    author_json_handle.close()
'''

def create_venue_nodes():
    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
    cur = conn.cursor()

    paper_venue_file_handle = open(paper_venue, 'r')
    venue_dict = {}
    while True:
        line = paper_venue_file_handle.readline()
        if( line == '' ):
            break
        line = string_cleaner( line )
        line_contents = line.split('\t')
        try:
            paper_id = int(line_contents[0])
        except ValueError:
            continue
        venue = line_contents[1]
        if venue in venue_dict:
            venue_dict[ venue ].append( paper_id )
        else:
            venue_dict[ venue ] = [ paper_id ]
        print 'paper-venue'+str( paper_id )
    paper_venue_file_handle.close()

    for venue in venue_dict:
        ap = "{"
        for k in venue_dict[venue]:
            ap += "\"" + str(k) + "\", "
        if len(venue_dict[venue]) > 0:
            ap = ap[:-2]
        ap += "}"

        cur.execute( """INSERT INTO VENUES VALUES(%s, %s);""", (venue, ap ))
    conn.commit()
    conn.close()

'''
    venue_json_handle = open( venue_nodes_json, 'w' )
    venue_nodes_json_object = {}
    venue_nodes_json_object['Venues'] = venue_dict
    json.dump( venue_nodes_json_object, venue_json_handle )
    venue_json_handle.close()
'''

def create_field_nodes():
    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
    cur = conn.cursor()

    paper_field_file_handle = open(paper_fields, 'r')
    field_dict = {}
    while True:
        line = paper_field_file_handle.readline()
        if( line == '' ):
            break
        line = string_cleaner( line )
        line_contents = line.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        field = line_contents[1]
        if field in field_dict:
            field_dict[ field ].append( paper_id )
        else:
            field_dict[ field ] = [ paper_id ]
        print 'paper-field'+str( paper_id )
    paper_field_file_handle.close()

    for field in field_dict:
        ap = "{"
        for k in field_dict[field]:
            ap += "\"" + str(k) + "\", "
        if len(field_dict[field]) > 0:
            ap = ap[:-2]
        ap += "}"

        cur.execute( """INSERT INTO FIELDS VALUES(%s, %s);""", (field, ap ))
    conn.commit()
    conn.close()

'''field_json_handle = open( field_nodes_json, 'w' )
    field_nodes_json_object = {}
    field_nodes_json_object['Fields'] = field_dict
    json.dump( field_nodes_json_object, field_json_handle )
    field_json_handle.close()
'''

def create_year_nodes():
    conn = psycopg2.connect( database = "ir_group7", user = "ir7_user", password = "grp7", host = "localhost", port ="5432" )
    cur = conn.cursor()

    paper_year_file_handle = open(paper_year, 'r')
    year_dict = {}
    while True:
        line = paper_year_file_handle.readline()
        if( line == '' ):
            break
        line = string_cleaner( line )
        line_contents = line.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        try:
            year = line_contents[1]
        except ValueError:
            continue
        if year in year_dict:
            year_dict[ year ].append( paper_id )
        else:
            year_dict[ year ] = [ paper_id ]
        print 'paper-year'+str( paper_id )
    paper_year_file_handle.close()

    for year in year_dict:
        ap = "{"
        for k in year_dict[year]:
            ap += "\"" + str(k) + "\", "
        if len(year_dict[year]) > 0:
            ap = ap[:-2]
        ap += "}"

        cur.execute( """INSERT INTO YEARS VALUES(%s, %s);""", (year, ap ))
    conn.commit()
    conn.close()


    '''year_json_handle = open( year_nodes_json, 'w' )
    year_nodes_json_object = {}
    year_nodes_json_object['Years'] = year_dict
    json.dump( year_nodes_json_object, year_json_handle )
    year_json_handle.close()'''
