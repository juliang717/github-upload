class Player:
    def __init__(self, stack, position, seat = None, hand_range = None):
        self.stacksize = stack
        self.position = position
        self.seat = seat
        self.hand_range = hand_range
        self.invested = 0
        self.closed = False

    def get_invested(self):
        return self.invested

    def get_position(self):
        return self.position

    def get_seat(self):
        return self.seat

    def get_range(self):
        return self.hand_range

    def set_range(self, input_range):
        self.hand_range = input_range
        
    def put_money(self, bet_amount):
        self.stacksize -= bet_amount - self.get_invested()
        self.invested += bet_amount - self.get_invested()