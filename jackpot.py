from random import randint
import pygame as pg

pg.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
red2 = (200, 0, 0)
green = (0, 255, 0)
green2 = (0, 200, 0)
FONT = pg.font.Font(None, 72)

screen = pg.display.set_mode([1048, 650])
pg.display.set_caption("JackPot")


def gen_num_images():
    image_list = []
    for i in range(1, 10):
        image_list.append(pg.image.load(f"images/number_{i}.png"))
    return image_list


def gen_ltr_images():
    image_dict = {}
    image_dict["*"] = pg.image.load(f"images/asterisk.png")
    for l in "jackpot":
        image_dict[l] = pg.image.load(f"images/letter_{l}.png")
    return image_dict


def paddle_call():
    pass


class Paddle(pg.sprite.Sprite):
    def __init__(
        self, x, number, callback=paddle_call, y=100, font=FONT, height=100, width=50,
    ):
        super().__init__()
        paddle_dict = {
            1: "*",
            2: "j",
            3: "a",
            4: "c",
            5: "k",
            6: "p",
            7: "o",
            8: "t",
            9: "*",
        }
        ltr_img_dict = gen_ltr_images()
        num_img_list = gen_num_images()
        self.number = number
        self.letter = paddle_dict[self.number]
        self.num_image = num_img_list[self.number - 1]
        self.ltr_image = ltr_img_dict[self.letter]
        self.image = self.num_image
        self.rect = self.image.get_rect(topleft=(x, y))
        # True means the number is showing
        self.state = True

    def flip(self):
        if self.state:
            self.image = self.ltr_image
            self.state = False
        else:
            self.image = self.num_image
            self.state = True

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.flip()


class Game:
    def __init__(self, screen):
        self.clock = pg.time.Clock()
        first_x = 25
        offset = 22
        self.screen = screen
        self.done = False
        self.won = False
        self.paddle1 = Paddle(x=first_x, number=1)
        self.paddle2 = Paddle(x=first_x + 5 * offset, number=2)
        self.paddle3 = Paddle(x=first_x + 10 * offset, number=3)
        self.paddle4 = Paddle(x=first_x + 15 * offset, number=4)
        self.paddle5 = Paddle(x=first_x + 20 * offset, number=5)
        self.paddle6 = Paddle(x=first_x + 25 * offset, number=6)
        self.paddle7 = Paddle(x=first_x + 30 * offset, number=7)
        self.paddle8 = Paddle(x=first_x + 35 * offset, number=8)
        self.paddle9 = Paddle(x=first_x + 40 * offset, number=9)
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
        self.all_paddles = pg.sprite.Group()
        # num_images = gen_num_images()
        # ltr_imgs = gen_ltr_images()

        # for idx, p in enumerate(self.paddle_list):
        #     p.letter_image = ltr_imgs[idx]
        #     p.num_image = num_images[idx]

        self.all_paddles.add(
            self.paddle1,
            self.paddle2,
            self.paddle3,
            self.paddle4,
            self.paddle5,
            self.paddle6,
            self.paddle7,
            self.paddle8,
            self.paddle9,
        )

    def get_legal_moves(self, roll):
        moves = poss_moves(roll)
        legal_moves = []
        for m in moves:
            if self.paddle_list[m - 1].state:
                legal_moves.append(m)
        return legal_moves

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def run_logic(self):
        self.all_paddles.update(self.dt)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            for paddle in self.all_paddles:
                paddle.handle_event(event)

    def draw(self):
        self.all_paddles.draw(self.screen)
        pg.display.flip()


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
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(gameDisplay, ac, (x, y, w, h))
        # print(f"Click 0: {click[0]}")
        if click[0] == 1 and action is not None:
            action(act_args)
    else:
        pg.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pg.font.Font(None, 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


class Button:
    def __init__(self, position, size):
        self._images = [
            pg.Surface(size),
            pg.Surface(size),
        ]

        self._images[0].fill(green)
        self._images[1].fill(green2)

        # get image size and position
        self._rect = pg.Rect(position, size)

        self._index = 0

    def draw(self, screen):
        # draw selected image
        screen.blit(self._images[self._index], self._rect)

    def event_handler(self, event):
        # if some mouse button is clicked
        if event.type == pg.MOUSEBUTTONDOWN:
            # if it is the left button
            if event.button == 1:
                self._index = (self.index + 1) % 2


class DiceButton(Button):
    def __init__(self, position, size, msg, dice_images):

        self._msg = msg
        self._dice_images = dice_images

        self._images = [
            pg.Surface(size),
            pg.Surface(size),
        ]

        self._images[0].fill(green)
        self._images[1].fill(green2)

        # get image size and position
        self._rect = pg.Rect(position, size)

        self._index = 0
        mouse = pg.mouse.get_pos()

        if self._rect.collidepoint(mouse):
            self._index = 1
        else:
            self._index = 0

    def event_handler(self, event, screen):
        if event.type == pg.MOUSEBUTTONDOWN:
            # if it is the left button
            if event.button == 1:
                if self._rect.collidepoint(event.pos):
                    # self._index = (self._index + 1) % 2
                    # roll = roll_dice()
                    screen.blit(self._dice_images[3], (40, 200))
                    # screen.blit(self._dice_images[roll[0]], (40, 200))
                    # screen.blit(self._dice_images[roll[1]], (250, 200))


if __name__ == "__main__":
    pg.init()
    Game(screen).run()
    pg.quit()
