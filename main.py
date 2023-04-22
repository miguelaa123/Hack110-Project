import pygame
import random
from constants import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Piano Tiles")
screen.fill(WHITE)
clock = pygame.time.Clock()

# Create empty sprite group for tiles
tile_group = pygame.sprite.Group()

# Create class for tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        """Sets tile's properties."""
        super().__init__()
        self.image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        
    def update(self):
        """Function moves tile down at the set speed and removes the tile once it hits the bottom."""
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()
        
    def check_hit(self, key):
        """Function checks users input and returns True or False depending on whether the tile is in the corresponding column."""
        if key == pygame.K_LEFT and self.rect.x == 0:  # User hits left arrow and tile is in the left column
            return True
        elif key == pygame.K_DOWN and self.rect.x == TILE_WIDTH:  # User hits down arrow and tile is in the middle column
            return True
        elif key == pygame.K_RIGHT and self.rect.x == 2 * TILE_WIDTH:  # User hits right arrow and tile is in the right column
            return True
        else:
            return False


# Create function to add a new tile
def add_tile():
    color = BLACK  #random.choice([BLACK, RED])
    tile = Tile(random.randint(0, 2)*TILE_WIDTH, -TILE_HEIGHT, color)
    tile_group.add(tile)


game_over = False

# Main game loop
while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            for tile in tile_group:
                if tile.check_hit(event.key):
                    tile.kill()
                else:
                    game_over = True
    
    # Add new tile every 80 frames
    if pygame.time.get_ticks() % 80 == 0:
        add_tile()
        
    # Update sprites
    tile_group.update()
    
    # Update screen
    screen.fill(WHITE)
    tile_group.draw(screen)
    pygame.display.flip()  # Update the display, is the equivalent of update() with no args
    
    # Set game frame rate
    clock.tick(FPS)

pygame.quit()
