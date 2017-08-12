from flask import Flask, request, render_template
from metapath_apc import *
from aco_apc_metapath import *
import time

app = Flask(__name__)
@app.route('/')
def load_first():
    return render_template('home.html')

@app.route('/result', methods=['GET', 'POST'])
def load_result():
     start_time = time.time()
     query = request.form['query'].encode('ascii')
     if queryis None:
         flag=1
     else:
         [author, venue] = query.split('::')
         result = metapathapc(author, venue)
         flag=0
    
 
    return render_template('result.html',flag = flag, result = result, time_taken = time.time() - start_time, num_match = len( result ) )

if __name__ == '__main__':
    app.run(host='0.0.0.0')
