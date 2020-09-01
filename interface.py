'''
Implements functionality to interact with the poker UI.

Fully Documented.

TODO: 1
'''

import pyautogui, win32gui, win32con, random, time, pytesseract
from PIL import ImageOps, ImageEnhance
from termcolor import colored

import util
from pkr_range import card_to_index

#TODO: Move profiles into a JSON or *.txt file.

random.seed()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Global Poker, Large Screen, 1 Table:
gp_large_one_table = {
    'site': 'gp',
    'table_title': 'NO_LIMIT',
    'table_window': (1910, 0, 1940, 2110),
    'solver_window': (-7, 0, 1051, 2110),
    'table_area': (
        (2040, 598, 1661, 1038),
    ),
    'seat': (   #(x, y, low_bound, high_bound)
        (107, 649, 90, 100),    
        (112, 297, 75, 85),
        (824, 150, 70, 80),
        (1531, 296, 75, 85),
        (1522, 650, 90, 100),
    ),
    'seat_pix': None,
    'sitting_out': (    #(x, y, expected_pixel_value)
        (100, 680, 128),
        (100, 330, 117),
        (800, 182, 153),
        (1544, 330, 116),
        (1544, 680, 127),
    ),
    'waiting': (
        (127, 680),
        (),
        (827, 182),
        (),
        (1571, 680),     #128
    ),
    'cards': (
        (141, 578),
        (143, 230),
        (843, 85),
        (1545, 229),
        (1546, 577),
    ),
    'cards_pix': (94, 142, 164),
    'bet_chips': (
        (376, 566),
        (376, 340),
        (789, 239),
        (1304, 340),
        (1304, 567),
    ),
    'bet_chips_pix': (255, 255, 255),
    'bet_chips_not_pix': None,
    'bet_amount': (
        (2440, 1151, 78, 30),
        (2440, 923, 78, 30),
        (2851, 824, 78, 30),
        (3234, 923, 78, 30),
        (3234, 1151, 78, 30),
    ),
    'bet_option': None,
    'stack_size': (
        (2080, 1230, 144, 32),
        (2080, 880, 144, 32),
        (2776, 732, 144, 32),
        (3530, 880, 144, 32),
        (3530, 1230, 144, 32),
    ),
    'pot_size': None,
    'button': ( #(x, y, expected_pixel_value)
        (331, 570, 154),
        (330, 344, 168),
        (743, 243, 176),
        (1342, 344, 156),
        (1342, 570, 154),
    ),
    'button_pix': (
        (154, 154, 154),
        (168, 168, 168),
        (176, 176, 176),
        (156, 156, 156),
        (154, 154, 154),
    ),
    'board_ranks': (
        (2635, 990, 45, 31),
        (2735, 990, 45, 31),
        (2835, 990, 45, 31),
        (2935, 990, 45, 31),
        (3035, 990, 45, 31),
    ),
    'board_suits': (
        (626, 488),
        (729, 488),
        (830, 488),
        (941, 488),
        (1033, 488),
    ),
    'board_suits_pix':(
        (), # Spade
        (), # Heart
        (), # Diamond
        (), # Club
    ),
    'card_dealt': (
        (), # 3rd card
        (), # 4th card
        (), # 5th card
    ),
    'card_dealt_pix': (),
    'active': (
        (),
        (),
        (),
        (),
        (),
    ),
    'hero_active': (1371, 1002),
    'hero_active_pix': (152, 45, 29),
    'hero_active_not_pix': None,
    'hero_cards': (854, 707),
    'hero_cards_pix': (255, 255, 255),
    'hero_ranks': (2815, 1288, 70, 25),
    'hero_suits': (
        (787, 729),
        (819, 728)
    ),
    'fold': (3455, 1592),
    'check_call': (3598, 1592),
    'bet_raise': (3761, 1592),
    'betsize': (3754, 1501)
}
#Bovada, Large Screen, 1 Table:
bovada_large_one_table = {
    'site': 'bovada',
    'table_title': 'No Limit Hold',
    'table_window': [(952, 0, 976, 1038)],
    'solver_window': (-7, 0, 1051, 2110),
    'table_area': (33, 214, 899, 559),
    'seat': (   #(x, y, low_bound, high_bound)
        (99, 349, 0, 0),
        (99, 133, 0, 0),
        (455, 67, 0, 0),
        (810, 133, 0, 0),
        (810, 349, 0, 0)
    ),
    'seat_pix': (
        (207, 214, 214),
        (207, 214, 214),
        (207, 214, 214),
        (207, 214, 214),
        (207, 214, 214)
    ),
    'sitting_out': (    #(x, y, expected_pixel_value)
        None,
        None,
        None,
        None,
        None,
    ),
    'waiting': (
        None,
        None,
        None,
        None,
        None
    ),
    'cards': (
        (125, 353),
        (125, 135),
        (479, 70),
        (834, 135),
        (834, 353)
    ),
    'cards_pix': (43, 43, 43),
    'bet_chips': (
        (158, 351),
        (186, 223),
        (542, 157),
        (680, 223),
        (707, 351)
    ),
    'bet_chips_pix': None,
    'bet_chips_not_pix': (13, 52, 52),
    'bet_amount': (
        (202, 556, 55, 20),
        (229, 427, 55, 20),
        (585, 361, 55, 20),
        (722, 427, 55, 20),
        (750, 556, 55, 20)
    ),
    'bet_option': (602, 911, 178, 22),
    'stack_size': (
        (100, 605, 80, 22),
        (100, 389, 80, 22),
        (455, 324, 80, 22),
        (812, 390, 80, 22),
        (812, 606, 80, 22)
    ),
    'pot_size': (502, 401, 99, 20),
    'button': ( #(x, y)
        (191, 406),
        (191, 190),
        (547, 109),
        (720, 190),
        (720, 406)
    ),
    'button_pix': (
        (206, 33, 39),
        (206, 33, 39),
        (206, 33, 39),
        (206, 33, 39),
        (206, 33, 39),
    ),
    'board_ranks': (
        (302, 453, 45, 35),
        (380, 453, 45, 35),
        (458, 453, 45, 35),
        (536, 453, 45, 35),
        (613, 453, 45, 35),
    ),
    'board_suits': (
        (304, 304),
        (380, 304),
        (459, 304),
        (536, 304),
        (614, 304)
    ),
    'board_suits_pix':(
        (0, 0, 0), # Spade
        (200, 0, 0), # Heart
        (0, 138, 207), # Diamond
        (50, 160, 40), # Club
    ),
    'card_dealt': (
        (474, 248), # 3rd card
        (551, 248), # 4th card
        (629, 248), # 5th card
    ),
    'card_dealt_pix': (255, 255, 255),
    'active': (
        (148, 371),
        (148, 154),
        (503, 89),
        (866, 154),
        (866, 371)
    ),
    'active_not_pix': (13, 52, 52),
    'hero_active': (511, 441),
    'hero_active_pix': None,
    'hero_active_not_pix': (13, 52, 52),
    'hero_cards': (492, 399),
    'hero_cards_pix': (255, 255, 255),
    'hero_bet_chips': (432, 375),
    'hero_stack_size': (455, 674, 80, 22),
    'hero_ranks': (
        (442, 607, 33, 23),
        (491, 607, 33, 23)
    ),
    'hero_suits': (
        (432, 438),
        (482, 438)
    ),
    'fold': None,
    'check_call': None,
    'bet_raise': None,
    'betsize': None
}

