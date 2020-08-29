import pyperclip

'''
Implements functionality concerning poker ranges.

Fully Documented.

Todos: 2
'''

from operator import itemgetter

class PkrRange:
    '''
    Represents a poker range, where each hand is assigned:
    hand_id:    unique id associated with hand (int)
    hand_str:   hand string (for example, Ac8s)
    frequency:  percent of the time the given hand takes the action associated with this range
    combos:     total combos of the hand in this range

    TODO:
    -could make code clearer by implementing Hand class to represent each hand
    '''
    def __init__(self, file_path=None):
        
        self.combos = 0
        self.matrix = []

        reg_suits = [   
            'hh',
            'hc',
            'hd',
            'hs',
            'ch',
            'cc',
            'cd',
            'cs',
            'dh',
            'dc',
            'dd',
            'ds',
            'sh',
            'sc',
            'sd',
            'ss'
            ]

        pp_suits = [ # s > d > c > h
            'ch',
            'dh',
            'dc',
            'sh',
            'sc',
            'sd'
            ]

        '''
        Create Hand Matrix:

        i = row in hand matrix, starting from the bottom (top right range half)
        j = column in hand matrix, starting from the right (top right range half)

        -> i = left card, j = right card
        -> i = high card, j = low card

        hand representation: [hand_id, hand_str, frequency, combos, EV]
        '''

        hand_number = 0

        for i in range(13):
            for j in range(i + 1):
                if j == i:
                    for suit in pp_suits:
                        self.matrix.append([hand_number, index_to_card(i) + suit[0] + index_to_card(j) + suit[1], 0, 0, 0])
                        hand_number += 1
                else:
                    for suit in reg_suits:
                        self.matrix.append([hand_number, index_to_card(i) + suit[0] + index_to_card(j) + suit[1], 0, 0, 0])
                        hand_number += 1
        
        if file_path != None:
            self.read_range_from_file(file_path)
                
                    
        
    def range_to_string(self):
        '''
        Returns string that can be pasted into GTO+'s range selection to represent current range.
        '''
        result = ''

        for ele in self.matrix:
            result += '[' + '{0:.1f}'.format(self.get_frequency(ele)) + ']' + self.get_hand(ele) + '[/' + '{0:.1f}'.format(self.get_frequency(ele)) + ']'
        
        return result

    def sort_ev(self, descending=False):
        '''
        Sorts current hand list by EV in ascending order.

        If descending=True, sorts in descending order.
        '''
        self.matrix.sort(key=itemgetter(4), reverse=descending)

    def sort_hands(self):
        '''
        Sorts current hand list by default hand order:
        Starting with 2c2h, 2d2h, ..., 3h2h, 3h2c, ...

        If descending=True, sorts in reverse order:
        Starting with AsAd, AsAc, ..., AsKs, AsKd, ...
        '''
        self.matrix.sort(key = itemgetter(0))

    def add_combos(self, amount):
        '''
        Increases the combo counter by the given amount.
        '''
        self.combos += amount

    def get_hand(self, identifier):
        '''
        Returns the hand string of the hand specified, where identifier is one of:
        int (hand id)
        list (hand element)
        '''
        if isinstance(identifier, int):
            return self.matrix[identifier][1]
        elif isinstance(identifier, list):
            return identifier[1]

    def get_frequency(self, identifier):
        '''
        Returns frequency of the hand specified, where identifier is one of:
        str (hand string)
        int (hand id)
        list (hand element)
        '''
        if isinstance(identifier, str):
            return self.matrix[hand_to_index(identifier)][2]
        elif isinstance(identifier, int):
            return self.matrix[identifier][2]
        elif isinstance(identifier, list):
            return identifier[2]

    def get_combos(self, identifier):
        '''
        Returns the amount of combos of the hand specified, where identifier is one of:
        str (hand string)
        int (hand id)
        list (hand element)
        '''
        if isinstance(identifier, str):
            return self.matrix[hand_to_index(identifier)][3]
        elif isinstance(identifier, int):
            return self.matrix[identifier][3]
        elif isinstance(identifier, list):
            return identifier[3]

    def get_ev(self, identifier):
        '''
        Returns the expected value (EV) of the hand specified, where identifier is one of:
        str (hand string)
        int (hand id)
        list (hand element)
        '''
        if isinstance(identifier, str):
            return self.matrix[hand_to_index(identifier)][4]
        elif isinstance(identifier, int):
            return self.matrix[identifier][4]
        elif isinstance(identifier, list):
            return identifier[4]

    def set_frequency(self, identifier, frequency):
        '''
        Sets frequency of the hand specified, where identifier is one of:
        str (hand string)
        int (hand id)
        list (hand element)
        '''
        if isinstance(identifier, str):
            self.matrix[hand_to_index(identifier)][2] = frequency
        elif isinstance(identifier, int):
            self.matrix[identifier][2] = frequency
        elif isinstance(identifier, list):
            identifier[2] = frequency

    def set_combos(self, identifier, combos):
        '''
        Sets the amount of combos of the hand specified, where identifier is one of:
        str (hand string)
        int (hand id)
        list (hand element)
        '''
        if isinstance(identifier, str):
            self.matrix[hand_to_index(identifier)][3] = combos
        elif isinstance(identifier, int):
            self.matrix[identifier][3] = combos
        elif isinstance(identifier, list):
            identifier[3] = combos

    def set_ev(self, identifier, ev):
        '''
        Sets the expected value (EV) of the hand specified, where identifier is one of:
        str (hand string)
        int (hand id)
        list (hand element)
        '''
        if isinstance(identifier, str):
            self.matrix[hand_to_index(identifier)][4] = ev
        elif isinstance(identifier, int):
            self.matrix[identifier][4] = ev
        elif isinstance(identifier, list):
            identifier[4] = ev

    def read_range_from_file(self, file_path):
        '''
        Takes the path to a *.txt file.
        Reads the poker range contained in the file into this poker range.
        File format: 
        "2c2h 55.326 0.384 28.3593      (hand_string, frequency, combos, EV)
         2d2h 25.326 0.254 15.3593
         ..." (same order as hands in self.matrix)
        ''' 
        range_file = open(file_path, 'r')
        for i in range(len(self.matrix)):
            line = range_file.readline().rstrip()
            elements = line.split()
            
            self.set_frequency(self.matrix[i], float(elements[1]))
            self.set_combos(self.matrix[i], float(elements[2]))
            self.set_ev(self.matrix[i], float(elements[3]))

    def print_range(self):
        '''
        Prints the current range to the console.

        TODO: Add cleaner output using box characters and proper spacing.
        '''
        for ele in self.matrix:
            print("{hand}: {freq}%, Combos: {combos}, EV: {EV}".format(
                hand=self.get_hand(ele),
                freq=self.get_frequency(ele),
                combos=self.get_combos(ele),
                EV=self.get_ev(ele)))

