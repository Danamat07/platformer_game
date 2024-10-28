import pygame

# The Coin class represents a collectible item in the game.
# When the player collides with a Coin sprite, it can be collected to increase the player's score or for other purposes.
# This class inherits from pygame's Sprite class, enabling it to be included in sprite groups for collision detection.
class Coin(pygame.sprite.Sprite):

    # Initializes the Coin sprite with its image and position on the screen.
    def __init__(self, x, y):

        from platformer import tile_size

        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/star.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
