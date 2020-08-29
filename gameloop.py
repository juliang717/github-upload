import interface
import gamestate
import player
import time
import random
import os
import util
from termcolor import colored

os.system('color')

delays = {
    # Delay before action
    'r_rand': (1000, 3000),
    'c_rand': (1000, 3000),
    'f_rand': (1000, 3000),
    'fast_f_short_rand': (500, 1500),
    'fast_f_long_rand': (2000, 5000),
    'fast_f_default': 500,
    'read_board': 200,

    # Delay after action
    'r_wait': 1000,
    'c_wait': 1000,
    'f_wait': 1000,
    'skipping': 1000,
}

random.seed()

def gameloop():
    tables = interface.get_table_list()
    windows = interface.get_window_list()
    interface.cc = interface.get_profile('bovada', tables, 'large')
    interface.positionSolver(windows)
    interface.positionTables(tables)

    games = [gamestate.GameState(tables[0][i], interface.get_stakes(tables[i][1]), i) for i in range(len(tables))]
    for i in range(1, len(games) + 1):
        print("Table {num}: {sb}/{bb}".format(num=i, sb=games[i - 1].stakes[0], bb=games[i - 1].stakes[1]))

    playing = True

    while(playing):
        for game in games:
            game.img = interface.get_table_img(game.index)
            game.img.save('img_debug/game{id}-{counter}.png'.format(id=game.index, counter=game.img_counter))
            game.inc_img_counter()
            if game.timeout == 0 or game.elapsed_time() >= game.timeout:
                game.timeout = 0

                if game.status == 'init':
                    if game.new_status:
                        print()
                        print("Waiting for New Hand ...")
                        game.new_status = False

                    if is_new_hand(game):
                        game.change_status('new_hand')

                if game.status == 'waiting':
                    if game.new_status:
                        game.waiting_counter = time.monotonic()
                        print()
                        print("Waiting for New Hand ...")
                        game.new_status = False
                    
                    if game.waiting_counter and time.monotonic() - game.waiting_counter >= 7:
                        #print("Unresponsive. Repeating fold ...")
                        interface.fold(game.ui_handle)
                        game.waiting_counter = time.monotonic()

                    if is_new_hand(game):
                        game.change_status('new_hand')

                elif game.status == 'new_hand':
                    if game.new_status:
                        print("Waiting for Cards ...")
                        game.new_status = False

                    if game.delayed_action == 'fast_f':
                        interface.fold(game.ui_handle)
                        game.delayed_action = None
                        game.set_timeout(delays['f_wait'])
                        game.change_status('waiting')
                    elif game.delayed_action == 'read_hand':
                        hand = interface.hero_hand(game.img, game.index)
                        if hand:
                            game.hero_hand = hand
                            game.delayed_action = None
                            game.change_status('playing')

                    elif interface.hero_has_cards(game.img):                        
                        active_seats = get_active_seats(game.img)
                        seat_nums = [i for i in range(0, len(active_seats)) if active_seats[i]]
                        button_pos = interface.button_pos(game.img)
                        game.players = [player.Player(None, None, seat=seat) for seat in seat_nums]
                        game.hero_pos = seat_to_pos(0, button_pos, active_seats)
                        
                        for p in game.players:
                            p.position = game.player_num_to_pos(seat_to_pos(p.seat, button_pos, active_seats))
                            #Assign default stacksize temporarily, to start new hand and compute fast_fold()
                            p.stacksize = 100
                        
                        sorted_players = game.players.copy()
                        sorted_players.sort(key = lambda player: pos_to_order_index(player.position, sum(active_seats)))
                        game.players = sorted_players.copy()

                        game.new_hand(game.players, game.hero_pos)

                        hand = interface.hero_hand(game.img, game.index)
                        if hand:
                            game.hero_hand = hand
                            fast_fold(game, delay=random.randrange(
                                delays['fast_f_short_rand'][0],delays['fast_f_short_rand'][1]))  
                        else:
                            game.delayed_action = 'read_hand'

                        if game.delayed_action == None:
                            game.change_status('playing')

                elif game.status == 'playing':
                    current_seat = game.players[game.current_action].seat
                    betsize = None

                    # First loop execution
                    if game.new_status:
                        game.new_status = False
                        street = game.get_street().lower()
                        if street == 'preflop':
                            print()
                            print("=" * 100)
                            print(" " * 46 + "NEW HAND" + " " * 46)
                            print("=" * 100)
                            for p in game.players:
                                p.stacksize = round(float(interface.player_stacksize(p.seat, game.index)) / game.stakes[1], 1)
                                print("Seat {seat} ({stack} bb){hero}: {pos}".format(
                                    seat = p.seat, 
                                    stack = p.stacksize, 
                                    hero="[Hero]" if game.player_pos_to_num(p.position) == game.hero_pos else "", 
                                    pos = p.position.upper()))            
                            print()
                    
                    # If hero has acted and street has changed, catch up on action.
                    elif (game.players[game.hero_pos].closed and 
                        game.get_street().lower() != interface.current_street(game.img) and
                        game.delayed_action == None):
                        while not game.action_closed():
                            #print()
                            #print("BEGINNING WHILE LOOP:")
                            #game.print_gamestate()
                            #print()
                            if not interface.has_cards(game.get_curr_player().seat, game.img):
                                game.fold()
                            elif game.highest_bet == 0:
                                game.check()
                            else:
                                game.call()

                            if game.action_closed():
                                game.change_status("reading_board")
                            #print()
                            #print("ENDING WHILE LOOP:")
                            #game.print_gamestate()
                            #print()

                    # If current seat is not active, update action.
                    elif (not interface.is_active(current_seat, game.img) and
                        game.delayed_action == None):
                        bet_status = interface.has_bet(current_seat, game.img)
                        if not interface.has_cards(current_seat, game.img):
                            game.fold()
                        elif game.highest_bet == game.get_curr_player().invested and not bet_status:
                            game.check()
                        elif bet_status:
                            cash_bet = interface.read_betsize(current_seat, game.index)
                            
                            if cash_bet != '':
                                betsize = round(float(cash_bet) / game.stakes[1], 1)
                                if betsize == game.highest_bet:
                                    game.call()
                                elif betsize > game.highest_bet:
                                    game.bet(betsize)
                                    fast_fold(game, delay=random.randrange(
                                        delays['fast_f_short_rand'][0],delays['fast_f_short_rand'][1])) 

                        #game.print_gamestate()
                        
                        if game.action_closed():
                            game.change_status("reading_board")

                    # If it is Hero's turn and Hero hasn't made a decision yet, get Hero's decision and queue it
                    elif current_seat == 0 and game.delayed_action == None and game.status == 'playing':
                        print("Hero acting.")
                        action = game.hero_decision()
                        if not action:
                            game.change_status('init')
                            game.set_timeout(delays['skipping'])
                        elif action == 'f':
                            game.set_delayed_action(action, random.randrange(delays['f_rand'][0], delays['f_rand'][1]))
                        elif action == 'c' or action == 'x' or action == '0.0':
                            game.set_delayed_action(action, random.randrange(delays['c_rand'][0], delays['c_rand'][1]))
                        elif action == 'r' or action == 'b' or action == 'a' or util.is_number(action):
                            game.set_delayed_action(action, random.randrange(delays['r_rand'][0], delays['r_rand'][1]))
                    
                    # If a decision is queued, execute it.
                    elif game.delayed_action:
                        if game.delayed_action == 'r' or game.delayed_action == 'b':
                            betsize = round(float(interface.read_bet_option(game.index)) / game.stakes[1], 1)
                            game.bet(betsize)
                            interface.bet(game.ui_handle)
                            game.delayed_action = None
                            game.set_timeout(delays['r_wait'])
                        elif game.delayed_action == 'a':
                            betsize = game.players[game.hero_pos].stacksize
                        elif game.delayed_action == 'c' or game.delayed_action == 'x' or game.delayed_action == '0.0':
                            if game.highest_bet == game.get_curr_player().invested:
                                game.check()
                            else:
                                game.call()
                            if game.action_closed():
                                game.change_status("reading_board")
                            interface.check_call(game.ui_handle)
                            game.delayed_action = None
                            game.set_timeout(delays['c_wait'])
                        elif util.is_number(game.delayed_action):
                            game.bet(float(game.delayed_action), percentage=True)
                            interface.bet(game.ui_handle, amount=float(game.delayed_action))
                            game.delayed_action = None
                            game.set_timeout(delays['r_wait'])
                        elif game.delayed_action == 'f':
                            game.fold()
                            interface.fold(game.ui_handle)
                            game.delayed_action = None
                            game.set_timeout(delays['f_wait'])
                            game.change_status('waiting')
                        elif game.delayed_action == 'fast_f':
                            interface.fold(game.ui_handle)
                            game.delayed_action = None
                            game.set_timeout(delays['f_wait'])
                            game.change_status('waiting') 
                        else:
                            print(colored("ERROR in gameloop. Unknown delayed action: {action}".format(
                                action=game.delayed_action
                            ), 'red'))

                    # Did a player win the hand?
                    if len(game.players) == 1: 
                        if game.players[0].seat == 0:
                            print("Hero wins.")
                        else:
                            print("Villain wins.")
                        game.change_status('waiting') 

                elif game.status == 'reading_board': 
                    if game.new_status:
                        game.new_status = False
                        print()
                        print("Reading Board ... ")
                    if game.delayed_action == 'read_board':
                        game.add_board_cards(interface.read_board(game.img, game.index, start_street='recent'))
                        game.change_status('playing')
                        game.delayed_action = None
                    elif interface.current_street(game.img).lower() != game.get_street().lower():
                        game.set_delayed_action('read_board', delays['read_board'])

