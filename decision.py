import random
from termcolor import colored

import pkr_range
import database as db

def preflop_decision(game):
    '''
    Takes a preflop GameState.
    Returns hero's new range and his decision as a tuple: (range, decision_str).
    '''
    # Get data
    faced_action = game.facing_action(game.current_action) 
    facing = faced_action[0]
    pos_list = [game.players[game.hero_pos].position] + faced_action[1]  

    print()
    print("Preflop Decision:")
    print("Facing {facing} from {pos_list}.".format(facing=facing, pos_list=pos_list))

    # Get ranges
    ranges = [(pkr_range.PkrRange(path[0]), path[1]) for path in db.get_path(
                'preflop', facing, pos_list, None, True)]
    
    # No ranges found
    if not ranges or sum([r[0].combos for r in ranges]) == 0:
        return None
    
    # Make decision
    return make_decision(game, ranges)
    
def HU_flop_decision(game):
    '''
    Takes a flop GameState with a bet level of 2 or lower.
    Returns hero's new range and his decision as a tuple: (range, decision_str).
    '''
    faced_action = game.facing_action(game.current_action) 

    facing = faced_action[0]
    pos_list = [game.players[game.hero_pos].position] + faced_action[1]
    sizing = faced_action[2]
    adj_sizing = db.adjust_size(sizing) if sizing != 0.0 else sizing

    print()
    print("Flop Decision:")
    print("Facing {facing} from {pos_list}.".format(facing=facing, pos_list=pos_list))
    print("Sizing: {sizing} Adjusted: {adj}".format(
        sizing=sizing,
        adj=adj_sizing,
    ))

    ranges = [(pkr_range.PkrRange(path[0]), path[1]) for path in db.get_path(
                'flop', facing, pos_list, None, True, flop=game.board[:6], pot_type=game.pot_type,
                sizing=adj_sizing
    )]

    return make_decision(game, ranges)
    
def make_decision(game, ranges):
    '''
    Takes a list of poker ranges that correspond to the different decisions hero can make.
    Returns a decision and the corresponding range as a tuple: (range, decision_str).
    '''
    random.seed()
    decision = ('', None)
    frequencies = [r[0].get_frequency(game.hero_hand)*10000 for r in ranges]
    targets = []

    target_counter = 0

    for i in range(len(frequencies)):
        targets.append((target_counter, target_counter + frequencies[i]))
        target_counter += frequencies[i]
        print("Option {i}: {action} | {freq}% | {target}".format(
            i=i, action=ranges[i][1], freq=frequencies[i] / 10000, target=targets[i]
        ))
        
    choice = random.randrange(1, 1000001)
    print("Choice:", choice)

    for i in range(len(targets)):
        if targets[i][0] < choice <= targets[i][1]:
            decision = ranges[i]
                    
    if decision[0] == '':
        if game.highest_bet == 0:
            decision = (None, 'x')
        else:
            decision = (None, 'f')

    return decision

def hero_decision(game):
        '''
        Takes a GameState.
        Returns hero's new range and his decision as a tuple: (range, decision_str).
        '''
        street = game.get_street().lower()
        player_count = len(game.players)
        pot_type = int(game.pot_type[0]) if game.pot_type else None
        bet_level = game.bet_level

        if street == 'preflop':
            return preflop_decision(game)
        elif street == 'flop':
            if player_count == 2:
                if not pot_type or pot_type <= 2:
                    if bet_level <= 2:
                        return HU_flop_decision(game)
                    else:
                        print(colored("Cannot make decisions vs {bet_level}-bets on the flop. Skipping hand ...".format(
                        bet_level=bet_level
                    ), 'red'))
                else: 
                    #TODO
                    print(colored("Cannot make decisions in {pot_type}-bet pots on the flop. Skipping hand ...".format(
                        pot_type=pot_type
                    ), 'red'))
            else:
                #TODO
                print(colored("Cannot make decisions in {player_count}-way pot. Skipping hand ...".format(
                    player_count=player_count
                ), 'red'))
        else:
            #TODO
            print(colored("Cannot make decisions on the {street}. Skipping hand ...".format(
                street=street
            ), 'red'))

        return None
