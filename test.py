import gamestate
import player

game = gamestate.GameState(0, '303234', (0.02, 0.05))
game.new_hand([player.Player(100, pos) for pos in ['sb', 'bb', 'lj', 'hj', 'co', 'btn']], 4)
game.hero_hand = 'As2c'
game.print_gamestate()
game.fold()
game.next_player()
game.fold()
game.next_player()
game.bet(3.0)
game.next_player()
game.call()
game.next_player()
game.fold()
game.next_player()
game.fold()
game.add_board_cards('Ad5c2s')
game.check()
game.bet(4.0)