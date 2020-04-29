from random import randint
import pygame as pg


pg.init()
black = (0, 0, 0)
white = (255, 255, 255)
red1 = (255, 0, 0)
red2 = (200, 0, 0)
red3 = (175, 0, 0)
green1 = (0, 255, 0)
green2 = (0, 200, 0)
green3 = (0, 175, 0)
blue1 = (0, 0, 255)
blue2 = (0, 0, 200)
blue3 = (0, 0, 175)

red_colors = (red1, red2, red3)
green_colors = (green1, green2, green3)
blue_colors = (blue1, blue2, blue3)
pg.font.init()
FONT = pg.font.Font(None, 72)
BW = 160
BH = int(BW / 2)

screen = pg.display.set_mode([1048, 650])
pg.display.set_caption("JackPot")


def get_dice_images():
    # die_blank = pg.Surface((60, 60))
    # die_blank.fill(pg.Color('black'))
    dice_dict = {}
    numbers = ["1", "2", "3", "4", "5", "6"]
    for n in numbers:
        dice_dict[n] = pg.image.load(f"images/die{n}.png")
    # dice_dict["0"] = die_blank
    return dice_dict


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


class Die(pg.sprite.Sprite):
    def __init__(self, x, number, y=350, height=60, width=60):
        super().__init__()

        self.number = str(number)
        self.die_images = get_dice_images()
        self.image = pg.Surface((60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        # self.image.fill(pg.Color('black'))
        self.pos = (x, y)

    # def roll(self);
    #     pass

    # def handle_event(self, event):
    #     pass


class Button(pg.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        callback,
        font,
        image_normal,
        image_hover,
        image_down,
        text="",
        text_color=(0, 0, 0),
    ):
        super().__init__()
        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover, (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))

        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)

        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        self.button_down = False
        self.callback = callback

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
        elif event.type == pg.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()  # Call the function.
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pg.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal


class ControlButton(Button):
    def __init__(
        self,
        x,
        colors,
        callback,
        y=500,
        width=BW,
        height=BH,
        font=FONT,
        text="",
        image_normal=pg.Surface((BH, BW)),
        image_hover=pg.Surface((BH, BW)),
        image_down=pg.Surface((BH, BW)),
        text_color=white,
    ):
        super().__init__(
            x,
            y,
            width,
            height,
            callback,
            font,
            image_normal,
            image_hover,
            image_down,
            text=text,
            text_color=text_color,
        )
        self.image_normal.fill(colors[0])
        self.image_hover.fill(colors[1])
        self.image_down.fill(colors[2])

        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)

        # Blit the text onto the images.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)


class Paddle(pg.sprite.Sprite):
    def __init__(
        self, x, number, callback=paddle_call, y=55, font=FONT, height=100, width=50,
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
        self.poss_moves = []

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
                if self.number in self.poss_moves:
                    self.flip()
                else:
                    self.ill_move()

    def ill_move(self):
        pass


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
        self.all_buttons = pg.sprite.Group()
        self.all_dice = pg.sprite.Group()
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
        self.die1 = Die(x=175, number=0)
        self.die2 = Die(x=50, number=0)

        self.roll_button = ControlButton(
            x=85, colors=green_colors, callback=self.roll_dice, text="Roll"
        )

        self.quit_button = ControlButton(
            x=650, colors=red_colors, callback=self.quit_game, text="Quit"
        )
        self.reset_button = ControlButton(
            x=850, colors=blue_colors, callback=self.reset_game, text="Reset"
        )

        self.all_buttons.add(self.roll_button, self.quit_button, self.reset_button)
        self.all_dice.add(self.die1, self.die2)

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def run_logic(self):
        self.all_paddles.update(self.dt)
        self.all_buttons.update(self.dt)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            for paddle in self.all_paddles:
                paddle.handle_event(event)
            for button in self.all_buttons:
                button.handle_event(event)

    def draw(self):
        self.all_paddles.draw(self.screen)
        self.all_buttons.draw(self.screen)
        self.all_dice.draw(self.screen)
        pg.display.flip()

    def quit_game(self):
        """Callback method to quit the game."""
        self.done = True

    def roll_dice(self):
        """This function simulates rolling two six sided dice
        It returns a tuple of two ints """

        d1 = randint(1, 6)
        d2 = randint(1, 6)
        self.die1.image = self.die1.die_images[str(d1)]
        self.die2.image = self.die2.die_images[str(d2)]

        for p in self.paddle_list:
            p.poss_moves = self.poss_moves(d1, d2)
        for p in self.paddle_list:
            print(f"Paddle {p.number}: state : {p.state}")
        # print(f"Possible Moves: {self.poss_moves(d1, d2)}")
        print(f"D1: {d1}")
        print(f"D2: {d2}\n")

    def reset_game(self):
        for p in self.paddle_list:
            p.state = True
            p.image = p.num_image

    def poss_moves(self, d1, d2):
        """This function takes a tuple dice roll and returns a list of possible paddles that can be flipped"""
        moves = []
        if d1 + d2 < 10:
            moves = [d1 + d2]
        if d1 == d2:
            moves.append(d1)
        else:
            moves.append(d1)
            moves.append(d2)

        # if d1 == d2:
        #     moves = [d1]
        # elif d1 + d2 < 10:
        #     moves = [d1, d2, d1 + d2]
        # else:
        #     moves = [d1, d2]
        # if d1 + d2 < 10:
        #     moves.append(d1 + d2)
        print(f"Pre Moves: {moves}")
        for m in moves:
            if not self.paddle_list[m - 1].state:
                moves.remove(m)
        for m in moves:
            if not self.paddle_list[m - 1].state:
                moves.remove(m)
        print(f"Post Moves : {moves}")
        return moves


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


if __name__ == "__main__":
    pg.init()
    Game(screen).run()
    pg.quit()
