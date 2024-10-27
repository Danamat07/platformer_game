import pygame
from pygame import mixer
from levelData import level_data

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# define font
font = pygame.font.SysFont('Bauhaus 93', 42)
font_score = pygame.font.SysFont('Bauhaus 93', 18)

run = True

# define game variables
tile_size = 30
game_over = 0
main_menu = True
level = 1
max_levels = 10
score = 0

# define colours
white = (255, 255, 255)
blue = (0, 90, 255)

# load images
bg_img = pygame.image.load('images/bg.png')
restart_img = pygame.image.load('images/restart_button.png')
start_img = pygame.image.load('images/start_button.png')
exit_img = pygame.image.load('images/exit_button.png')
shroomRed_left_img = pygame.image.load('images/shroomRedAltLeft.png')
shroomRed_mid_img = pygame.image.load('images/shroomRedAltMidAlt.png')
shroomRed_right_img = pygame.image.load('images/shroomRedAltRight.png')
shroomBrown_left_img = pygame.image.load('images/shroomBrownAltSpotsLeft.png')
shroomBrown_mid_img = pygame.image.load('images/shroomBrownAltSpotsMidAlt.png')
shroomBrown_right_img = pygame.image.load('images/shroomBrownAltSpotsRight.png')
stem_base_img = pygame.image.load('images/stemBaseAlt.png')
stem_vine_img = pygame.image.load('images/stemVine.png')
stem_shroom_img = pygame.image.load('images/stemShroom.png')
stem_crown_img = pygame.image.load('images/stemCrown.png')
tiny_shroom_img = pygame.image.load('images/tinyShroom_brown.png')