cc = bovada_large_one_table

def isRealWindow(hWnd):
    '''
    Return True iff given window is a real Windows application window.
    '''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def get_window_list():
    '''
    Return a list of tuples (handle, title (x, y, width, height)) for each real window.
    '''
    def callback(hWnd, windows):
        if not isRealWindow(hWnd):
            return
        rect = win32gui.GetWindowRect(hWnd)
        title = win32gui.GetWindowText(hWnd)
        windows.append((hWnd, title, (rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1])))
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def get_table_list(window_list=None):
    if window_list == None:
        window_list = get_window_list()
    
    return list(filter(lambda window: cc['table_title'] in window[1], window_list))

def get_profile(site, table_list, screensize):
    '''
    Sets the coordinate profile based on screensize and the list of open tables, table_list.
    site = 'gp'             --> Global Poker
    site = 'bovada'         --> Bovada
    screensize = 'large'    --> Main Desktop Screen
    '''
    if site == 'gp':
        if screensize == 'large':
            if len(table_list) == 1:
                return gp_large_one_table
            else:
                print("ERROR in get_profile(): Invalid Table Count:", len(table_list))
        else:
            print("ERROR in get_profile(): Invalid Screen Size:", screensize)
    if site == 'bovada':
        if screensize == 'large':
            if len(table_list) == 1:
                return bovada_large_one_table
            else:
                print("ERROR in get_profile(): Invalid Table Count:", len(table_list))
        else:
            print("ERROR in get_profile(): Invalid Screen Size:", screensize)
    else:
        print("ERROR in get_profile(): Invalid Site Name:", cc['site'])