def pos_to_order_index(pos_str, player_amount):
    if pos_str == 'sb':
        return 0
    elif pos_str == 'bb':
        return 1
    elif pos_str == 'lj' and player_amount >= 6:
        return player_amount - 4
    elif pos_str == 'hj' and player_amount >= 5:
        return player_amount - 3
    elif pos_str == 'co' and player_amount >= 4:
        return player_amount - 2
    elif pos_str == 'btn' and player_amount >= 3:
        return player_amount - 1
    else:
        print("ERROR in pos_to_order_index(). Invalid position string: {pos_str}, Player Amount: {player_amount}".format(
            pos_str=pos_str, player_amount=player_amount
        ))        

def is_new_hand(game):
    potsize = interface.read_potsize(game.index)

    if potsize != '' and float(potsize) == game.stakes[0] + game.stakes[1]:
        return True
    
    return False

def fast_fold(game, delay=None):
    if game.fast_fold():
        # Use default delay:
        fold_delay = delays['fast_f_default']
        # 20% Chance to override given delay with longer delay:
        if random.randrange(0, 10) <= 1:
            fold_delay = random.randrange(delays['fast_f_long_rand'][0], delays['fast_f_long_rand'][1])
        # Use given delay:
        elif delay:
            fold_delay = delay

        game.set_delayed_action('fast_f', fold_delay)
        print("Fast folding ... (Delay: {delay}s)".format(delay=round(fold_delay / 1000, 3)))
        print()

