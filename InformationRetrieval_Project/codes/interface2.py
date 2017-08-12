from flask import Flask, request, render_template
from metapath_ay import *
#from aco_apc_metapath import *
import time

app = Flask(__name__)
@app.route('/')
def load_first():
    return render_template('home.html')

@app.route('/result', methods=['GET', 'POST'])
def load_result():
     start_time = time.time()
     query = request.form['query'].encode('ascii')
     result = {}
     if len(query)==0:
         flag=True
     else:
         [author, year] = query.split('::')
         result = metapathay(author, year)
         flag=False

    
 
     return render_template('result2.html',flag = flag,count =0, result = result, time_taken = time.time() - start_time, num_match = len( result ) )

if __name__ == '__main__':
    app.run(host='0.0.0.0')