def positionTables(poker_tables):
    '''
    Position the windows in the list into the layout defined in the current profile.
    '''
    if len(poker_tables) == 0:
        print("ERROR in positionTables(): No existing tables.")
    if len(poker_tables) == 1:
        win32gui.SetWindowPos(poker_tables[0][0], win32con.HWND_TOP, cc['table_window'][0][0], cc['table_window'][0][1], cc['table_window'][0][2], cc['table_window'][0][3], 0)
    elif len(poker_tables) >= 2:
        pass

def positionSolver(window_list):
    '''
    Positions the solver at the position defined in the current profile.
    '''
    for win in window_list:
        if 'GTO' in win[1]:
            win32gui.SetWindowPos(win[0], win32con.HWND_TOP, cc['solver_window'][0], cc['solver_window'][1], cc['solver_window'][2], cc['solver_window'][3], 0)
            break

def fold(handle):
    '''
    Takes handle of a poker table window.
    Interacts with the poker UI to fold.
    '''
    win32gui.SetForegroundWindow(handle)

    if cc['site'] == 'gp':
        pyautogui.click(cc['fold'])
    elif cc['site'] == 'bovada':
        pyautogui.press('q')
    else:
        print("ERROR in fold(): Invalid Site Name:", cc['site'])

def check_call(handle):
    '''
    Takes handle of a poker table window.
    Interacts with the poker UI to check or call.
    '''
    win32gui.SetForegroundWindow(handle)

    if cc['site'] == 'gp':
        pyautogui.click(cc['check_call'])
    elif cc['site'] == 'bovada':
        pyautogui.press('w')
    else:
        print("ERROR in check_call(): Invalid Site Name:", cc['site'])

def bet(handle, amount=None):
    '''
    Takes handle of a poker table window.
    Interacts with the poker UI to place a bet of the given size, or by default the current bet.
    '''
    win32gui.SetForegroundWindow(handle)

    if cc['site'] == 'gp':
        if amount != None:
            pyautogui.click(cc['betsize'])

            for char in amount:
                time.sleep(random.randrange(100, 300)/1000)
                pyautogui.press(char)

            time.sleep(random.randrange(100, 300)/1000)
        pyautogui.click(cc['bet_raise'])

    elif cc['site'] == 'bovada':
        if amount == None:
            pyautogui.press('e')
        elif amount == 33.3:
            pyautogui.press('1')
        elif amount == 66.7:
            pyautogui.press('2')
        elif amount == 75.0:
            pyautogui.press('3')
        else:
            print("ERROR in bet(): Invalid Betsize:", amount)
    else:
        print("ERROR in bet(): Invalid Site Name:", cc['site'])
    
