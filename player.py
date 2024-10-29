import pygame

# A Player class to represent a playable character in a Pygame platformer game.
class Player():

    # Initializes a Player instance and sets the initial position.
    # Calls the reset method to initialize images and set player properties.
    def __init__(self, x, y):
        self.reset(x, y)

    # Updates the player's position, handles inputs, animations, and collision detection.
    def update(self, game_over):

        from platformer import blob_group, game_over_fx, water_group, exit_group, platform_group, draw_text, font, blue, \
        screen_width, screen_height, screen, jump_fx, world

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
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
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
            if pygame.sprite.spritecollide(self, water_group, False):
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

            # Invisible boundaries to prevent player from leaving the screen
            if self.rect.left < 0:  # left boundary
                self.rect.left = 0
            if self.rect.right > screen_width:  # right boundary
                self.rect.right = screen_width
            if self.rect.top < 0:  # top boundary
                self.rect.top = 0
            if self.rect.bottom > screen_height:  # bottom boundary
                self.rect.bottom = screen_height

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
