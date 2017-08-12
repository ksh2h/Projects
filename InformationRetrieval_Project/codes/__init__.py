from util_classes import *
from global_variable_def import *
from util_functions import *
import time

start_time = time.time()
# PAPER NODES

#create_paper_nodes(  )
add_keywords()
print 'paper nodes created'

#VENUE NODES

#create_venue_nodes()
print 'venue nodes created'

#AUTHOR NODES

#create_author_nodes()
print 'author nodes created'

#FIELD NODES

#create_field_nodes()
print 'field nodes created'

#YEAR NODES

#create_year_nodes()
print 'year nodes created'

print 'Graph construction completed'
print 'Time taken : '+str( time.time() - start_time )