def seat_open(player_pos, img):
    '''
    Takes an integer between 0 and 5, defining the seat (clockwise positions starting at the bottom).
    Takes a screenshot of a poker table.
    Returns True if the seat on the given table is open and False otherwise.
    '''
    if not 0 <= player_pos <= 5:
        print("ERROR in seat_open(): Invalid Player Position:", player_pos)
        return None

    player_pos -= 1

    if player_pos == -1:
        return False

    rgb_val = img.getpixel((cc['seat'][player_pos][0], cc['seat'][player_pos][1]))
    if cc['site'] == 'gp':
        return True if cc['seat'][player_pos][2] < rgb_val[0] < cc['seat'][player_pos][3] and cc['seat'][player_pos][2] < rgb_val[1] < cc['seat'][player_pos][3] and cc['seat'][player_pos][2] < rgb_val[2] < cc['seat'][player_pos][3] else False
    elif cc['site'] == 'bovada':
        return True if rgb_val == cc['seat_pix'][player_pos] else False

def has_cards(player_pos, img):
    '''
    Takes player_pos as an Integer; 0 = bottom position. 1, 2, 3, 4 = clockwise positions.
    Takes img, a screenshot of the poker table.
    Returns True if player in position player_pos has cards.
    '''
    if not 0 <= player_pos <= 5:
        print("ERROR in has_cards(): Invalid Player Position:", player_pos)
        return None

    player_pos -= 1

    if player_pos == -1:
        return hero_has_cards(img)

    return True if img.getpixel((cc['cards'][player_pos][0], cc['cards'][player_pos][1])) == cc['cards_pix'] else False

def button_pos(img):
    '''
    Returns Seat number that is has the button. Returns -1 if Hero has the button.
    Outputs: -1 to 4
    '''
    for i in range(5):
        rgb_val = img.getpixel((cc['button'][i][0], cc['button'][i][1]))
        if (rgb_val == cc['button_pix'][i]):
            return i + 1

    return 0

def has_bet(player_pos, img):
    '''
    Takes an integer between 0 and 5, defining the seat (clockwise positions starting at the bottom).
    Takes a screenshot of a poker table.
    Returns True if the seat on the given table has bet and False otherwise.
    '''
    if not 0 <= player_pos <= 5:
        print("ERROR in has_bet(): Invalid Player Position:", player_pos)
        return None

    player_pos -= 1

    if player_pos == -1:
            return hero_has_bet(img)
    
    if cc['site'] == 'gp':
        return True if img.getpixel(cc['bet_chips'][player_pos]) == cc['bet_chips_pix'] else False
    elif cc['site'] == 'bovada':
        return True if img.getpixel(cc['bet_chips'][player_pos]) != cc['bet_chips_not_pix'] else False

def hero_has_bet(img):
    '''
    Takes a screenshot of a poker table.
    Returns True if hero has bet and False otherwise.
    '''
    if cc['site'] == 'bovada':
        return True if img.getpixel(cc['hero_bet_chips']) != cc['bet_chips_not_pix'] else False

def read_betsize(player_pos, i):
    '''
    Takes an integer between 0 and 5, defining the seat (clockwise positions starting at the bottom).
    Takes the table index to read from.
    Returns the size of the bet that seat on that table has placed.
    '''
    if not 1 <= player_pos <= 5:
        print("ERROR in read_betsize(): Invalid Player Position:", player_pos)
        return None

    player_pos -= 1

    img = pyautogui.screenshot(region=(
        cc['bet_amount'][player_pos][0] + cc['table_window'][i][0],
        cc['bet_amount'][player_pos][1] + cc['table_window'][i][1],
        cc['bet_amount'][player_pos][2],
        cc['bet_amount'][player_pos][3],
    ))
    img = ImageOps.grayscale(img)
    img = ImageOps.invert(img)
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2)
    img.save('img_debug/betsize' + str(player_pos + 1) + '.png')

    betsize = pytesseract.image_to_string(img, config='--psm 7')

    if cc['site'] == 'bovada':
        return extract_number(betsize)
    elif cc['site'] == 'gp':
        return betsize

