# -*- coding:utf-8 -*-

import json
import sqlite3
import os
import subprocess

from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True

# Connect to the database (create a new one if it doesn't exist)
conn = sqlite3.connect('data.db')

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# # Create a table with the specified columns
cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
                no INTEGER PRIMARY KEY,
                email TEXT,
                name TEXT,
                status TEXT,
                timestamp DATETIME
                )''')

conn.commit()
conn.close()

class BaseDataTables:
    
    def __init__(self, request, columns, collection):
        self.columns = ['check', 'copy'] + columns # Add 'check' as the first column
        self.collection = collection
        
        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values
         
        # results from the db
        self.result_data = None
         
        # total in the table after filtering
        self.cardinality_filtered = 0
 
        # total in the table unfiltered
        self.cadinality = 0
 
        self.run_queries()
    
    def output_result(self):
        output = {}
        
        aaData_rows = []
        for row in self.result_data:
            aaData_row = []
            for i in range(len(self.columns)-2):
                aaData_row.append(str(row[self.columns[i+2]]).replace('"', '\\"'))
            aaData_rows.append(aaData_row)
            aaData_row.append('<a href="javascript:void(0)" onclick="copyToClipboard(this)">COPY</a>') # Add checkbox cell
            aaData_row.append('<input type="checkbox" name="id" value="' + str(row[self.columns[2]]) + '">') # Add checkbox cell
            
        output['aaData'] = aaData_rows
        
        return output
    
    def run_queries(self):
         self.result_data = self.collection
         self.cardinality_filtered = len(self.result_data)
         self.cardinality = len(self.result_data)


columns = ['No', 'EMAIL', 'NAME', 'STATUS', 'TIMESTAMP']

@app.route('/')
def index():
    return render_template('index.html', columns=columns)

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    num = eval(request.form['num'])
    print(name, num)
    for i in range(num):
        try:
            process = subprocess.Popen(['python', 'here.py', name], stdout=subprocess.PIPE)
            output, error = process.communicate()
        except:
            continue
    
    return 'Your request was successful.'

@app.route('/remove', methods=['POST'])
def remove():
    data = request.get_json()
    ids = data['ids']
    
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    for i in range(len(ids)):
        cur.execute('DELETE FROM accounts WHERE no=?', (ids[i],))
    conn.commit()
    conn.close()
    
    return 'Your request was successful.'

@app.route('/open', methods=['POST'])
def open():
    data = request.get_json()
    name = data['name']
    url = data['url']

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute('SELECT email from accounts WHERE name=? AND status="active"', (name, ))
    email = cur.fetchone()
    cur.execute('UPDATE accounts SET status=? WHERE email=?', ('sent', email[0], ))
    print(email[0])
    conn.commit()
    conn.close()

    process = subprocess.Popen(['python', 'google.py', email[0], url], stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    return 'Your request was successful.'

@app.route('/open-to-see', methods=['POST'])
def open_to_see():
    data = request.get_json()
    id_ = data['id']

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute('SELECT email from accounts WHERE no=?', (id_, ))
    email = cur.fetchone()
    conn.close()

    url = 'https://www.upwork.com/ab/proposals/'

    process = subprocess.Popen(['python', 'google.py', email[0], url], stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    return 'Your request was successful.'

@app.route('/change-status', methods=['POST'])
def change_status():
    data = request.get_json()
    status = data['status']
    ids = data['ids']
    # UPDATE your_table SET status='active' WHERE no='3';
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    for i in range(len(ids)):
        cur.execute('UPDATE accounts SET status=? WHERE no=?', (status, ids[i],))
    conn.commit()
    conn.close()
    
    return 'Your request was successful.'

@app.route('/screenshot', methods=['POST'])
def screenshot():
    image_files = [f for f in os.listdir('static') if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif')]
    for image in image_files:
        os.remove(os.path.join('static', image))
    process = subprocess.Popen(['python', 'screen.py'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    return 'Your request was successful.'

@app.route('/show-screenshots')
def show_screenshots():
    image_files = [f for f in os.listdir('static') if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif')]

    return render_template('screen.html', image_files=image_files)

@app.route('/_server_data')
def get_server_data():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM accounts')
    rows = cur.fetchall()
    conn.close()
    collection = [dict(zip(columns, row)) for row in rows]
    results = BaseDataTables(request, columns, collection).output_result()
    
    # return the results as a string for the datatable
    return json.dumps(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
