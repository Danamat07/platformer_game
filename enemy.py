import pygame

# The Enemy class represents an enemy sprite in the game.
# It handles the loading, positioning, and movement of the enemy character, which moves horizontally in a back-and-forth pattern.
class Enemy(pygame.sprite.Sprite):

    # Initializes the enemy sprite with its image, starting position, and movement variables.
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    # Updates the enemy's position by moving it horizontally.
    # The method increments the x-coordinate of the rect by the move_direction value (either left or right).
    # The move_counter tracks the distance traveled in one direction and when it exceeds a threshold (30),
    # the enemy reverses direction by flipping the sign of move_direction and resetting move_counter.
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 30:
            self.move_direction *= -1
            self.move_counter *= -1
