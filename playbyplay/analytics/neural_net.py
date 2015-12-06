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
    player_plays = {}
    for play in plays:

        '''
        Who is really responsible for the play? attribute the yards to
        both players, weighting will work out
        TODO kickers and qbs
        '''
        for player in play['players']:
            db_player = player_table.find({'_id': player})
            if not player_plays.get(player, None):
                player_plays[player] = {
                    'yards': [],
                    'weighted_yards_avg': 0
                }

            player_plays[player]['yards'].append(play['ydsnet'])
            player_plays[player]['weighted_yards_avg'] = np.average(
                player_plays[player]['yards'])

    # Noice: players and their yearly plays, all set up
    # TODO not keying of players and plays yet
    print player_plays


# Sigmoid: http://mathworld.wolfram.com/SigmoidFunction.html
sigmoid = lambda x, d=False: x * (1 - x) if d else 1 / (1 + np.exp(-x))

if __name__ == '__main__':
    input_space(2015)