def read_bet_option(i):
    '''
    Returns the bet size currently entered in the bet size selector on the poker UI
    on the i'th table.
    '''
    img = pyautogui.screenshot(region=(
        cc['bet_option'][0] + cc['table_window'][i][0],
        cc['bet_option'][1] + cc['table_window'][i][1],
        cc['bet_option'][2],
        cc['bet_option'][3],
    ))
    img = ImageOps.grayscale(img)
    img = ImageOps.invert(img)
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2)
    img.save('img_debug/bet_option.png')

    bet_option = pytesseract.image_to_string(img, config='--psm 7')

    return extract_number(bet_option)

def read_potsize(i):
    '''
    Returns the current size of the pot on the i'th table.
    '''
    img = pyautogui.screenshot(region=(
        cc['pot_size'][0] + cc['table_window'][i][0],
        cc['pot_size'][1] + cc['table_window'][i][1],
        cc['pot_size'][2],
        cc['pot_size'][3],
    ))
    img = ImageOps.grayscale(img)
    img = ImageOps.invert(img)
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2)
    img.save('img_debug/potsize.png')

    potsize = pytesseract.image_to_string(img, config='--psm 7')

    return extract_number(potsize)

def extract_number(inp_str):
    '''
    Takes a string.
    Returns the floating point number contained in the string, or an empty
    string if no valid number is found.
    '''
    i = 0
    while(i < len(inp_str)):
        if not (inp_str[i].isdigit() or inp_str[i] == '.'):
            inp_str = inp_str[0:i] + inp_str[i + 1: len(inp_str)]
        else:
            i = i + 1

    if not util.is_number(inp_str):
        inp_str = ''
    
    return inp_str

def current_street(img):
    '''
    Takes a screenshot of a poker table.
    Returns the current street of the game.
    '''
    if img.getpixel(cc['card_dealt'][2]) == cc['card_dealt_pix']:
        return 'river'
    elif img.getpixel(cc['card_dealt'][1]) == cc['card_dealt_pix']:
        return 'turn'
    elif img.getpixel(cc['card_dealt'][0]) == cc['card_dealt_pix']:
        return 'flop'
    else:
        return 'preflop'

def is_active(player_pos, img):
    '''
    Takes an integer between 0 and 5, defining the seat (clockwise positions starting at the bottom).
    Takes a screenshot of a poker table.
    Returns True if it is the given seat's turn to act, and False otherwise.
    '''
    player_pos -= 1

    if player_pos == -1:
        return is_hero_turn(img)

    return img.getpixel(cc['active'][player_pos]) != cc['active_not_pix']
    
def is_hero_turn(img):
    '''
    Takes a screenshot of a poker table.
    Returns True if it is the hero's turn to act, and False otherwise.
    '''
    if cc['site'] == 'gp':
        return True if img.getpixel(cc['hero_active']) == cc['hero_active_pix'] else False
    elif cc['site'] == 'bovada':
        return True if img.getpixel(cc['hero_active']) != cc['hero_active_not_pix'] else False

def sitting_out(player_pos, img):
    '''
    Takes an integer between 0 and 5, defining the seat (clockwise positions starting at the bottom).
    Takes a screenshot of a poker table.
    Returns True if player in position player_pos is sitting out, and False otherwise.
    '''
    if not 0 <= player_pos <= 5:
        print("ERROR in sitting_out(): Invalid Player Position:", player_pos)
        return None

    player_pos -= 1

    if player_pos == -1:
        return False

    rgb = img.getpixel((cc['sitting_out'][player_pos][0], cc['sitting_out'][player_pos][1]))
    return (rgb[0] == cc['sitting_out'][player_pos][2]
        and rgb[1] == cc['sitting_out'][player_pos][2]
        and rgb[2] == cc['sitting_out'][player_pos][2])

