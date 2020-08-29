'''
Implements functionality to set up, solve, and query a real-time GTO+ solution.
'''

import pyperclip
import pyautogui as auto
import database as db
import pkr_range
import util
import imagesearch
import time
import win32gui
import pytesseract
from interface import get_window_list
from PIL import ImageOps, ImageEnhance

locs = {
        'oop_range_btn': (80, 255),
        'oop_range_check': (88, 295, 3, 3),
        'oop_range_pix': (0, 174, 239),
        'ip_range_btn': (80, 365),
        'ip_range_check': (88, 404, 3, 3),
        'ip_range_pix': (114, 191, 68),
        'range_string_btn': (300, 766),
        'board_btn': (98, 448),
        'board_check': (213, 229, 3, 3),
        'board_pix': (251, 204, 204),
        'board_string_btn': (401, 445),
        'build_tree_btn': (90, 486),
        'build_tree_check': (694, 954, 3, 3),
        'build_tree_pix': (0, 130, 202),
        'pot_size_btn': (397, 374),
        'stack_size_btn': (397, 428),
        'profile_base_btn': (360, 761),
        'profile_offset': 21,
        'build_confirm_btn': (687, 960),
        'build_ok_btn': (796, 891),
        'run_solver_btn': (90, 529),
        'run_confirm_btn': (488, 600),
        'size_count_offset': 29,
        'node1_btn': (49, 112),
        'node2_base_btn': (246, 112),
        'node3_base_btn': (433, 112),
        'node3_base_check': (418, 110, 3, 3),
        'node3_base_pix': (0, 174, 239),
        'node4_base_check': (606, 110, 3, 3),
        'node4_base_pix': (0, 174, 239),
        'run_solver_font': (386, 609, 79, 19),
    }

cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
suits = ['h', 'c', 'd', 's']

profiles = [
    'turn',
    'river',
    '3bet',
]
profile_options = {
    'turn_fx': ['150.0', '75.0'],
    'turn_fb': ['75.0', '0.0'],
    'river_fx': ['200.0', '100', '50.0'],
    'river_fb': ['75.0', '0.0'],
    '3bet_fx': ['66.7'],
    '3bet_fb': ['66.7', '0.0'],
}

