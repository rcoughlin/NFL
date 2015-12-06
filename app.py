#!/usr/bin/env python

import os

import redis
import nflgame
import json
import requests

from flask import Flask, url_for
from flask import session
from flask import jsonify
from flask import request
from flask import redirect
from flask_oauth import OAuth
from flask.ext.cors import CORS


# Some application level configurations
OAUTH_ENABLED = os.getenv('OAUTH_ENABLED', False)
REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
REDIS = redis.from_url(REDIS_URL)

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)
cors = CORS(app)
twitter = OAuth().remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY', 0),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET', 0)
)


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


def login_required(method):
    def wrapper(*args, **kwargs):
        if OAUTH_ENABLED == True and session.get('authenticated', None) or \
            OAUTH_ENABLED == False:
            return method(*args, **kwargs)
        else:
            return redirect('login')

    wrapper.__name__ = method.__name__
    wrapper.__doc__ = method.__doc__
    return wrapper


@app.route('/login')
def login():
    try:
        return twitter.authorize(callback=url_for('oauth_authorized',
            next=request.args.get('next') or request.referrer or None))
    except Exception as e:
        raise e


@app.route('/logout')
@login_required
def logout():
    session['__invalidate__'] = True
    session['authenticated'] = False
    return redirect('plays')


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(response):
    next_url = request.args.get('next', 'plays')
    if response is None:
        return redirect('login')

    session['twitter_token'] = (
        response.get('oauth_token'),
        response.get('oauth_token_secret'),
    )
    session['authenticated'] = True
    session['twitter_user'] = response.get('screen_name')

    return redirect(next_url)


@app.route('/', methods=['GET'])
@login_required
def serve_index_asset():
    return send_static_file('index.html')


@app.route('/plays', methods=['GET'])
@login_required
def serve_play_by_play_asset():
    return send_static_file('html/plays.html')


@app.route('/neural', methods=['GET'])
@login_required
def serve_neural_network_asset():
    return send_static_file('html/neural.html')


@app.route('/<path:path>', methods=['GET'])
@login_required
def serve_static_assets(path):
    return send_static_file(path)


@app.route('/rushing_yds.json', methods=['GET'])
@login_required
def rushing_yards():
    name, year, week = parse_request_arguments(request.args)

    games = fetch_games(year, week)
    players = nflgame.combine_game_stats(games)

    plays = []

    key = 'rushing_yds|{}|{}'.format(year, week)
    data = REDIS.get(key)

    if not (data and len(data)):
        for player in players.rushing().sort('rushing_yds'):
            plays.append('{} {} carries for {} yards and {} TDs'.format(
                player, player.rushing_att, player.rushing_yds,
                player.rushing_tds))
        plays = set_data_on_redis_key(key, plays, True)
    else:
        plays = data

    return plays


@app.route('/plays_by_player.json', methods=['GET'])
@login_required
def plays_by_player():
    name, year, week = parse_request_arguments(request.args)

    '''
    Try to perform some arithmetic on our inputs, if they aren't ints, our API
    will throw errors
    '''
    try:
        year = year + 1 - 1
        week = week + 1 - 1
    except TypeError as e:
        return e

    plays = []
    if name and year and week:
        try:
            key = 'plays_by_player|{}|{}'.format(year, week)
            data = fetch_data_from_redis_by_key(key)
            if not data:
                data = fetch_plays(name, year, week)
                plays = set_data_on_redis_key(key, [
                    play.data for play in data
                ], True)
            else:
                plays = data
        except TypeError as e: pass

    return plays


@app.route('/plays_by_team.json', methods=['GET'])
@login_required
def plays_by_team():
    name, year, week = parse_request_arguments(request.args)
    team = None
    player = None

    # The NFL API only recognizes proper upper case names
    name = ' '.join(n.capitalize() for n in name.split(' '))

    players = fetch_player(name)
    if len(players) > 0:
        player = players[0]
        team = player.team

    '''
    Try to perform some arithmetic on our inputs, if they aren't ints, our API
    will throw errors
    '''
    try:
        year = year + 1 - 1
        week = week + 1 - 1
    except TypeError as e:
        return e

    plays = []
    if team and year and week:
        try:
            key = 'plays_by_team|{}|{}|{}'.format(player.name, year, week)
            data = fetch_data_from_redis_by_key(key)
            if not data:
                data = nflgame.combine_plays(fetch_games(year, week, team))
                plays = set_data_on_redis_key(key, [
                    play.data for play in data if team == play.team
                ], True)
            else:
                plays = data
        except TypeError as e: pass

    return plays


def fetch_games(year, week, team = None):
    games = nflgame.games(year, week)
    if team:
        for game in games:
            if game.home == team or game.away == team:
                return [ game ]
    return games


def fetch_player(name):
    return nflgame.find(name)


def fetch_plays(name, year, week):
    player = fetch_player(name)
    if len(player) > 0:
        return player[0].plays(year, week)
    else:
        return None


def fetch_data_from_redis_by_key(key, parse=False):
    data = REDIS.get(key)
    if data and len(data):
        if parse == True:
            return json.loads(data)
        else:
            return data
    else:
        return None


def set_data_on_redis_key(key, data, parse=False):
    redis_data = json.dumps(data)
    REDIS.set(key, redis_data)

    if parse == True:
        return redis_data
    else:
        return data


def parse_request_arguments(args):
    name, year, week = None, None, None

    if len(args.getlist('name')):
        name = args.getlist('name')[0]
    if len(args.getlist('year')):
        year = int(args.getlist('year')[0])
    if len(args.getlist('week')):
        week = int(args.getlist('week')[0])

    return name, year, week


def send_static_file(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)