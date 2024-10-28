import pygame
from pygame import mixer
from levelData import level_data
from coin import Coin
from button import Button
from player import Player
from world import World

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
