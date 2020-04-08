
import pygame
from jackpot import Game, button, green, green2, red, red2, roll_dice


def load_images():
    images = {}
    numbers = ["1", "2", "3", "4", "5", "6"]
    for i, num in enumerate(numbers, start=1):
        # images[i] = pygame.image.load("die{}.png".format(num)).convert()
        images[i] = pygame.image.load(f"images/die{num}.png")
    return images


def show_dice(dice_images):
    # roll = roll_dice()
    # screen.blit(dice_images[roll[0]], (40, 200))
    # screen.blit(dice_images[roll[1]], (250, 200))
    screen.blit(dice_images[3], (40, 200))
    screen.blit(dice_images[5], (250, 200))


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([640, 480])
pygame.display.set_caption('JackPot')
new_game = Game()
dice_images = load_images()

game_str = ""
for p in new_game.paddle_list:
    game_str += str(p.show()) + " | "

dice_images = load_images()
# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    font = pygame.font.Font(None, 72)
    text = font.render(game_str, 1, (55, 55, 250), (125, 125, 125))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    screen.blit(text, textpos)

    # button("Roll", x=100, y=350, w=100, h=50, ic=green, ac=green2, gameDisplay=screen)

    button("Roll", x=100, y=350, w=100, h=50, ic=green, ac=green2, gameDisplay=screen, action=show_dice, act_args=dice_images)

    button("Quit", x=400, y=350, w=100, h=50, ic=red, ac=red2, gameDisplay=screen, action=pygame.QUIT)


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
