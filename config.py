base_dir = r'C:\Users\Julian\Desktop\Bot\database'
legacy_dir = r'C:\Users\Julian\Desktop\Bot\legacy_boards.txt'

locs = {
    'run_solver_btn': (91, 532),
    'process_db_area': (250, 500, 677, 739),
    'select_flop_base': (1255, 235),
    'select_flop_offset': 21,
    'node1_btn': (38, 113),
    'raw_data_area': (664, 280, 745, 861),
    'raw_data_offset': (14, 14),
    'data_check': (974, 1438, 3, 3),
    'data_pix': (240, 240, 240),
    'data_popup': (788, 969),
    'menu_check': (818, 988, 3, 3),
    'menu_pix': (240, 240, 240),
    'select_all_offset': (75, 188),
    'vert_offset': 29,
    'area2': (398, 92, 470, 135),
    'area3': (584, 92, 659, 135),
    'area4': (791, 92, 848, 135),
    'node_offset': 195,
}

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
    'table_window': [(1910, 0, 1940, 2110)],
    'solver_window': (-7, 0, 1051, 2110),
    'table_area': (75, 542, 1767, 976),
    'seat': (   #(x, y, low_bound, high_bound)
        (183, 596, 0, 0),    
        (183, 164, 0, 0),
        (895, 32, 0, 0),
        (1607, 164, 0, 0),
        (1607, 596, 0, 0)
    ),
    'seat_pix': (
        (193, 203, 203),
        (193, 203, 203),
        (195, 205, 205),
        (195, 205, 205),
        (195, 205, 205)
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
        (228, 613),
        (228, 173),
        (936, 44),
        (1651, 173),
        (1651, 613)
    ),
    'cards_pix': (43, 43, 43),
    'bet_chips': (
        (302, 608),
        (358, 349),
        (1070, 217),
        (1344, 349),
        (1400, 608)
    ),
    'bet_chips_pix': None,
    'bet_chips_not_pix': (13, 52, 52),
    'bet_amount': (
        (397, 1132, 109, 35),
        (452, 874, 109, 35),
        (1166, 741, 109, 35),
        (1439, 874, 109, 35),
        (1495, 1132, 109, 35)
    ),
    'bet_option': (1143, 1920, 264, 37),
    'stack_size': (
        (188, 1225, 189, 48),
        (188, 795, 189, 48),
        (900, 663, 189, 48),
        (1614, 795, 189, 48),
        (1614, 1225, 189, 48)
    ),
    'pot_size': (997, 817, 126, 43),
    'button': ( #(x, y)
        (360, 731),
        (360, 299),
        (1072, 136),
        (1418, 299),
        (1418, 731)
    ),
    'button_pix': (
        (206, 33, 39),
        (206, 33, 39),
        (206, 33, 39),
        (206, 33, 39),
        (206, 33, 39),
    ),
    'board_ranks': (
        (599, 924, 95, 70),
        (755, 924, 95, 70),
        (912, 924, 95, 70),
        (1065, 924, 95, 70),
        (1220, 924, 95, 70),
    ),
    'board_suits': (
        (592, 518),
        (747, 518),
        (902, 518),
        (1057, 518),
        (1212, 518)
    ),
    'board_suits_pix':(
        (0, 0, 0), # Spade
        (200, 0, 0), # Heart
        (0, 138, 207), # Diamond
        (50, 160, 40), # Club
    ),
    'card_dealt': (
        (931, 399), # 3rd card
        (1088, 399), # 4th card
        (1240, 399), # 5th card
    ),
    'card_dealt_pix': (255, 255, 255),
    'active': (
        (276, 653),
        (280, 218),
        (989, 86),
        (1701, 222),
        (1701, 653)
    ),
    'active_not_pix': (13, 52, 52),
    'hero_active': (890, 956),
    'hero_active_pix': None,
    'hero_active_not_pix': (13, 52, 52),
    'hero_cards': (971, 704),
    'hero_cards_pix': (255, 255, 255),
    'hero_bet_chips': (851, 656),
    'hero_stack_size': (902, 1364, 189, 48),
    'hero_ranks': (
        (876, 1230, 70, 53),
        (974, 1230, 70, 53)
    ),
    'hero_suits': (
        (850, 785),
        (949, 785)
    ),
    'fold': (0, 0),
    'check_call': (0, 0),
    'bet_raise': (0, 0),
    'betsize': (0, 0)
}

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