def hand_to_index(hand):
    '''
    Takes a hand string (for example, Ac7s).
    Returns the hand's ID (integer).
    '''
    def get_suit_offset(suits, pp):
        '''
        Takes a suit combination (str) and whether the hand is a pocket pair (boolean).
        Returns the offset of the given suit combination in the hand matrix.
        '''
        if pp:
            inp_suits = suits
            for _ in range(2):
                if inp_suits == 'ch':
                    return 0
                elif inp_suits == 'dh':
                    return 1
                elif inp_suits == 'dc':
                    return 2
                elif inp_suits == 'sh':
                    return 3
                elif inp_suits == 'sc':
                    return 4
                elif inp_suits == 'sd':
                    return 5
                else:
                    inp_suits = suits[1] + suits[0]
        else:
            if suits[0] == 'h':
                suit1 = 0
            elif suits[0] == 'c':
                suit1 = 4
            elif suits[0] == 'd':
                suit1 = 8
            elif suits[0] == 's':
                suit1 = 12
            
            if suits[1] == 'h':
                suit2 = 0
            elif suits[1] == 'c':
                suit2 = 1
            elif suits[1] == 'd':
                suit2 = 2
            elif suits[1] == 's':
                suit2 = 3
            
            return suit1 + suit2

    card1 = card_to_index(hand[0])
    card2 = card_to_index(hand[2])

    if card1 == card2:
        pp = True
    else:
        pp = False

    return (sum(range(card1)) * 16) + (card1 * 6) + (card2 * 16) + get_suit_offset(hand[1] + hand[3], pp)

def card_to_index(card):
    '''
    Takes a card rank (for example, Q for a queen).
    Returns a card rank's integer value:
    A -> 12, K -> 11, ..., 3 -> 1, 2 -> 0.
    '''
    if card == 'A':
        return 12
    elif card == 'K':
        return 11
    elif card == 'Q':
        return 10
    elif card == 'J':
        return 9
    elif card == 'T':
        return 8
    else:
        return int(card) - 2

def index_to_card(num):
    '''
    Takes a card rank's integer value (A -> 12, K -> 11, ..., 3 -> 1, 2 -> 0.).
    Returns the associated card rank (for example, Q for a queen).
    '''
    if num == 12:
        return 'A'
    elif num == 11:
        return 'K'
    elif num == 10:
        return 'Q'
    elif num == 9:
        return 'J'
    elif num == 8:
        return 'T'
    else:
        return str(2 + num)

def raw_data_to_range(raw_data, action, total_actions): # takes a GTO+ range in raw data format and returns it as a PkrRange
            
            #  action = which action to take; 1 = most aggressive (largest size), higher numbers less aggressive (lower size)
            #  total_actions = total possible actions in the solve (including check)

            result = PkrRange()
            line_data = raw_data.splitlines()
            elements = []

            for line in line_data:
                elements.append(line.split())
            
            for ele in elements:
                hand = hand_to_index(ele[0])
                result.add_combos(float(ele[2 + action]))
                result.set_combos(hand, float(ele[2 + action]))
                result.set_frequency(hand, float(ele[2 + total_actions + action]))
                result.set_ev(hand, float(ele[2 + (2 * total_actions) + action + 1]))

            return result

def parse_raw_data(raw_data, action, total_actions):
    poker_range = raw_data_to_range(raw_data, action, total_actions)
    parsed_data = ''
    
    for ele in poker_range.matrix:
        parsed_data += (poker_range.get_hand(ele) + ' ' +
                        str(poker_range.get_frequency(ele)) + ' ' +
                        str(poker_range.get_combos(ele)) + ' ' +
                        str(poker_range.get_ev(ele)) + '\n')

    return parsed_data

def parse_clipboard(action, total_actions):
    pyperclip.copy(parse_raw_data(pyperclip.paste(), action, total_actions))

parse_clipboard(2, 2)