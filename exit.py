import pygame

# The Exit class represents an exit point in the game, where players can finish the level or stage.
# This class inherits from pygame's Sprite class, allowing it to be part of sprite groups for efficient collision detection and rendering.
class Exit(pygame.sprite.Sprite):

    # Initializes the Exit sprite with its image and position on the screen.
    def __init__(self, x, y):

        from platformer import tile_size

        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
