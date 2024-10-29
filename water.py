import  pygame

# The Water class represents a stationary hazard in the game, which causes the player to lose if they come into contact with it.
# It inherits from pygame's Sprite class, allowing it to be used within sprite groups for collision detection.
class Water(pygame.sprite.Sprite):

    # Initializes the Water sprite with its image and position on the screen.
    def __init__(self, x, y):

        from platformer import  tile_size

        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/water.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
