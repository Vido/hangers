import json

import flask
import pingo

from hangers import Stand

app = flask.Flask('stand-ws')
stand = Stand()
board = pingo.detect.MyBoard()
stand._hang_hangers(board)

@app.route('/')
def index():
    return '<h1>stand-ws</h1>'

@app.route('/list_hangers/')
def list_hangers():
    response = json.dumps(stand.list(), indent=4)
    return flask.Response(response, mimetype='application/json')

@app.route('/refresh')
def refresh():
    stand.refresh()
    return

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
