import pygame

# The World class is responsible for creating and displaying the game's world elements based on a provided data structure.
# Each element (tile, platform, enemy, etc.) in the game world is loaded, positioned, and displayed on the screen.
class World():

    # Initializes the World instance by creating tiles and interactive objects based on the input data.
    def __init__(self, data):

        from enemy import Enemy
        from platformer import tile_size, blob_group, platform_group, water_group, coin_group, exit_group
        from coin import Coin
        from exit import Exit
        from water import Water
        from platform import Platform

        self.tile_list = []

        # load images
        stone_img = pygame.image.load('images/sandCenter.png')
        ground_img = pygame.image.load('images/sandMid.png')
        half_platform = pygame.image.load('images/sandHalf_mid.png')

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
                    lava = Water(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    water_group.add(lava)
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
        from platformer import screen
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
