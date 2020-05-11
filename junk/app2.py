import pygame as pg 

pg.init()
screen = pg.display.set_mode((640, 480))
FONT = pg.font.Font(None, 72)
ROLL_NORMAL = pg.Surface((100, 50))
ROLL_NORMAL.fill(pg.Color(('green2')))
ROLL_HOVER = pg.Surface((100, 50))
ROLL_HOVER.fill(pg.Color(('green4')))
ROLL_DOWN = pg.Surface((100, 50))
ROLL_DOWN.fill(pg.Color(('green')))

QUIT_NORMAL = pg.Surface((100, 50))
QUIT_NORMAL.fill(pg.Color(('red')))
QUIT_HOVER = pg.Surface((100, 50))
QUIT_HOVER.fill(pg.Color(('firebrick2')))


class Button(pg.sprite.Sprite):
    """
    Button is a sprite subclass, that means it can be added to a sprite group.
    You can draw and update all sprites in a group by
    calling `group.update()` and `group.draw(screen)`.
    """

    def __init__(self, x, y, width, height, callback,
                 font=FONT, text='', text_color=(0, 0, 0),
                 image_normal=ROLL_NORMAL, image_hover=ROLL_HOVER,
                 image_down=ROLL_DOWN):
        super().__init__()
        # Scale the images to the desired size (doesn't modify the originals).
        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover, (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))

        self.image = self.image_normal  # The currently active image.
        self.rect = self.image.get_rect(topleft=(x, y))
        # To center the text rect.
        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)
        # Blit the text onto the images.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        # This function will be called when the button gets pressed.
        self.callback = callback
        self.button_down = False

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
