import pygame

# A Button class to represent a clickable button in a Pygame interface.
class Button():

    # Initializes a Button instance.
    # Sets the button's position based on the provided coordinates, initializes a rect for detecting clicks,
    # and sets the clicked status to False.
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    # Draws the button on the screen and checks if it has been clicked.
    #This method checks if the mouse cursor is over the button and whether the left mouse button has been pressed.
    # If clicked, it returns True, signaling an action has been triggered. Otherwise, it returns False.
    def draw(self):

        from platformer import screen

        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # draw button
        screen.blit(self.image, self.rect)
        return action
