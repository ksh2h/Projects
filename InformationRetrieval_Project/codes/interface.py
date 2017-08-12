from flask import Flask, request, render_template
from query_parser import *
from yearwiseCitation import *
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)
@app.route('/')
def load_first():
    return render_template('home.html')

@app.route('/result', methods=['GET', 'POST'])
def load_result():
     start_time = time.time()
     query = request.form['query'].encode('ascii')
     query = query + ' #'
     (result, flag, view, reco) = parser(query)
     #(flag, view) = ( False, "graph")
     #result = { "x" : [ "algos", "prog_lang", "ml" ], "y" : [3, 1, 4], "xalbel" : "Fields", "ylabel" : "No. of papers",    "title" : "Paper vs Field distribution for auhtor till year" }
     if view == 'list':
         return render_template('result.html', view = view, flag = flag, result = result, reco = reco, time_taken = time.time() - start_time, num_match = len( result ) )
     elif view == 'graph':
         return render_template('graph.html', view = view, flag = flag, result = result, time_taken = time.time() - start_time, num_match = 3 )

@app.route('/query')
def load_query_format():
    return render_template('query_form.html')

if __name__ == '__main__':
     app.run(host='0.0.0.0')
