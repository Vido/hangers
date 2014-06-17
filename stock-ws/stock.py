import json
import sqlite3

from flask import Flask
app = Flask('Stock WebService')

@app.route('/')
def index():
    return '<h1>stock-ws<h2>'

@app.route('/check_stock/<code>')
def check_stock(code):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    template = "SELECT code, quantity FROM inventory WHERE code = {_code}"
    query = cur.execute(template.format(_code=code))
    results = query.fetchall()
    response = json.dumps({k: v for k, v in results})
    conn.close()
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
