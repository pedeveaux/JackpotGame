from random import randint


class Paddle():
    def __init__(self, number):
        self.number = number
        self.state = True


class Game():
    def __init__(self):
        self.won = False
        self.paddle1 = Paddle(1)
        self.paddle2 = Paddle(2)
        self.paddle3 = Paddle(3)
        self.paddle4 = Paddle(4)
        self.paddle5 = Paddle(5)
        self.paddle6 = Paddle(6)
        self.paddle7 = Paddle(7)
        self.paddle8 = Paddle(8)
        self.paddle9 = Paddle(9)

    def get_legal_moves(self, roll):
        dice_sum = roll[0] + roll[1]
        if 


def roll_dice():
    '''This function simulates rolling two six sided dice
    It returns a tuple of two ints '''

    first_die = randint(1, 6)
    second_die = randint(1, 6)

    return (first_die, second_die)