def get_active_seats(img):
    return [True if not interface.seat_open(i, img) else False for i in range(6)]

def pos_to_seat(pos, button_pos, active_seats):
    '''
    Takes a position integer (SB = 0, BB = 1, ...)
    Returns a seat integer (Bottom = -1, Bot-Left = 0, Top-Left = 1, Top = 2, ...)
    ''' 

    #UNTESTED

    if sum(active_seats) <= pos:
        print("ERROR: Position does not exist. Players:", sum(active_seats), "Position:", pos)
        return None

    seat = button_pos
    while pos >= 0:
        seat = seat + 1
        if seat >= 5:
            seat = seat - 6
        if active_seats[seat]:
            pos = pos - 1
    
    return seat

def seat_to_pos(seat, button_pos, active_seats):
    '''
    Takes a seat integer (Bottom = -1, Bot-Left = 0, Top-Left = 1, Top = 2, ...)
    Returns a position integer (SB = 0, BB = 1, ...)
    '''
    if not active_seats[seat]:
        print("ERROR: Seat is inactive. Seat:", seat)
        return None
    
    player_count = sum(active_seats)
    pos = player_count - 1
    while button_pos != seat:
        button_pos += 1
        if button_pos >= 6:
            button_pos = 0
        if active_seats[button_pos]:
            pos += 1
        if pos >= player_count:
            pos = 0

    return pos

gameloop()