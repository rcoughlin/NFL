#!/usr/bin/env python

import numpy as np

from playbyplay.database.mongo import MONGO_CLIENT



# Pull all of our input players
def input_space(year):
    db = MONGO_CLIENT.playbyplay
    play_table = db.plays
    player_table = db.players

    # With our defined year we grab all of the plays in the year
    players = player_table.find({})
    plays = play_table.find({'year': str(year)})

    print plays.count(), players.count()

    '''
    Ok, we have all of the players in our input year, and all of the players
    We have no indication of whether we have viable players yet, does our
    player have plays in our input year
    '''
    for player in players:
        for play in plays:
            for uuid in play['players']:
                print uuid, player['_id']
            if player['_id'] in play['players']: pass


# Sigmoid: http://mathworld.wolfram.com/SigmoidFunction.html
sigmoid = lambda x, d=False: x * (1 - x) if d else 1 / (1 + np.exp(-x))

if __name__ == '__main__':
    input_space(2015)