def interp_suit(rgb):
        '''
        Takes (r, g, b) tuble.
        Returns suit string: 'hc' = heart club, 'ds' = diamond space, etc
        '''
        if rgb[0] - 50 > rgb[1] and rgb[0] - 50 > rgb[2]:
            return 'h'
        elif rgb[1] - 50 > rgb[0] and rgb[1] - 50 > rgb[2]:
            return 'c'
        elif rgb[2] - 50 > rgb[1] and rgb[2] - 50 > rgb[0]:
            return 'd'
        elif rgb[0] < 70 and rgb[1] < 70 and rgb[2] < 70:
            return 's'
        else:
            return '-'

def img_to_inv_cont(img):
    '''
    Takes a PIL Image.
    Returns the image after applying an invert filter, and enhacing the contrast by two units.
    '''
    invert_img = ImageOps.invert(img)
    contrast = ImageEnhance.Contrast(invert_img)
    invert_img = contrast.enhance(2)

    return invert_img

def hero_has_cards(img):
    '''
    Takes a screenshot of a poker table.
    Returns True if the hero has cards, and False otherwise.
    '''
    return img.getpixel(cc['hero_cards']) == cc['hero_cards_pix']

def hero_hand(img, table_id):
    '''
    Takes a screenshot of a poker table.
    Returns the hand that was dealt to the hero as a card string (for example, 'As6c').
    '''
    def hero_suits():
        '''
        Returns the suits of the hero's cards (for example, 'sc' for spade, club).
        '''
        rgb_val_left = img.getpixel(cc['hero_suits'][0])
        rgb_val_right = img.getpixel(cc['hero_suits'][1])

        return interp_suit(rgb_val_left) + interp_suit(rgb_val_right)

    def hero_ranks(table_id):
        '''
        Returns the ranks of the hero's cards (for example, 'A6').
        '''
        if cc['site'] == 'gp':
            img = pyautogui.screenshot(region=cc['hero_ranks'])
            img = ImageOps.grayscale(img)
            contrast = ImageEnhance.Contrast(img)
            img = contrast.enhance(2)
            img.save('img_debug/hero_ranks.png')

            text = pytesseract.image_to_string(img, config='--psm 10')
        elif cc['site'] == 'bovada':
            text = ''

            for i in range(2):
                img = pyautogui.screenshot(region=(
                    cc['hero_ranks'][i][0] + cc['table_window'][table_id][0],
                    cc['hero_ranks'][i][1] + cc['table_window'][table_id][1],
                    cc['hero_ranks'][i][2],
                    cc['hero_ranks'][i][3],
                ))
                img = ImageOps.grayscale(img)
                contrast = ImageEnhance.Contrast(img)
                img = contrast.enhance(2)
                img.save('img_debug/hero_ranks' + str(i) + '.png')

                text += pytesseract.image_to_string(img, config='--psm 10')
        else: 
            print("ERROR in hero_ranks(): Invalid Site Name:", cc['site'])

        text = text.replace(' ', '')
        text = text.replace('10', 'T')

        if len(text) == 2:
            for c in text:
                if not c in ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
                    return None
            return text
        
        return None
    
    suits = hero_suits()
    ranks = hero_ranks(table_id)

    #Invalid readings:
    if not (suits and ranks):
        return None

    #Sort the cards such that the highest card is on the left.

    if card_to_index(ranks[0]) < card_to_index(ranks[1]):
        ranks = (ranks[1], ranks[0])
        suits = (suits[1], suits[0])

    return ranks[0] + suits[0] + ranks[1] + suits[1]

