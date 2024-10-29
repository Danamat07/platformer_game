import pygame

# The Platform class represents a moving platform in the game, allowing for horizontal or vertical movement.
# It inherits from pygame's Sprite class, which allows it to be added to sprite groups and benefit from pygame's collision detection.
class Platform(pygame.sprite.Sprite):

    # Initializes the platform sprite with its image, starting position, and movement parameters.
    def __init__(self, x, y, move_x, move_y):

        from platformer import tile_size

        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/sandHalf_mid.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    # Updates the platform's position based on its move_x and move_y values, alternating directions at regular intervals.
    # Moves the platform by `move_direction * move_x` horizontally and `move_direction * move_y` vertically.
    # Increments move_counter with each update. If the move_counter exceeds 30 units in either direction,
    # the platform reverses direction by flipping the sign of move_direction and resetting move_counter.
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1