class Solver:
    def __init__(self, id, handle, title, x, y):
        self.id = id
        self.handle = handle
        self.title = title
        self.x = x
        self.y = y
        self.offset = 0
        self.profile = 'default'
        self.status = 'empty'
        self.options = []
        self.queue = []

    def set_offset(self, total_actions):
        self.offset = (total_actions - 2) * locs['size_count_offset']

    def absolute(self, location):
        '''
        Takes a position tuple relative to this solver.
        Returns the corresponding absolute postion tuple.
        '''
        new_x = location[0] + self.x
        new_y = location[1] + self.y
        remaining_pos = [location[i] for i in range(2, len(location))]

        return tuple([new_x, new_y] + remaining_pos)


    def select_element(self, button, area, pixel, inverse=False):
        '''
        Clicks the button at the given location relative to this solver, screenshots the given area and repeats until
        the pixel in position (1, 1) on the screenshot is equal to the given pixel RGB value.
        '''
        while True:
            auto.click(self.absolute(button))
            check = auto.screenshot(region=(self.absolute(area)))
            if ((not inverse and check.getpixel((1, 1)) == pixel) or
                (inverse and check.getpixel((1, 1)) != pixel)):
                break

    def create_solve(self, oop_range, ip_range, board, pot_size, stack_size, tree_profile):

        def enter_range(inp_range):
            auto.click(self.absolute(locs['range_string_btn']))
            pyperclip.copy(inp_range.range_to_string())
            auto.keyDown('ctrl')
            auto.press('v')
            auto.keyUp('ctrl')
            auto.press('enter')
            
        self.reset()

        # Enter Ranges
        #select_element(locs['oop_range_btn'], locs['oop_range_check'], locs['oop_range_pix'], n)
        auto.click(self.absolute(locs['oop_range_btn']))
        enter_range(oop_range)
        #select_element(locs['ip_range_btn'], locs['ip_range_check'], locs['ip_range_pix'], n)
        auto.click(self.absolute(locs['ip_range_btn']))
        enter_range(ip_range)

        # Enter Board
        #select_element(locs['board_btn'], locs['board_check'], locs['board_pix'], n)
        auto.click(self.absolute(locs['board_btn']))
        auto.click(self.absolute(locs['board_string_btn']))
        pyperclip.copy(board)
        auto.keyDown('ctrl')
        auto.press('v')
        auto.keyUp('ctrl')
        auto.press('enter')

        # Build Tree
        #select_element(locs['build_tree_btn'], locs['build_tree_check'], locs['build_tree_pix'], n)
        auto.click(self.absolute(locs['build_tree_btn']))
        auto.click(self.absolute(locs['pot_size_btn']))
        pyperclip.copy(pot_size)
        auto.keyDown('ctrl')
        auto.press('v')
        auto.keyUp('ctrl')
        auto.click(self.absolute(locs['stack_size_btn']))
        pyperclip.copy(stack_size)
        auto.keyDown('ctrl')
        auto.press('v')
        auto.keyUp('ctrl')
        auto.doubleClick(self.absolute((locs['profile_base_btn'][0],
            locs['profile_base_btn'][1] + profiles.index(tree_profile) * locs['profile_offset'])))
        auto.click(self.absolute(locs['build_confirm_btn']))
        self.profile = tree_profile
        self.offset = (len(profile_options[tree_profile + '_fx']) - 1) * locs['size_count_offset']
        auto.click(self.absolute((locs['build_ok_btn'][0], locs['build_ok_btn'][1] + self.offset)))

        #Run Solver
        auto.click(self.absolute((locs['run_solver_btn'][0], locs['run_solver_btn'][1] + self.offset)))
        auto.click(self.absolute((locs['run_confirm_btn'][0], locs['run_confirm_btn'][1] + self.offset)))
        self.status = 'solving'
    
    def done_solving(self):
        img = auto.screenshot(region=self.absolute(locs['run_solver_font']))
        img = ImageOps.grayscale(img)
        img = ImageOps.invert(img)
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(2)
        img.save('img_debug/run_solver.png')

        text = pytesseract.image_to_string(img, config='--psm 7')

        if text == 'Run solver':
            self.status = 'ready'
            return True
        return False

    def get_ranges(self, oop, facing, action):
        self.select_element(locs['node1_btn'], locs['node3_base_check'], locs['node3_base_pix'], inverse=True)
        options_fx = profile_options[self.profile + '_fx']
        options_fb = profile_options[self.profile + '_fb']
        ranges = []

        if facing == 'fx':
            if not oop:
                self.select_element(
                    (locs['node2_base_btn'][0],
                    locs['node2_base_btn'][1] + len(options_fx) * locs['size_count_offset']),
                    locs['node3_base_check'],
                    locs['node3_base_pix']
                )
            
            if action:
                ranges = db.raw_data_to_range(
                    db.get_raw_data(None, None, (self.x, self.y)),
                    options_fx.index(action) + 1 if action in options_fx else len(options_fx) + 1,
                    len(options_fx) + 1
                )
            else:
                ranges = [
                    (
                        db.raw_data_to_range(db.get_raw_data(None, None, (self.x, self.y)), i, len(options_fx) + 1),
                        options_fx[i - 1]
                    )
                    for i in range(1, len(options_fx) + 1)
                ]

        elif util.is_number(facing):
            if oop:
                self.select_element(
                    (locs['node2_base_btn'][0],
                    locs['node2_base_btn'][1] + len(options_fx) * locs['size_count_offset']),
                    locs['node3_base_check'],
                    locs['node3_base_pix']
                )
                self.select_element(
                    (locs['node3_base_btn'][0],
                    locs['node3_base_btn'][1] + options_fx.index(facing) * locs['size_count_offset']),
                    locs['node4_base_check'],
                    locs['node4_base_pix']
                )
            else:
                self.select_element(
                    (locs['node2_base_btn'][0],
                    locs['node2_base_btn'][1] + options_fx.index(facing) * locs['size_count_offset']),
                    locs['node3_base_check'],
                    locs['node3_base_pix']
                )
            if action:
                ranges = db.raw_data_to_range(
                    db.get_raw_data(None, None, (self.x, self.y)),
                    options_fb.index(action) + 1,
                    len(options_fb) + 1
                )
            else:
                ranges = [(db.raw_data_to_range(db.get_raw_data(None, None, (self.x, self.y)), i, len(options_fb) + 1), options_fb[i - 1])
                    for i in range(1, len(options_fb) + 1)]

        return ranges

    def reset(self):
        win32gui.SetForegroundWindow(self.handle)

        auto.keyDown('ctrl')
        auto.press('n')
        auto.keyUp('ctrl')
        auto.press('n')

        self.status = 'empty'
        self.profile = 'default'
        self.options = []

r'''
solvers = [Solver(0, window[0], window[1], window[2][0], window[2][1])
    for window in get_window_list() if 'Untitled - GTO' in window[1]]

solvers[0].create_solve(
        pkr_range.PkrRange(db.base_dir + r'\pre\lj\uni\rfi.txt'),
        pkr_range.PkrRange(db.base_dir + r'\pre\hj\uni\rfi.txt'),
       'AcJs4d2s', '20', '75', 'turn'
)


while not solvers[0].done_solving():
    time.sleep(0.1)


range_list = solvers[0].get_ranges(True, 'fx', None)
pyperclip.copy(range_list[0][0].range_to_string())
'''