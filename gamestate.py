import pyautogui, time, random
from termcolor import colored

import pkr_range, player, decision, util, client
import database as db

class GameState:

    def __init__(self, handle, stakes, index):
        self.index = index         #index of the table on the screen that corresponds to this gamestate
        self.ui_handle = handle         #window handle of the game represented by this game state
        self.img = None                 #pyautogui screenshot
        self.img_counter = 0            #Counts the amount of debug images saved to disk (only for debug purposes)
        self.stakes = stakes            #tuple of floats: (sb, bb)
        self.board = ''                 #string
        self.pot = None                 #float
        self.hero_pos = None            #int
        self.hero_hand = None           #string
        self.current_action = None      #int
        self.highest_bet = None         #float
        self.bet_level = None           #bet_level = 2 -> highest placed bet is a 2bet, 3 = 3bet, etc
        self.pot_type = None            #'1bp', '2bp', '3bp', '4bp'
        self.players = []               #list of Player instances
        self.action_sequence = []       #list of [<pos>, <action>, <amount>] pairs, where amount is
                                        #unaffected by alraedy invested amount; i.e 3betting to 100
                                        #after previously betting 20 is a raise to 100, not 80,
                                        #postflop raises/bets are stored as percentage of the pot, for example '66.7'
                                        #resets after each street, ignores folds
        self.translation = None         #dict
        self.status = 'init'    #Possible Values: 'waiting', 'new_hand', 'playing', 
                                        #'solving', 'delaying'
        self.new_status = True          #True if first loop of new status, else False
        self.timer_ref = None           #previous time.monotonic() value
        self.timeout = 0                #time to act again
        self.delayed_action = None      #string: action to take after timeout
        self.waiting_counter = None     #time.monotic() value when gamestate started waiting for a new hand.
        self.solved = False             #'solved' if a create solve command has been sent, 'queried' if current get range request has been sent, 
        self.solver_dec = False         #Holds Hero's upcoming decision as a tuple: (range, decision_str), or None if no decision has been made.
        self.wait_range = False         #True if waiting for response from solver
        self.request_queue = []         #Queue failed send requests to retry at later time
        self.street_changes = 0            #Number of street changes before current solve is invalid

    def inc_img_counter(self):
        self.img_counter += 1
        if self.img_counter >= 10:
            self.img_counter = 0

    def change_status(self, status):
        self.status = status
        self.new_status = True
        
    def set_timeout(self, millisec):
        self.timer_ref = time.monotonic()
        self.timeout = millisec / 1000

    def set_delayed_action(self, action, delay):
        self.delayed_action = action
        self.set_timeout(delay)

    def elapsed_time(self):
        return time.monotonic() - self.timer_ref

    def get_board(self):
        return self.board

    def get_pot(self):
        return self.pot

    def get_hero_pos(self):
        return self.hero_pos

    def get_player(self, i):
        return self.players[i]

    def get_street(self):
        count = len(self.board)

        if count == 0: 
            return 'Preflop'

        elif count == 6:
            return 'Flop'

        elif count == 8:
            return 'Turn'

        elif count == 10:
            return 'River'

        else:
            print('Invalid Board: Length = {0}', count)
            return None

    def get_OOP(self):
        if len(self.players) == 2:
            return self.players[0]
        elif len(self.players) < 2:
            raise NameError('There are less than 2 players in the hand.')
        elif len(self.players) > 2:
            raise NameError('There are more than 2 players in the hand.')

    def get_IP(self):
        if len(self.players) == 2:
            return self.players[1]
        elif len(self.players) < 2:
            raise NameError('There are less than 2 players in the hand.')
        elif len(self.players) > 2:
            raise NameError('There are more than 2 players in the hand.')

    def get_curr_player(self):
        return self.players[self.current_action]

    def is_hero_turn(self):
        '''
        Returns True if it is hero's turn, and False otherwise.
        '''
        return self.current_action == self.hero_pos

    def next_player(self):
        #print(colored("NEXT PLAYER", 'red'))
        if self.current_action == len(self.players) - 1:
            self.current_action = 0
        else: 
            self.current_action += 1
    
    def closed_count(self):
        return sum([p.closed for p in self.players])

    def action_closed(self):
        for p in self.players:
            if not p.closed:
                return False
        
        return True

    def print_gamestate(self):
        print(colored("============ GAME STATE ============", 'green'))
        print("Pot: {potsize} bb  {level}-bet Pot".format(potsize=self.pot, level=self.bet_level))
        print("Board:", self.board)
        print("Hand:", self.hero_hand)
        print("Highest Bet: {bet} bb".format(bet=self.highest_bet))
        print("Hero Pos:", self.hero_pos)
        print("Active Player:", self.current_action)
        print()
        for i in range(len(self.players)):
            print("{pos} (Seat {seat}, {stack} bb) {hero}: {invested} bb - {closed}".format(
                pos=self.players[i].position.upper(), 
                seat=self.players[i].seat, 
                stack=self.players[i].stacksize, 
                hero="[Hero]" if self.hero_pos == self.players[i].position else "", 
                invested=self.players[i].invested, 
                closed="Closed" if self.players[i].closed else ""))

    def new_hand(self, player_list, hero_pos):   
        
        #hero_pos = integer, sb = 0, bb = 1, btn = players_amount - 1, co = players_amount - 2, ...

        self.board = ''
        self.pot = 1.5
        self.hero_pos = hero_pos
        self.current_action = 2
        self.highest_bet = 1.0
        self.bet_level = 1
        self.pot_type = None
        self.players = player_list
        self.action_sequence = []
        self.translation = None

        self.players[0].put_money(0.5)
        self.players[1].put_money(1.0)
            
    def put_money(self, amount, player_num):
        self.pot += amount - self.get_player(player_num).get_invested()
        self.get_player(player_num).put_money(amount)

    def fold(self):
        print(colored("{position}({stack}){is_hero} folds".format(
            position=self.get_curr_player().get_position().upper(),
            stack=self.get_curr_player().stacksize,
            is_hero="[Hero]" if self.is_hero_turn() else '',
        ), 'yellow'))
        if self.current_action < self.hero_pos:
            self.hero_pos -= 1
        elif self.current_action == self.hero_pos:
            return True
        del self.players[self.current_action]
        self.current_action -= 1
        self.next_player()

    def call(self):
        if not self.is_hero_turn():
            facing = self.facing_action(self.current_action)
            if facing:
                self.assign_range(facing[0], facing[1], facing[2], 'c')
        print(colored("{position}({stack}){is_hero} calls {amount}".format(
            position=self.get_curr_player().get_position().upper(),
            stack=str(self.get_curr_player().stacksize - 
                (self.highest_bet - self.get_curr_player().invested)),
            is_hero="[Hero]" if self.is_hero_turn() else '',
            amount=self.highest_bet - self.get_curr_player().invested,
        ), 'blue'))
        self.put_money(self.highest_bet, self.current_action)
        self.action_sequence.append([self.get_player(self.current_action).get_position(), 'c', self.highest_bet])
        self.get_player(self.current_action).closed = True
        self.next_player()

    def check(self):
        if not self.is_hero_turn():
            facing = self.facing_action(self.current_action)
            if facing:
                self.assign_range(facing[0], facing[1], facing[2], 'x')
        print(colored("{position}({stack}){is_hero} checks".format(
            position=self.get_curr_player().get_position().upper(),
            stack=self.get_curr_player().stacksize,
            is_hero="[Hero]" if self.is_hero_turn() else '',
        ), 'blue'))
        self.action_sequence.append([self.get_player(self.current_action).get_position(), 'x', 0])
        self.get_player(self.current_action).closed = True
        self.next_player()

    def bet(self, amount, percentage=False):
        if not self.is_hero_turn():
            facing = self.facing_action(self.current_action)
            if facing:
                self.assign_range(facing[0], facing[1], facing[2], str(amount))
        self.bet_level += 1

        raw_amount = amount
        if percentage:
            raw_amount = self.highest_bet + (float(amount) / 100) * (self.highest_bet + self.pot)

        print(colored("{position}({stack}){is_hero} {bets} {amount}".format(
            position=self.get_curr_player().get_position().upper(),
            stack=self.get_curr_player().stacksize - (amount - self.get_curr_player().invested),
            is_hero="[Hero]" if self.is_hero_turn() else '',
            bets="bets" if self.bet_level == 1 else "raises to",
            amount=raw_amount
        ), 'green'))
    
        if self.get_street().lower() == 'preflop':
            self.action_sequence.append([self.get_player(self.current_action).get_position(), 'r', raw_amount])
        else:
            self.action_sequence.append([self.get_player(self.current_action).get_position(),
                'r', round((raw_amount - self.highest_bet) / (self.pot + self.highest_bet), 2) * 100])

        self.highest_bet = raw_amount

        self.put_money(raw_amount, self.current_action)

        for index in range(len(self.players)):
            self.players[index].closed = False

        self.get_player(self.current_action).closed = True
        self.next_player()

    def add_board_cards(self, card_string):
        if not self.translation:
            self.translation = db.translate_flop(card_string[:6])
            self.hero_hand = db.apply_translation(self.hero_hand, self.translation)
            self.board += self.translation['flop']
            if len(card_string) > 6:
                self.board += db.apply_translation(card_string[6:], self.translation)
        else:
            self.board += db.apply_translation(card_string, self.translation)

        if not self.pot_type:
            self.pot_type = str(self.bet_level) + 'bp'

        self.bet_level = 0
        self.highest_bet = 0
        self.current_action = 0
        self.action_sequence = []
        for player in self.players:
            player.invested = 0.0
            player.closed = False

        if self.street_changes:
            self.street_changes = self.street_changes - 1
        else:
            self.solved = False

        print(colored('_' * 70, 'magenta'))
        print(colored("Board: {board} \t Pot: {pot}".format(board=self.get_board(), pot=str(self.get_pot())), 'magenta'))
        print(colored("Hero Hand: {hand}".format(hand=self.hero_hand), 'magenta'))
        print()

    def player_num_to_pos(self, player_num, player_amount=None):
        '''
        Takes a player position integer: 0 = sb, 1 = bb, 2 = ... clockwise.
        Returns the player's position string (for example, 'lj', 'hj', ...)
        Only guaranteed to return a correct result if no players have folded yet.
        '''
        if player_amount == None:
            player_amount = len(self.players)

        positions = ['btn', 'co', 'hj', 'lj']

        if player_num == 0:
            return 'sb'
        elif player_num == 1:
            return 'bb'
        else:
            return positions[player_amount - player_num - 1]

    def player_pos_to_num(self, player_pos):
        for i in range(len(self.players)):
            if self.players[i].position.lower() == player_pos.lower():
                return i
        print("ERROR in player_pos_to_num(): Player in position {pos} is no longer in the hand.".format(
            pos=player_pos
        ))
        return None

    def count_limpers(self):
        '''
        Returns the amount of players that have currently voluntarily invested 1bb preflop.
        '''
        if self.get_street() == 'Preflop':
            return sum([True if (p.invested == 1.0) and (p.position != 'bb') else False 
                        for p in self.players])
        else:
            print("ERROR in count_limpers(): Street is not Preflop. Street:", self.get_street())

    def facing_action(self, player_pos):
        '''
        Returns tuple representing the action the current player is facing: (action, position, sizing)
        
        Preflop:
        The action(s) of villains are followed by (v) and the actions of
        Hero are followed by (h). For example, 
        'rfi(v)_3b(h)_4b(v)' = RFI (Villain) -> 3bet (Hero) -> 4bet (Villain)

        Below, Hero refers to the player specified by the position index player_pos.
        '''
        #print()
        #print("Action Sequence:")
        #for action in self.action_sequence:
        #    print("{pos}: {action} {amount}".format(pos=action[0], action=action[1], amount=action[2]))

        def player_is_actor(action_element):
            return True if self.player_pos_to_num(action_element[0]) == player_pos else False

        raise_count = 2
        limp_count = 0
        prev_raise_size = 0.0
        f_action = ''
        pos_list = []
        sizing = None

        if self.get_street() == 'Preflop':

            #Facing Folds if there are no actions yet
            if len(self.action_sequence) == 0:
                f_action = 'f_'

            for i in range(len(self.action_sequence)):
                hero_action = player_is_actor(self.action_sequence[i])
                curr_action = ''

                #Facing folds if Hero is first action
                if i == 0 and hero_action:
                    f_action += 'f_'

                #Add Preflop Raise
                if self.action_sequence[i][1] == 'r':
                    if raise_count == 2:
                        curr_action += 'rfi'
                        
                        if limp_count == 0 and 3.5 < self.action_sequence[i][2] <= 5.0:
                            curr_action += '+'
                        elif limp_count == 0 and 5.0 < self.action_sequence[i][2]:
                            curr_action += '++'
                    else:
                        curr_action += str(raise_count) + 'b'
                        if self.action_sequence[i][2] > 6 * prev_raise_size:
                            curr_action += '+'
                    
                    prev_raise_size = self.action_sequence[i][2]
                    raise_count += 1

                #Add Preflop Limp or Flat
                elif self.action_sequence[i][1] == 'c' or self.action_sequence[i][1] == 'x':
                    #If action is an open limp:
                    if raise_count == 2 and (limp_count == 0 or hero_action):
                        curr_action += 'c'
                        limp_count += 1
                    #Only add flats to action string if hero made them:
                    elif hero_action:
                        curr_action += 'c'

                #Append Hero/Villain tag and Villain position
                if curr_action != '':
                    f_action += curr_action
                    if hero_action:
                        f_action += '(h)_'
                    else:
                        f_action += '(v)_'
                        pos_list.append(self.action_sequence[i][0])
            
            #Remove trailing underscore
            if len(f_action) >= 1 and f_action[-1] == '_':
                f_action = f_action[:-1]
        
        #Postflop:
        else:
            if len(self.players) == 2:
                #Append Villain position:
                pos_list.append(self.players[0].position if player_pos == 1 else self.players[1].position)

                if self.bet_level == 0:
                    f_action = 'fx'
                    sizing = 0.0
                else:
                    if self.bet_level == 1:
                        f_action = 'fb'
                    elif self.bet_level == 2:
                        f_action = 'fr'

                    for i in range(1, len(self.action_sequence) + 1):
                        if self.action_sequence[-i][1] == 'r':
                            sizing = self.action_sequence[-i][2]
                            break
        
        if f_action == '':
            return None

        return (f_action, pos_list, sizing)

    def assign_range(self, facing, pos_list, faced_sizing, action):
        '''
        Takes action string (for example:'x', 'c', or '9.5')
        Assigns a poker range to the currently acting villain based on his action.
        '''
        path = ''
        pos_list = [self.get_curr_player().position] + pos_list

        if self.get_street() == 'Preflop':
            if util.is_number(action):
                action = 'r'
            elif action == 'x':
                action = 'c'
            path = db.get_path('preflop', facing, pos_list, action, False)
        elif self.get_street() == 'Flop':
            if ((self.bet_level == 2 and util.is_number(action)) or
                self.bet_level > 2 or
                len(self.players) > 2 or
                self.pot_type != '2bp'):
                pass
            else:
                if action == 'c' or action == 'x':
                    action = '0.0'
                path = db.get_path('flop', facing, pos_list, action, False, flop=self.board, pot_type=self.pot_type, sizing=faced_sizing)
        elif self.get_street() == 'Turn':
            if len(self.players == 2):
                if self.solved:
                    client.get_ranges(
                        0,
                        self.get_curr_player() == self.players[0],
                        facing,
                        action,
                        self.get_curr_player().position
                    )
                    self.wait_range = True
        elif self.get_street() == 'River':
            #TODO Assign river ranges
            pass
            
        if not path:
            print("No range path given. Could not assign range to {n}.".format(n=self.get_curr_player().seat))
            self.get_curr_player().set_range(None)
        else:
            self.get_curr_player().hand_range = pkr_range.PkrRange(path)
            print("{pos} range: {combos}".format(
                pos=self.get_curr_player().position.upper(),
                combos=self.get_curr_player().hand_range.combos
            ))
        '''
        else:
            print("ERROR in assign_range(): Street: {street} Facing: {facing} Action: {action}".format(
                street=self.get_street(), facing=facing, action=action))
        '''

    def hero_decision(self):
        choice = decision.hero_decision(self)

        if not choice:
            return None

        self.players[self.hero_pos].set_range(choice[0])

        print("Decision:", choice[1])
        print()

        return choice[1]

    def fast_fold(self):
        '''
        Returns True if Hero always folds against the action so far. Otherwise, returns False.
        '''
        if not self.get_street().lower() == 'preflop':
            return False

        faced_action = self.facing_action(self.hero_pos)
        facing = faced_action[0]

        pos_list = [self.players[self.hero_pos].position] + faced_action[1]

        print()
        print("Fast Fold Decision:")
        print("Facing {facing} from {pos_list}.".format(facing=facing, pos_list=pos_list))
        print("Hero Hand:", self.hero_hand)

        ranges = [pkr_range.PkrRange(path[0]) for path in db.get_path(
                self.get_street(), facing, pos_list, None, True)]

        if (self.players[self.hero_pos].position == 'bb' and
            facing == 'f'):
            ranges.extend([pkr_range.PkrRange(path[0]) for path in db.get_path(
                'preflop', 'rfi(v)', [pos_list[0], 'sb'], None, True)])

        frequencies = [r.get_frequency(self.hero_hand)*10000 for r in ranges]
        
        freq_sum = sum(frequencies) 
        print("Frequency Sum: {freq}%".format(freq=freq_sum / 10000))
        print()

        return True if freq_sum == 0.0 else False

    def process_response(self, resp):
        if resp[1] == 'hero':
            self.solver_dec = decision.make_decision(self, resp[0])
        else:
            self.players[self.player_pos_to_num(resp[1].lower())].hand_range = resp[0]
            self.wait_vill_range = False

