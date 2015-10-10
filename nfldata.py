from flask import Flask
from flask import jsonify
from flask import request
from flask.ext.cors import CORS
import nflgame
import json
import requests

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        inputYear = request.args['inputYear'] or request.args.getList('inputYear')[0]
        inputWeek = request.args['inputWeek'] or request.args.getList('inputWeek')[0]

        games = nflgame.games(int(inputYear), week=int(inputWeek))
        players = nflgame.combine_game_stats(games)
        messages=[]

        for p in players.rushing().sort('rushing_yds').limit(10):
           msg = '%s %d carries for %d yards and %d TDs' %(p, p.rushing_att, p.rushing_yds, p.rushing_tds)
           messages.append(msg)
        print messages
        return json.dumps(messages)
    return False
if __name__ == '__main__':
    app.run(debug=True)