def player_stacksize(player_pos, i):
    '''
    Takes an integer between 0 and 5, defining the seat (clockwise positions starting at the bottom).
    Takes an integer specifying the table to read from.
    Returns that seat's stacksize.
    '''
    if not 0 <= player_pos <= 5:
        print("ERROR in player_stacksize(): Invalid Player Position:", player_pos)
        return None

    player_pos -= 1
    
    if player_pos == -1:
        return hero_stacksize(i)

    img = pyautogui.screenshot(region=(
        cc['stack_size'][player_pos][0] + cc['table_window'][i][0],
        cc['stack_size'][player_pos][1] + cc['table_window'][i][1],
        cc['stack_size'][player_pos][2],
        cc['stack_size'][player_pos][3],
    ))
    img.save('img_debug/stacksize' + str(player_pos + 1) + '.png')

    if cc['site'] == 'gp':
        img = img_to_inv_cont(img)
    elif cc['site'] == 'bovada':
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(2)
    else: 
        print("ERROR in player_stacksize(): Invalid Site Name:", cc['site'])

    text = pytesseract.image_to_string(img, config='--psm 7')
    
    text = extract_number(text)

    if text == '':
        text = '-1'

    return text

def hero_stacksize(i):
    '''
    Returns hero's stacksize on the i'th table.
    '''
    img = pyautogui.screenshot(region=(
        cc['hero_stack_size'][0] + cc['table_window'][i][0],
        cc['hero_stack_size'][1] + cc['table_window'][i][1],
        cc['hero_stack_size'][2],
        cc['hero_stack_size'][3],
    ))
    img.save('img_debug/stacksize0.png')

    if cc['site'] == 'gp':
        img = img_to_inv_cont(img)
    elif cc['site'] == 'bovada':
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(2)
    else: 
        print("ERROR in hero_stacksize(): Invalid Site Name:", cc['site'])

    text = pytesseract.image_to_string(img, config='--psm 7')
    
    text = extract_number(text)

    if text == '':
        text = '-1'

    return text

def read_board(img, table_id, start_street=None):
    '''
    Returns the entire board of the i'th poker table if street = None.
    If a street is given, starts returning cards from that street from table i.
    If start_street = 'recent', only readts the most recent street.
    '''
    table_street = current_street(img)
    if start_street == 'recent':
        start_street = table_street

    board = ''
    cards = 0
    first_card = 0

    if table_street == 'flop':
        cards = 3
    elif table_street == 'turn':
        cards = 4
    elif table_street == 'river':
        cards = 5

    if start_street == 'turn':
        first_card = 3
    elif start_street == 'river':
        first_card = 4

    for i in range(first_card, cards):
        board += board_rank(i, table_id) + board_suits(i, img)

    return board
    
def board_rank(i, table_id):
    '''
    Takes an integer specifying the table.
    Returns the rank of the i'th card on the board, where i = 0 is the first card.
    '''
    img = pyautogui.screenshot(region=(
        cc['board_ranks'][i][0] + cc['table_window'][table_id][0],
        cc['board_ranks'][i][1] + cc['table_window'][table_id][1],
        cc['board_ranks'][i][2],
        cc['board_ranks'][i][3],
    ))
    img = ImageOps.grayscale(img)
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(2)
    img.save('img_debug/board_rank' + str(i) + '.png')

    text = pytesseract.image_to_string(img, config='--psm 10')

    text = text.replace(' ', '')
    #text = text.replace ('g', '')
    text = text.replace('10', 'T')

    if not ((text.isalpha() or text.isdigit()) and len(text) <= 2):
        text = ''

    return text

def board_suits(i, img):
    '''
    Takes a screenshot of a poker table.
    Returns the suit of the i'th board card as 'c', 'h', 'd', 's'
    Returns '' if the i'th board card is not dealt.
    '''
    img.save(r'img_debug\board_suits.png')
    rgb_val = img.getpixel(cc['board_suits'][i])

    if rgb_val == cc['board_suits_pix'][0]:
        return 's'
    elif rgb_val == cc['board_suits_pix'][1]:
        return 'h'
    elif rgb_val == cc['board_suits_pix'][2]:
        return 'd'
    elif rgb_val == cc['board_suits_pix'][3]:
        return 'c'
    else:
        print(colored("ERROR in board_suits(). Invalid pixel RGB value:", rgb_val, 'red'))
        return  ''

