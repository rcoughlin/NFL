#!/usr/bin/env python

import os
import redis
import json

from pymongo import MongoClient

REDIS_URL = os.environ.get('REDIS_URL') or '0.0.0.0:6379'
REDIS = redis.from_url(REDIS_URL)


# TODO configure this with environment variables on an env by env basis
client = MongoClient('localhost', 27017)
db = client['playbyplay']


# TODO only applicable for plays endpoint
def persist_play_data():
    play_table = db.plays
    player_table = db.players

    for key in REDIS.keys():
        data = json.loads(REDIS.get(key))

        for play in data:

            if len(play.split('|')) < 4:
                continue

            # TODO players association
            players = play['players']
            del play['players']

            if play_table.count(play) < 1:
                play_table.insert(play)


if __name__ == '__main__':
    persist_play_data()