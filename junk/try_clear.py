import pygame

pygame.init()

screen = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, size=(32, 32), image=None):
        super(Button, self).__init__()
        if image is None:
            self.rect = pygame.Rect(pos, size)
            self.image = pygame.Surface(size)
        else:
            self.image = image
            self.rect = image.get_rect(topleft=pos)
        self.pressed = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(*mouse_pos) and mouse_clicked:
            print("BUTTON PRESSED!")
            self.kill()  # Will remove itself from all pygame groups.


image = pygame.Surface((100, 40))
image.fill((255, 0, 0))
buttons = pygame.sprite.Group()
buttons.add(Button(pos=(50, 25), image=image), Button(pos=(50, 75), image=image), Button(pos=(50, 125), image=image))

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                buttons.add(Button(pos=(50, 25), image=image))
            elif event.key == pygame.K_2:
                buttons.add(Button(pos=(50, 75), image=image))
            elif event.key == pygame.K_3:
                buttons.add(Button(pos=(50, 125), image=image))

    buttons.update()  # Calls the update method on every sprite in the group.

    screen.fill((0, 0, 0))
    buttons.draw(screen)  # Draws all sprites to the given Surface.
    pygame.display.update()