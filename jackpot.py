from random import randint
import pygame

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
red2 = (200, 0, 0)
green = (0, 255, 0)
green2 = (0, 200, 0)



class Paddle:
    def __init__(self, number):
        paddle_dict = {
            1: "*",
            2: "J",
            3: "A",
            4: "C",
            5: "K",
            6: "P",
            7: "O",
            8: "T",
            9: "*",
        }
        self.number = number
        self.letter = paddle_dict[self.number]
        # True means the number is showing
        self.state = True

    def flip(self):
        if self.state:
            self.state = False

    def show(self):
        if self.state:
            return self.number
        else:
            return self.letter


class Game:
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
        self.paddle_list = [
            self.paddle1,
            self.paddle2,
            self.paddle3,
            self.paddle4,
            self.paddle5,
            self.paddle6,
            self.paddle7,
            self.paddle8,
            self.paddle9,
        ]

    def get_legal_moves(self, roll):
        moves = poss_moves(roll)
        legal_moves = []
        for m in moves:
            if self.paddle_list[m - 1].state:
                legal_moves.append(m)
        return legal_moves


def roll_dice():
    """This function simulates rolling two six sided dice
    It returns a tuple of two ints """

    first_die = randint(1, 6)
    second_die = randint(1, 6)

    return (first_die, second_die)


def poss_moves(roll):
    """This function takes a tuple dice roll and returns a list of possible paddles that can be flipped"""
    if roll[0] + roll[1] > 9:
        return [roll[0], roll[1]]
    else:
        return [roll[0], roll[1], roll[0] + roll[1]]


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, gameDisplay, action=None, act_args=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        # print(f"Click 0: {click[0]}")
        if click[0] == 1 and action is not None:
            action(act_args)
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font(None, 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