# load sounds
pygame.mixer.music.load('audio/music.wav')
pygame.mixer.music.play(-1, 0.0, 50000)
coin_fx = pygame.mixer.Sound('audio/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('audio/game_over.wav')
game_over_fx.set_volume(0.5)


# Draws the title of the game on the screen.
def draw_title():
    title_font = pygame.font.SysFont('Bauhaus 93', 72)  # Larger font for the title
    title_text = 'Platformer'
    draw_text(title_text, title_font, blue, (screen_width // 2) - 150, screen_height // 2 - 100)


# This function creates a surface from the text string and blits it onto the main game screen at the specified coordinates.
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Resets the game level to its initial state.
def reset_level(level):
    player.reset(60, screen_height - 78)
    blob_group.empty()      # Clear blobs
    coin_group.empty()      # Clear coins
    platform_group.empty()  # Clear platforms
    lava_group.empty()      # Clear lava
    exit_group.empty()      # Clear exit points
    if level in level_data:
        world_data = level_data[level]
    else:
        world_data = []         # Use an empty world_data if the level is not defined
    world = World(world_data)   # Create a new world based on level data
    return world                # Return the new world


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


# A Player class to represent a playable character in a Pygame platformer game.
class Player():

    # Initializes a Player instance and sets the initial position.
    # Calls the reset method to initialize images and set player properties.
    def __init__(self, x, y):
        self.reset(x, y)

    # Updates the player's position, handles inputs, animations, and collision detection.
    def update(self, game_over):
        dx = 0              # Horizontal movement delta
        dy = 0              # Vertical movement delta
        walk_cooldown = 3   # Frames to wait between walk animation updates
        col_thresh = 12     # Collision threshold for platform handling

        if game_over == 0:
            # Handle player input
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -12    # Jump height
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5     # Move left
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5     # Move right
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                # Set idle image based on direction
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Handle walk animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Apply gravity
            self.vel_y = min(self.vel_y + 1, 10)    # Limit fall speed
            dy += self.vel_y

            # Check collision with tiles
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if the player is below the ground (jumping)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if the player is above the ground (falling)
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()

            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            # check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            #check for collision with platforms
            for platform in platform_group:
                #collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    #move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        # Display game over message and apply death animation
        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER', font, blue, (screen_width // 2) - 120, screen_height // 2)
            if self.rect.y > 120:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)  # Draw player onto the screen
        return game_over

    # Resets the player's position, animation, and attributes.
    # This method initializes the player's images for animation, sets the starting position and size,
    # and resets movement and status attributes.
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'images/alien_walk{num}.png')
            img_right = pygame.transform.scale(img_right, (24, 40))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('images/ghost_dead.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


# The World class is responsible for creating and displaying the game's world elements based on a provided data structure.
# Each element (tile, platform, enemy, etc.) in the game world is loaded, positioned, and displayed on the screen.
class World():

    # Initializes the World instance by creating tiles and interactive objects based on the input data.
    def __init__(self, data):
        self.tile_list = []

        # load images
        stone_img = pygame.image.load('images/stoneCenter.png')
        ground_img = pygame.image.load('images/stoneMid.png')
        half_platform = pygame.image.load('images/stoneHalfMid.png')

        # Iterate through rows and columns in the data to create the world
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:   # Create stone tile
                    img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:   # Create ground tile
                    img = pygame.transform.scale(ground_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:   # Create enemy and add it to the blob group
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 9)
                    blob_group.add(blob)
                if tile == 4:   # Create horizontal moving platform
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:   # Create vertical moving platform
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:   # Create lava object and add to lava group
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:   # Create coin object and add to coin group
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:   # Create exit object and add to exit group
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 9:   # Create half platform tile
                    img = pygame.transform.scale(half_platform, (tile_size, tile_size // 2))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    # Draws each tile in the world on the screen.
    # This method iterates through the tile_list and blits each tile's image at its corresponding position, displaying it on the game screen.
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


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


# The Platform class represents a moving platform in the game, allowing for horizontal or vertical movement.
# It inherits from pygame's Sprite class, which allows it to be added to sprite groups and benefit from pygame's collision detection.
class Platform(pygame.sprite.Sprite):

    # Initializes the platform sprite with its image, starting position, and movement parameters.
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/stoneHalfMid.png')
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


# The Lava class represents a stationary hazard in the game, which causes the player to lose if they come into contact with it.
# It inherits from pygame's Sprite class, allowing it to be used within sprite groups for collision detection.
class Lava(pygame.sprite.Sprite):

    # Initializes the Lava sprite with its image and position on the screen.
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# The Coin class represents a collectible item in the game.
# When the player collides with a Coin sprite, it can be collected to increase the player's score or for other purposes.
# This class inherits from pygame's Sprite class, enabling it to be included in sprite groups for collision detection.
class Coin(pygame.sprite.Sprite):

    # Initializes the Coin sprite with its image and position on the screen.
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/star.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


# The Exit class represents an exit point in the game, where players can finish the level or stage.
# This class inherits from pygame's Sprite class, allowing it to be part of sprite groups for efficient collision detection and rendering.
class Exit(pygame.sprite.Sprite):

    # Initializes the Exit sprite with its image and position on the screen.
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Initialize the player character at a specified position
player = Player(60, screen_height - 78)

# Create sprite groups for different game entities
blob_group = pygame.sprite.Group()      # Group for enemy blobs
platform_group = pygame.sprite.Group()  # Group for platforms
lava_group = pygame.sprite.Group()      # Group for lava hazards
coin_group = pygame.sprite.Group()      # Group for collectible coins
exit_group = pygame.sprite.Group()      # Group for exit points

# create coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# Load world data based on the current level
if level in level_data:
    world_data = level_data[level]  # Retrieve the level data if it exists
else:
    world_data = []                 # Use an empty world_data if the level is not defined
world = World(world_data)           # Instantiate a World object with the level's data

# create buttons
restart_button = Button(screen_width // 2 - 30, screen_height // 2 + 50, restart_img)
start_button = Button(screen_width // 2 - 210, screen_height // 2 - 100, start_img)
exit_button = Button(screen_width // 2 + 90, screen_height // 2 + 50, exit_img)


# The main game loop that runs continuously until the game is exited.
while run:

    clock.tick(fps)                 # control the game's frame rate
    screen.blit(bg_img, (0, 0))     # render the background
    screen.blit(stem_base_img, (130, 525))
    screen.blit(stem_crown_img, (130, 435))
    screen.blit(stem_vine_img, (130, 475))
    screen.blit(shroomBrown_mid_img, (130, 395))
    screen.blit(shroomBrown_left_img, (60, 395))
    screen.blit(shroomBrown_right_img, (200, 395))
    screen.blit(stem_base_img, (420, 525))
    screen.blit(stem_shroom_img, (420, 455))
    screen.blit(stem_crown_img, (420, 350))
    screen.blit(stem_vine_img, (420, 385))
    screen.blit(shroomRed_mid_img, (420, 310))
    screen.blit(shroomRed_left_img, (350, 310))
    screen.blit(shroomRed_right_img, (490, 310))

    if main_menu == True:           # check if the main menu is active
        if exit_button.draw():      # check for exit button click to close the game
            run = False
        if start_button.draw():     # check for start button click to enter the game
            main_menu = False
    else:
        world.draw()                # draw the game world
        if game_over == 0:          # if the game is not over, update game elements
            blob_group.update()
            platform_group.update()
            # update score
            # check if a coin has been collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            # display the current score on the screen
            draw_text('X ' + str(score), font_score, white, tile_size - 6, 6)

        # draw game elements on the screen
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)    # update the player's state

        # check if the player has died
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

        # check if the player has completed the level
        if game_over == 1:
            # reset game and go to next level
            level += 1
            if level <= max_levels:
                # reset level data
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                # display winning message if game completed
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 84, screen_height // 2)
                if restart_button.draw():
                    level = 1
                    # reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    # handle events like quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False     # exit the game loop

    # update the display with the drawn frame
    pygame.display.update()

# clean up and exit the game
pygame.quit()
