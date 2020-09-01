'''
Implements functionality relating to the solver and the database.
'''

import pyautogui, pyperclip, time
from termcolor import colored

import pkr_range, util, imagesearch
from interface import get_window_list

base_dir = r'C:\Users\julia\Desktop\Bot\database'
legacy_dir = r'C:\Users\julia\Desktop\Bot\legacy_boards.txt'

locs = {
    'run_solver_btn': (79, 474), ###
    'process_db_area': (265, 469, 461, 605), ###
    'select_flop_base': (765, 203), ###
    'select_flop_offset': 18, ###
    'node1_btn': (44, 97), ###
    'raw_data_area': (545, 247, 659, 735), ###
    'raw_data_offset': (-14, 14), # ???
    'data_check': (605, 853, 3, 3), ###
    'data_pix': (240, 240, 240), # ???
    'data_popup': (361, 359), ###
    'menu_check': (108, 488, 3, 3), ###
    'menu_pix': (242, 242, 242), ###
    'select_all_offset': (-178, 149), ###
    'vert_offset': 32, ###
    'area2': (342, 77, 410, 125), ###
    'area3': (502, 77, 577, 125), ###
    'area4': (664, 77, 743, 125), ###
    'node_offset': 165, ###
}

# Villain is Hero:
preflop_paths_vil = {   # pos0 = player, pos1 = first villain, pos2 = second villain, ...
    # Hero didn't act yet:
    'f': {
        'r': base_dir + r'\pre\pos0\uni\rfi.txt',
        'c': '' #base_dir + r'\pre\pos\uni\limp.txt',
    },
    'c(v)': {
        'r': base_dir + r'\pre\pos0\uni\iso.txt',
        'c': '', #base_dir + r'\pre\pos0\uni\limp_along',
    },
    'rfi(v)': {
        'r': base_dir + r'\pre\pos0\pos1\3bet_v.txt',
        'c': base_dir + r'\pre\pos0\pos1\flat_v.txt',
    },
    'rfi+(v)': {
        'r': base_dir + r'\pre\pos0\pos1\3bet_v.txt',                   # Same as regular RFI currently (need update)
        'c': base_dir + r'\pre\pos0\pos1\flat_v.txt',                   # Same as regular RFI currently (need update)
    },
    'rfi++(v)': {
        'r': base_dir + r'\pre\pos0\pos1\3bet_v.txt',                   # Same as regular RFI currently (need update)
        'c': base_dir + r'\pre\pos0\pos1\flat_v.txt',                   # Same as regular RFI currently (need update)
    },
    'c(v)_rfi(v)': {
        'r': base_dir + r'\pre\pos0\pos2\3bet_iso_v.txt',
        'c': base_dir + r'\pre\pos0\pos2\flat_iso_v.txt',
    },
    'rfi(v)_3b(v)': {
        'r': base_dir + r'\pre\pos0\pos1\cold_4bet_v.txt',              # Range depends on RFI position (pos1)
        'c': base_dir + r'\pre\pos0\pos1\cc_3bet_v.txt',                # Range depends on RFI position (pos1)
    },
    'rfi(v)_3b(v)_4b(v)': {
        'r': base_dir + r'\pre\pos0\uni\cold_5bet_v.txt',
        'c': base_dir + r'\pre\pos0\uni\cc_4bet_v.txt',
    },
    'rfi(v)_3b(v)_4b(v)_5b(v)': {
        'r': base_dir + r'\pre\pos0\uni\cold_6bet_v.txt',
        'c': base_dir + r'\pre\pos0\uni\cc_5bet_v.txt',
    },

    # Hero RFI'd:
    'f_rfi(h)_3b(v)': {
        'r': base_dir + r'\pre\pos0\pos1\4bet_v.txt',
        'c': base_dir + r'\pre\pos0\pos1\flat_3bet_v.txt',
    },

    # Hero isolated a limp:
    'c(v)_rfi(h)_3b(v)': {
        'r': base_dir + r'\pre\generic\KK+.txt',
        'c': base_dir + r'\pre\generic\QQ_AK.txt',
    },

    # Hero Flatted an RFI:
    'rfi(v)_c(h)_3b(v)': {
        'r': base_dir + r'\pre\pos0\uni\4bet_after_flat_v.txt',
        'c': base_dir + r'\pre\pos0\pos1\flat_3bet_after_flat_rfi_v.txt',
    },

    # Hero 3bet an RFI:
    'rfi(v)_3b(h)_4b(v)': {
        'r': base_dir + r'\pre\pos0\pos1\pos2\5bet_after_3bet_v.txt',
        'c': base_dir + r'\pre\pos0\pos1\pos2\flat_after_3bet_v.txt',
    },

    # Hero cold 4bet a 3bet:
    'rfi(v)_3b(v)_4b(h)_5b(v)': {
        'r': base_dir + r'\pre\pos1\6bet_after_cold_4bet_v.txt',
        'c': base_dir + r'\pre\pos1\flat_after_cold_4bet_v.txt',
    },

    # Obscure action including one of the following strings, minus ellipsis:
    'rfi+...': {
        'r': base_dir + r'\pre\generic\KK+.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    },
    'rfi++...': {
        'r': base_dir + r'\pre\generic\KK+.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    },
    'b+...': {
        'r': base_dir + r'\pre\generic\KK+.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    }
}
# Hero is Hero:
preflop_paths_hero = {   # pos0 = hero, pos1 = first villain, pos2 = second villain, ...
    # Hero didn't act yet:
    'f': {
        'r': base_dir + r'\pre\pos0\uni\rfi.txt',
        'c': base_dir + r'\pre\pos0\uni\limp_h.txt',
    },
    'c(v)': {
        'r': base_dir + r'\pre\pos0\uni\iso.txt',
        'c': base_dir + r'\pre\pos0\uni\limp_along_h.txt',
    },
    'rfi(v)': {
        'r': base_dir + r'\pre\pos0\pos1\3bet_h.txt',
        'c': base_dir + r'\pre\pos0\pos1\flat_h.txt',
    },
    'rfi+(v)': {
        'r': base_dir + r'\pre\pos0\pos1\3bet_h.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    },
    'rfi++(v)': {
        'r': base_dir + r'\pre\generic\QQ+_AK.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    },
    'c(v)_rfi(v)': {
        'r': base_dir + r'\pre\pos0\pos2\3bet_iso_h.txt',
        'c': base_dir + r'\pre\pos0\pos2\flat_iso_h.txt',
    },
    'rfi(v)_3b(v)': {
        'r': base_dir + r'\pre\pos0\pos1\cold_4bet_h.txt',              # Range depends on RFI position (pos1)
        'c': base_dir + r'\pre\pos0\pos1\cc_3bet_h.txt',                # Range depends on RFI position (pos1)
    },
    'rfi(v)_3b(v)_4b(v)': {
        'r': base_dir + r'\pre\pos0\uni\cold_5bet_h.txt',
        'c': base_dir + r'\pre\pos0\uni\cc_4bet_h.txt',
    },
    'rfi(v)_3b(v)_4b(v)_5b(v)': {
        'r': base_dir + r'\pre\pos0\uni\cold_6bet_h.txt',
        'c': base_dir + r'\pre\pos0\uni\cc_5bet_h.txt',
    },

    # Hero RFI'd:
    'f_rfi(h)_3b(v)': {
        'r': base_dir + r'\pre\pos0\pos1\4bet_h.txt',
        'c': base_dir + r'\pre\pos0\pos1\flat_3bet_h.txt',
    },

    # Hero Flatted an RFI:
    'rfi(v)_c(h)_3b(v)': {
        'r': base_dir + r'\pre\generic\empty_range.txt',
        'c': base_dir + r'\pre\pos0\uni\flat_3bet_after_flat_rfi_h.txt',
    },

    # Hero 3bet an RFI:
    'rfi(v)_3b(h)_4b(v)': {
        'r': base_dir + r'\pre\pos0\pos1\pos2\5bet_after_3bet_h.txt',
        'c': base_dir + r'\pre\pos0\pos1\pos2\flat_after_3bet_h.txt',
    },

    # Hero cold 4bet a 3bet:
    'rfi(v)_3b(v)_4b(h)_5b(v)': {
        'r': base_dir + r'\pre\generic\KK+.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    },

    # Obscure action including one of the following strings, minus ellipsis:
    'rfi+...': {
        'a': base_dir + r'\pre\generic\KK+.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    },
    'rfi++...': {
        'a': base_dir + r'\pre\generic\KK+.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    },
    'b+...': {
        'a': base_dir + r'\pre\generic\KK+.txt',
        'c': base_dir + r'\pre\generic\empty_range.txt',
    }
}
#Postflop database path template:
flop_path = base_dir + r'\pot_type\pos0\pos1\facing\sizing\action\flop'
#Hero's options when facing the given action:
hero_options = {
    'fx': ['66.7', '33.3'],
    'fb': ['75.0', '0.0'],
    'fr': ['75.0', '0.0'],
}
#Possible bet/raise sizes for flop solutions:
bet_sizes = [83.3, 66.7, 50.0, 33.3, 16.7]
raise_sizes = [75.0]

def get_path(street, facing, pos_list, action, hero, flop=None, pot_type=None, sizing=None):
    '''
    Takes current street, the action faced (for example, 'f_rfi_3bet'),
    the corresponding position list as returned by gamestate.facing_action(),
    the action in response to the action faced (for example, 'r' for raise),
    and whether the player is hero (True/False).

    Returns the filepath to the range that corresponds to the given input.

    If action = None, returns a list of tuples (range, action) corresponding to all possible actions,
    given the action faced, ordered from most aggressive to least aggressive action,
    excluding fold.

    To get paths to flop solutions, specify the flop and the pot type (for example, '2bp') as optional parameters.
    '''

    def print_parameters():
        print("Street:", street)
        print("Facing:", facing)
        print("Position List:", pos_list)
        print("Action:", action)
        print("Hero:", hero)
        print("Flop:", flop)
        print("Pot Type:", pot_type)
        print("Sizing:", sizing)

    def get_preflop_paths(facing):
        path_dict = None

        preflop_paths = None
        
        if hero:
            path_dict = preflop_paths_hero
        else:
            path_dict = preflop_paths_vil

        if not facing in path_dict:
            if 'rfi+(' in facing:
                facing = 'rfi+...'
            elif 'rfi++(' in facing:
                facing = 'rfi++...'
            elif 'b+(' in facing:
                facing = 'b+...'

        # No ranges corresponding to situation found:
        elif not (facing in path_dict and (action in path_dict[facing] or action == None)):
            print(colored("ERROR in get_path(): Key Error in assigned path dictionary:", 'red'))
            print_parameters()
            return None

        if action != None and action in path_dict[facing]:
            preflop_paths = path_dict[facing][action]
        elif action == None:
            preflop_paths = [(path_dict[facing][key], key) for key in ['r', 'b', 'c', 'x'] if key in path_dict[facing]]
        else:
            print(colored("ERROR in get_path(): Given action is not part of path dictionary:", 'red'))
            print_parameters()
            return None

        return preflop_paths

    def get_flop_paths():
        if facing == 'fr':
            nonlocal sizing
            sizing += '-' + str(raise_sizes[0])
        if action != None:
            return flop_path.replace('action', action)
        elif not facing in hero_options:
            print(colored("ERROR in get_path(): Given facing action is invalid.", 'red'))
            print_parameters()
            return None
        elif action == None and hero:
            return [(flop_path.replace('action', option), option) for option in hero_options[facing]]
        else:
            print(colored("ERROR in get_path(): Player is not Hero and there is no action given.", 'red'))
            print_parameters()
            return None

    def parse_path(paths):
        for i in range(len(pos_list)):
            paths = paths.replace('pos' + str(i), pos_list[i])
        if flop:
            paths = paths.replace('flop', flop)
            paths = paths.replace('facing', facing)
            paths += '.txt'
        if pot_type:
            paths = paths.replace('pot_type', pot_type)
        if sizing:
            paths = paths.replace('sizing', sizing)
        
        return paths

    paths = ''
    sizing = str(sizing)

    if street.lower() == 'preflop':
        paths = get_preflop_paths(facing)

    elif street.lower() == 'flop':
        paths = get_flop_paths()
    
    if isinstance(paths, list):
        return [(parse_path(path[0]), path[1]) for path in paths]
    else:
        return parse_path(paths)

def adjust_size(size, raising=False):
    if raising:
        size_list = raise_sizes
    else:
        size_list = bet_sizes

    differences = [abs(curr_size - size) for curr_size in size_list]

    return size_list[differences.index(min(differences))]

def add_solve(pot_type, hero_pos, villain_pos, sizes, raise_sizes, solver_pos, start=0, legacy_mode=False, no_scroll=False):

    # make sure flop list is scrolled all the way up before calling add_solve

    # if not starting at 0, there is a chance that the program lags during the scrolling process and selects a flop that is earlier in the list, overwriting flops with the wrong ranges -> make sure the correct flop is selected when it starts gathering data

    # start = flop entry to start on, 0 = first entry
    # sizes = list of all betsizes in the solution in one digit precision float format, descending order, including check = 0.0
    # raise_sizes = list of all betsizes in the solution in one digit precision float format, descending order, including call = 0.0
    # hero_pos = OOP
    # villain_pos = IP
    # facing flop 3bet, only flat or fold, fold same freq as solver

    # sub-routines:

    def add_solution(pot_type, hero_pos, villain_pos, sizes, raise_sizes, board):   # adds the currently selected solution

        # sub-routines:

        def range_to_file(hand_range, pot_type, hero_pos, villain_pos, face_action, face_size, response_size, board): 
            savefile = open(base_dir + '\\' + pot_type + '\\' + hero_pos + '\\' + villain_pos + '\\' + face_action + '\\' + face_size + '\\' + response_size + '\\' + board + '.txt', 'w')
            for element in hand_range.matrix:
                savefile.write(hand_range.get_hand(element) + ' ' + str(hand_range.get_frequency(element)) + ' ' + str(hand_range.get_combos(element)) + ' ' + str(hand_range.get_ev(element)) + '\n')

            savefile.close()

        # (could be cleaner as recursive function)

        # TODO: group consecutive repeating statements into functions for readability (for example, while loops and range_to_file)
        # TODO: group (get_raw_data -> raw_data_to_range -> range_to file) into a single function save_raw_data()

        for i in range(len(sizes)): # get oop first-action ranges
            pyautogui.click(
                locs['node1_btn'][0] + solver_pos[0],
                locs['node1_btn'][1] + solver_pos[1])
            while imagesearch.imagesearcharea('img/icon1.png',
                locs['area2'][0] + solver_pos[0],
                locs['area2'][1] + solver_pos[1],
                locs['area2'][2] + solver_pos[0],
                locs['area2'][3] + solver_pos[1])[0] != -1:
                pyautogui.click(
                    locs['node1_btn'][0] + solver_pos[0],
                    locs['node1_btn'][1] + solver_pos[1])
                time.sleep(0.1)
            range_to_file(raw_data_to_range(get_raw_data(locs['node1_btn'][0], locs['node1_btn'][1], solver_pos), i + 1, len(sizes)), pot_type, hero_pos, villain_pos, 'fx', '0.0' , str(sizes[i]), board)
            pyautogui.click(
                locs['node1_btn'][0] + locs['node_offset'] + solver_pos[0],
                locs['node1_btn'][1] + (i * locs['vert_offset']) + solver_pos[1])
            if i == (len(sizes) - 1):
                for j in range(len(sizes)): # get ip facing-check ranges
                    while (imagesearch.imagesearcharea('img/icon2.png', 
                        locs['area3'][0] + solver_pos[0],
                        locs['area3'][1] + solver_pos[1],
                        locs['area3'][2] + solver_pos[0],
                        locs['area3'][3] + solver_pos[1])[0] != -1):
                        pyautogui.click(
                            locs['node1_btn'][0] + locs['node_offset'] + solver_pos[0],
                            locs['node1_btn'][1] + solver_pos[1])
                    while (imagesearch.imagesearcharea('img/icon1.png',
                        locs['area2'][0] + solver_pos[0],
                        locs['area2'][1] + solver_pos[1],
                        locs['area2'][2] + solver_pos[0],
                        locs['area2'][3] + solver_pos[1])[0] == -1):
                        time.sleep(0.1)
                    range_to_file(raw_data_to_range(get_raw_data(locs['node1_btn'][0] + locs['node_offset'], locs['node1_btn'][1], solver_pos), j + 1, len(sizes)), pot_type, villain_pos, hero_pos, 'fx', '0.0' , str(sizes[j]), board)
                    if j != (len(sizes) - 1):
                        pyautogui.click(
                            locs['node1_btn'][0] + locs['node_offset'] * 2,
                            locs['node1_btn'][1] + (j * locs['vert_offset']))
                        for k in range(len(raise_sizes)):   # get oop facing-bet ranges
                            while (imagesearch.imagesearcharea('img/icon1.png',
                                locs['area4'][0] + solver_pos[0],
                                locs['area4'][1] + solver_pos[1],
                                locs['area4'][2] + solver_pos[0],
                                locs['area4'][3] + solver_pos[1])[0] != -1):
                                pyautogui.click(
                                    locs['node1_btn'][0] + locs['node_offset'] * 2 + solver_pos[0],
                                    locs['node1_btn'][1] + solver_pos[1])
                            while (imagesearch.imagesearcharea('img/icon2.png',
                                locs['area3'][0] + solver_pos[0],
                                locs['area3'][1] + solver_pos[1],
                                locs['area3'][2] + solver_pos[0],
                                locs['area3'][3] + solver_pos[1])[0] == -1):
                                time.sleep(0.1)
                            range_to_file(raw_data_to_range(get_raw_data(locs['node1_btn'][0] + locs['node_offset'] * 2, locs['node1_btn'][1], solver_pos), k + 1, len(raise_sizes) + 1), pot_type, hero_pos, villain_pos, 'fb', str(sizes[j]), str(raise_sizes[k]), board)
                            if k != (len(raise_sizes) - 1):
                                pyautogui.click(
                                    locs['node1_btn'][0] + locs['node_offset'] * 3 + solver_pos[0],
                                    locs['node1_btn'][1] + (k * locs['vert_offset']) + solver_pos[1])
                                for n in range(len(raise_sizes)):   # get ip facing-raise ranges
                                    '''
                                    pyautogui.click(
                                        locs['node1_btn'][0] + locs['node_offset'] * 3 + solver_pos[0],
                                        locs['node1_btn'][1] + solver_pos[1])
                                    '''
                                    while imagesearch.imagesearcharea('img/icon1.png',
                                        locs['area4'][0] + solver_pos[0],
                                        locs['area4'][1] + solver_pos[1],
                                        locs['area4'][2] + solver_pos[0],
                                        locs['area4'][3] + solver_pos[1])[0] == -1:
                                        time.sleep(0.1)
                                    range_to_file(raw_data_to_range(get_raw_data(locs['node1_btn'][0] + locs['node_offset'] * 3, locs['node1_btn'][1], solver_pos), n + 1, len(raise_sizes) + 1), pot_type, villain_pos, hero_pos, 'fr', str(sizes[j]) + '-' + str(raise_sizes[k]), str(raise_sizes[n]), board)
            else:
                for j in range(len(raise_sizes)): # get ip facing-bet ranges
                    while (imagesearch.imagesearcharea('img/icon2.png',
                        locs['area3'][0] + solver_pos[0],
                        locs['area3'][1] + solver_pos[1],
                        locs['area3'][2] + solver_pos[0],
                        locs['area3'][3] + solver_pos[1])[0] != -1):
                        pyautogui.click(
                            locs['node1_btn'][0] + locs['node_offset'] + solver_pos[0],
                            locs['node1_btn'][1] + solver_pos[1])
                    while (imagesearch.imagesearcharea('img/icon1.png',
                        locs['area2'][0] + solver_pos[0],
                        locs['area2'][1] + solver_pos[1],
                        locs['area2'][2] + solver_pos[0],
                        locs['area2'][3] + solver_pos[1])[0] == -1):
                        time.sleep(0.1)
                    range_to_file(raw_data_to_range(get_raw_data(locs['node1_btn'][0] + locs['node_offset'], locs['node1_btn'][1], solver_pos), j + 1, len(raise_sizes) + 1), pot_type, villain_pos, hero_pos, 'fb', str(sizes[i]), str(raise_sizes[j]), board)
                    if j != (len(raise_sizes) - 1):
                        pyautogui.click(
                            locs['node1_btn'][0] + locs['node_offset'] * 2 + solver_pos[0],
                            locs['node1_btn'][1] + (j * locs['vert_offset']) + solver_pos[1])
                        for k in range(len(raise_sizes)): # get oop facing-raise ranges
                            '''
                            pyautogui.click(
                                locs['node1_btn'][0] + locs['node_offset'] * 2 + solver_pos[0],
                                locs['node1_btn'][1] + solver_pos[1])
                            '''
                            while imagesearch.imagesearcharea('img/icon2.png', 
                                locs['area3'][0] + solver_pos[0],
                                locs['area3'][1] + solver_pos[1],
                                locs['area3'][2] + solver_pos[0],
                                locs['area3'][3] + solver_pos[1])[0] == -1:
                                time.sleep(0.1)
                            range_to_file(raw_data_to_range(get_raw_data(locs['node1_btn'][0] + locs['node_offset'] * 2, locs['node1_btn'][1], solver_pos), k + 1, len(raise_sizes) + 1), pot_type, hero_pos, villain_pos, 'fr', str(sizes[i]) + '-' + str(raise_sizes[j]), str(raise_sizes[k]), board)
            pyautogui.click(
                locs['node1_btn'][0] + solver_pos[0],
                locs['node1_btn'][1] + solver_pos[1])

    # set vertical offset based on the height of the tree explorer of GTO+
    vert_offset = (len(sizes) - 2) * locs['vert_offset']

    # find start flop subset:
    if not no_scroll:
        for i in (range(start // 20)):
            select_flop(19, solver_pos, y_offset=vert_offset)

    # generate flop list:
    flops = get_flop_list(legacy_mode=legacy_mode)

    for i in range(1755):
        if i >= start:
            select_flop(i % 20, solver_pos, y_offset=vert_offset) if i < 1740 else select_flop(i % 20 + 9, solver_pos, y_offset = vert_offset)
            add_solution(pot_type, hero_pos, villain_pos, sizes, raise_sizes, flops[i])
            print(str(i))
            print(flops[i])
            time.sleep(0.2)

def get_flop_list(legacy_mode=False):
    flops = []

    if legacy_mode:
        legacy_file = open(legacy_dir, 'r')
        file_content = ''
        for line in legacy_file:
            file_content += line
        flop_list = file_content.splitlines()
        for flop in flop_list:
            flops.append(translate_flop(flop)['flop'])
            pass
    else:
        for i in range(13):
            for j in range(i, 13):
                for k in range(j, 13):
                    if i == j == k:
                        flops.append(pkr_range.index_to_card(k) + 's' + pkr_range.index_to_card(j) + 'd' + pkr_range.index_to_card(i) + 'c')
                    elif i == j:
                        flops.append(pkr_range.index_to_card(k) + 's' + pkr_range.index_to_card(j) + 'd' + pkr_range.index_to_card(i) + 'c')
                        flops.append(pkr_range.index_to_card(k) + 'c' + pkr_range.index_to_card(j) + 'd' + pkr_range.index_to_card(i) + 'c')
                    elif j == k:
                        flops.append(pkr_range.index_to_card(k) + 'd' + pkr_range.index_to_card(j) + 'c' + pkr_range.index_to_card(i) + 's')
                        flops.append(pkr_range.index_to_card(k) + 'd' + pkr_range.index_to_card(j) + 'c' + pkr_range.index_to_card(i) + 'c')
                    else:
                        flops.append(pkr_range.index_to_card(k) + 's' + pkr_range.index_to_card(j) + 'd' + pkr_range.index_to_card(i) + 'c')
                        flops.append(pkr_range.index_to_card(k) + 'd' + pkr_range.index_to_card(j) + 'c' + pkr_range.index_to_card(i) + 'c')
                        flops.append(pkr_range.index_to_card(k) + 'c' + pkr_range.index_to_card(j) + 'd' + pkr_range.index_to_card(i) + 'c')
                        flops.append(pkr_range.index_to_card(k) + 'c' + pkr_range.index_to_card(j) + 'c' + pkr_range.index_to_card(i) + 'd')
                        flops.append(pkr_range.index_to_card(k) + 'c' + pkr_range.index_to_card(j) + 'c' + pkr_range.index_to_card(i) + 'c')

    return flops 

def get_raw_data(x, y, solver_pos):   # grabs a GTO+ range in raw data format
    
    #sub-routines:

    def get_empty_data(total_actions = 4):  #returns an empty GTO+ range in raw data format
        sample_range = pkr_range.PkrRange()
        result = ''

        for i in range(1326):   # 1326 distinct hands
            result += sample_range.get_hand(i) + ('0 ' * (2 + (2 * total_actions) + total_actions + 1)) + '\n'

        return result

    # if x, y are given and image is not detected, click at coordinates x, y and repeat image search until found

    #Find Data Window
    fail_count = 0
    while True:
        if x and y:
            pyautogui.click(x + solver_pos[0], y + solver_pos[1])
        pos = imagesearch.imagesearcharea('img/raw_data_icon.png',
            locs['raw_data_area'][0] + solver_pos[0],
            locs['raw_data_area'][1] + solver_pos[1],
            locs['raw_data_area'][2] + solver_pos[0],
            locs['raw_data_area'][3] + solver_pos[1], absolute=True)
        if pos[0] != -1:
            break
        fail_count += 1
        if fail_count >= 8:
            return get_empty_data()

    #Open Data Window
    fail_count = 0
    while True:
        pyautogui.click(pos[0] + locs['raw_data_offset'][0], pos[1] + locs['raw_data_offset'][1])
        if pyautogui.screenshot(region=(
            locs['data_check'][0] + solver_pos[0],
            locs['data_check'][1] + solver_pos[1],
            locs['data_check'][2],
            locs['data_check'][3],
            )).getpixel((1, 1)) == locs['data_pix']:
            break
        fail_count += 1
        if fail_count > 5:
            pos = imagesearch.imagesearcharea('img/raw_data_icon.png',
                locs['raw_data_area'][0] + solver_pos[0],
                locs['raw_data_area'][1] + solver_pos[1],
                locs['raw_data_area'][2],
                locs['raw_data_area'][3], absolute=True)
    
    while True:
        pyautogui.rightClick(
            locs['data_popup'][0] + solver_pos[0],
            locs['data_popup'][1] + solver_pos[1])
        if pyautogui.screenshot(region=(
            locs['menu_check'][0] + solver_pos[0],
            locs['menu_check'][1] + solver_pos[1],
            locs['menu_check'][2],
            locs['menu_check'][3],
            )).getpixel((1, 1)) == locs['menu_pix']:
            break
    pyautogui.click(
        locs['data_popup'][0] + locs['select_all_offset'][0] + solver_pos[0],
        locs['data_popup'][1] + locs['select_all_offset'][1] + solver_pos[1])
    time.sleep(0.1)
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    pyautogui.press('esc')

    return pyperclip.paste()

def raw_data_to_range(raw_data, action, total_actions): # takes a GTO+ range in raw data format and returns it as a PkrRange
            
            #  action = which action to take; 1 = most aggressive (largest size), higher numbers less aggressive (lower size)
            #  total_actions = total possible actions in the solve (including check)

            result = pkr_range.PkrRange()
            line_data = raw_data.splitlines()
            elements = []

            for line in line_data:
                elements.append(line.split())
            
            for ele in elements:
                hand = pkr_range.hand_to_index(ele[0])
                result.add_combos(float(ele[2 + action]))
                result.set_combos(hand, float(ele[2 + action]))
                result.set_frequency(hand, float(ele[2 + total_actions + action]))
                result.set_ev(hand, float(ele[2 + (2 * total_actions) + action + 1]))

            return result

def select_flop(entry, solver_pos, y_offset=0):   #selects a flop from the flop list inside a solve

    # entry = entry number from the top of the flop list
    # 0 = select first flop in the list
    # 24 = select last flop in the list, then scroll down until only new items are in the last
    
    pyautogui.click(
        locs['run_solver_btn'][0] + solver_pos[0],
        locs['run_solver_btn'][1] + solver_pos[1] + y_offset)
    while imagesearch.imagesearcharea('img/process_database_btn.png', 
        locs['process_db_area'][0] + solver_pos[0],
        locs['process_db_area'][1] + solver_pos[1],
        locs['process_db_area'][2] + solver_pos[0],
        locs['process_db_area'][3] + solver_pos[1])[0] == -1:
        pyautogui.click(
            locs['run_solver_btn'][0] + solver_pos[0],
            locs['run_solver_btn'][1] + solver_pos[1] + y_offset)
        time.sleep(0.1)
    pyautogui.doubleClick(
        locs['select_flop_base'][0] + solver_pos[0],
        locs['select_flop_base'][1] + solver_pos[1] + entry * locs['select_flop_offset'] + y_offset)
    time.sleep(0.2)
    if entry == 19:
        for _ in range(4):
            pyautogui.scroll(-10)

def range_from_db(pot_type, hero_pos, villain_pos, face_action, size, response_size, board):
    file_path = base_dir + '\\' + pot_type + '\\' + hero_pos + '\\' + villain_pos + '\\' + face_action + '\\' + str(size) + '\\' + str(response_size) + '\\' + board + '.txt'
    new_range = pkr_range.PkrRange()
    new_range.read_range_from_file(file_path)

    return new_range

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

def translate_flop(flop):
    '''
    Returns translation dictionary to translate suits from actual suits to the one's matching
    the database solution for the given flop without loss of information or accuracy.

    'flop' key of returned dictionary contains the translated flop.
    '''

    #check if flop is three of a kind

    def trips(input_cards):
        return input_cards[0][0] == input_cards[1][0] == input_cards[2][0]

    #check if flop's two highest cards are paired
    
    def high_paired(input_cards):
        return input_cards[0][0] == input_cards[1][0] != input_cards[2][0]

    #check if flop's two lowest cards are paired
    
    def low_paired(input_cards):
        return input_cards[1][0] == input_cards[2][0] != input_cards[0][0]

    #check if flop consists of three different cards

    def regular(input_cards):
        return input_cards[0][0] != input_cards[1][0] != input_cards[2][0]

    #check if flop is rainbow

    def rainbow(input_cards):
        return ((input_cards[0][1] != input_cards[1][1]) and
            (input_cards[0][1] != input_cards[2][1]) and
            (input_cards[1][1] != input_cards[2][1]))

    #check if flop is monotone
    
    def monotone(input_cards):
        return input_cards[0][1] == input_cards[1][1] == input_cards[2][1]

    #check if flop's two highest cards are the same suit

    def top_suited(input_cards):
        return input_cards[0][1] == input_cards[1][1] != input_cards[2][1]

    #check if flop's highest card and lowest card are the same suit
    
    def top_bot_suited(input_cards):
        return input_cards[0][1] == input_cards[2][1] != input_cards[1][1]

    #check if flop's two lowest cards are the same suit

    def bot_suited(input_cards):
        return input_cards[1][1] == input_cards[2][1] != input_cards[0][1]

    def swap_cards(input_cards, card1, card2):
        temp = input_cards[card1]
        input_cards[card1] = input_cards[card2]
        input_cards[card2] = temp
        return input_cards

    def get_translation(input_cards, suit1, suit2, suit3):
        suits = ('s', 'h', 'd', 'c')
        trans_dict = {input_cards[0][1]: suit1, input_cards[1][1]: suit2, input_cards[2][1]: suit3}
        trans_keys = trans_dict.keys()
        trans_values = trans_dict.values()

        # Make sure every suit is mapped to another suit, and no suits are mapped to the same suit:
        for curr_suit in suits:
            if (not curr_suit in trans_keys) and (curr_suit in trans_values):
                for suit in suits:
                    if not suit in trans_values:
                        trans_dict[curr_suit] = suit
            elif (not curr_suit in trans_keys) and (not curr_suit in trans_values):
                trans_dict[curr_suit] = curr_suit

        return trans_dict


    translation = {}
    
    #cards ordered from highest to lowest

    #suit order:
    #three of a kind flop:          s, d, c
    #low paired rb flop:            s, d, c
    #low paired suited flop:        c, d, c
    #high paired rb flop:           d, c, s
    #high paired suited flop:       d, c, c
    #regular rb flop:               s, d, c
    #regular suited bottom flop:    d, c, c
    #regular suited top/bot flop:   c, d, c
    #regular suited top flop:       c, c, d
    #monotone flop:                 c, c, c

    #sort cards:

    cards = [flop[:2], flop[2:4], flop[4:]]

    cards.sort(key=lambda element: pkr_range.card_to_index(element[0]), reverse=True)

    if regular(cards):
        if rainbow(cards):
            translation = get_translation(cards, 's', 'd', 'c')
        elif bot_suited(cards):
            translation = get_translation(cards, 'd', 'c', 'c')
        elif top_bot_suited(cards):
            translation = get_translation(cards, 'c', 'd', 'c')
        elif top_suited(cards):
            translation = get_translation(cards, 'c', 'c', 'd')
        elif monotone(cards):
            translation = get_translation(cards, 'c', 'c', 'c')
    elif low_paired(cards): 
        if rainbow(cards):
            translation = get_translation(cards, 's', 'd', 'c')
        elif top_suited(cards):
            cards = swap_cards(cards, 1, 2)
            translation = get_translation(cards, 'c', 'd', 'c')
        elif  top_bot_suited(cards):
            translation = get_translation(cards, 'c', 'd', 'c')
    elif high_paired(cards):
        if rainbow(cards):
            translation = get_translation(cards, 'd', 'c', 's')
        elif top_bot_suited(cards):
            swap_cards(cards, 0, 1)
            translation = get_translation(cards, 'd', 'c', 'c')
        elif bot_suited(cards):
            translation = get_translation(cards, 'd', 'c', 'c')
    elif trips(cards):
        translation = get_translation(cards, 's', 'd', 'c')
    else:
        print('Invalid Flop. Cannot translate.')
    
    translation['flop'] = apply_translation(cards[0][0] + cards[0][1] + cards[1][0] + cards[1][1] + cards[2][0] + cards[2][1], translation)

    return translation

def apply_translation(card_string, translation, reverse=False):
    '''
    Translates a card string using a tranlation dictionary returned by translate_flop().
    Returns the translated card string.

    If reverse = True, reverses the translation of a translated card_string and returns the original card string.
    '''
    new_card_string = ''
    if len(card_string) % 2 == 0:
        if not reverse:
            for i in range(0, len(card_string), 2):
                new_card_string += card_string[i] + (translation[card_string[i + 1]])
        else:
            for i in range(0, len(card_string), 2):
                new_card_string += card_string[i] + util.get_key_by_value(translation, card_string[i + 1])
        return new_card_string

    else:
        print('Invalid card_string: Odd number of characters.')
        return None

def check_solve(pot_type, hero_pos, villain_pos, facing, face_size, response_size, action, total_actions, solver_pos, legacy_mode=False, start=19):
    flops = get_flop_list(legacy_mode=legacy_mode)
    vert_offset = (total_actions - 2) * locs['vert_offset']
    correct = True

    for i in range(start, 1755, 20):
        select_flop(19, solver_pos, y_offset=vert_offset)
        pyperclip.copy(get_raw_data(locs['node1_btn'][0], locs['node1_btn'][1], solver_pos))
        path = base_dir + '\\{pot_type}\\{hero_pos}\\{villain_pos}\\{face_action}\\{face_size}\\{response_size}\\{board}.txt'.format(
            pot_type=pot_type, 
            hero_pos=hero_pos, 
            villain_pos=villain_pos, 
            face_action=facing, 
            face_size=face_size, 
            response_size=response_size,
            board=flops[i]
        )

        if solve_equals_file(path, action, total_actions):
            print("{flop} ({i}): Correct".format(flop=flops[i], i=i))
        else:
            print(colored("{flop} ({i}): ERROR".format(flop=flops[i], i=i)))
            correct = False

    if correct:
        print(colored("=" * 20 + '\nSOLVE DATA CORRECT\n' + "=" * 20, 'green'))
    else:
        print(colored("=" * 20 + '\nERRORS IN DATA\n' + "=" * 20, 'red'))

def solve_equals_file(path, action, total_actions):
    clipboard = parse_raw_data(pyperclip.paste(), action, total_actions)
    file_text = ''
    try:
        file = open(path, 'r')
    except:
        print("Path not found.")
        return False
    for line in file:
        file_text += line

    return clipboard == file_text

r'''
solver_pos = ()
for window in get_window_list():
    if 'GTO' in window[1]:
        solver_pos = (window[2][0], window[2][1])

add_solve('3bp', 'sb', 'lj', [66.7, 33.3, 0.0], [75.0, 0.0], solver_pos, start=0)
#check_solve('3bp', 'sb', 'btn', 'fx', '0.0', '66.7', 1, 3, solver_pos)
'''