def get_table_img(i):
    '''
    Returns a screenshot of the i'th table.
    '''
    return pyautogui.screenshot(region=(
        cc['table_area'][0] + cc['table_window'][i][0],
        cc['table_area'][1] + cc['table_window'][i][1],
        cc['table_area'][2],
        cc['table_area'][3],
    ))

def get_stakes(table_title):
    '''
    Takes the title of a poker table window.
    Returns the table's stakes as a tuple: (sb, bb)
    '''
    if cc['site'] == 'bovada':
        bb_value = table_title[table_title.index('/') + 2:]
        bb_value = bb_value[:bb_value.index(' ')]
        
        sb_value = table_title[table_title.index('$') + 1:]
        sb_value = sb_value[:sb_value.index('/')]

        return (float(sb_value), float(bb_value))

def debug():
    window_list = get_window_list()
    poker_tables = get_table_list(window_list=window_list)
    print(poker_tables)
    positionTables(poker_tables)

    table_index = 0

    playing = True
    while playing:
        action = input("Action: ")
        table_img = get_table_img(table_index)
        table_img.save('img_debug/table.png')
        if action == 'fold':
            fold(poker_tables[0][0])

        elif action == 'check' or action == 'call':
            check_call(poker_tables[0][0])

        elif action[0:3] == 'bet':
            bet(action[4:])

        elif action == 'seat status':
            for i in range(6):
                if seat_open(i, table_img):
                    print("Seat", i, "is open.")
                else:
                    print("Seat", i, "is taken.")

        elif action == 'sitout status':
            for i in range(5):
                print("Seat", i, "is", ("sitting out." if sitting_out(i, table_img) else "not sitting out."))

        elif action == 'waiting status':
            pass
            #print(table_img.getpixel((cc['waiting'][testing][0], cc['waiting'][testing][1])))
        
        elif action == 'active status':
            for i in range(0, 6):
                print("Seat {num}: {active}".format(num=i, active= "Active" if is_active(i, table_img) else "Inactive"))

        elif action == 'card status':
            for i in range(6):
                print("Player", i, ("has cards." if has_cards(i, table_img) else "folded."))

        elif action == 'invested status':
            for i in range(1, 6):
                if has_bet(i, table_img):
                    amount = read_betsize(i, table_index)
                    print("Seat", i, "Bet:", amount)

        elif action == 'button status':
            print("Seat", button_pos(table_img), "has the button.")

        elif action == 'hero status':
            print("Hero", ("has cards." if hero_has_cards(table_img) else "does not have cards."))
            print("Hero has", ("bet." if has_bet(-1, table_img) else "not bet."))
            print("Hero is", ("active." if is_hero_turn(table_img) else "inactive."))

        elif action == 'hand status':
            if hero_has_cards(table_img):
                print('Hero Hand:', hero_hand(table_img, table_index))
            else:
                print("Hero does not have cards.")

        elif action == 'board status':
            print("Board:", read_board(table_img, table_index))

        elif action == 'stacksize status':
            for i in range(6):
                print("Seat", i, "Stack:", player_stacksize(i, table_index))

        elif action == 'pot status':
            print("Potsize:", read_potsize(table_index))

        elif action == 'option status':
            print("Bet Option:", read_bet_option(table_index))
            
        elif action == 'street status':
            print("Street:", current_street(table_img))

        elif action == 'stakes status':
            stakes = get_stakes(poker_tables[0][1])
            print("Stakes:", str(stakes[0]) + '/' + str(stakes[1]))

        elif action == 'end':
            playing = False

        else:
            print("Invalid. Try again.")

#debug()