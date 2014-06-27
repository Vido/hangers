import json

import flask
import pingo

from hangers import Stand

app = flask.Flask('stand-ws', template_folder="template")

stand = Stand()
board = pingo.detect.MyBoard()
stand._hang_hangers(board)

@app.route('/')
def index():
    response = flask.render_template('dashboard.html')
    return response

@app.route('/list_hangers/')
def list_hangers():
    response = json.dumps(stand.list(), indent=4)
    return flask.Response(response, mimetype='application/json')

@app.route('/refresh')
def refresh():
    stand.refresh()
    return flask.Response('', mimetype='application/json')

@app.route('/configure/')
def configure():
    code = int(flask.request.args.get('code'))
    location = int(flask.request.args.get('location'))
    hanger = stand.hangers[location]
    hanger.configure(code)
    return flask.Response('', mimetype='application/json')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
