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
            screen.fill(RED)  # makes screen red if a tile touches bottom of screen
            display_score(score, "Game Over", (SCREEN_WIDTH // 2 - 120), (SCREEN_HEIGHT // 2))
            pygame.display.flip()  # updates screen
            global game_over
            game_over = True  # Ends game

        
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
    tile = Tile(random.randint(0, 2) * TILE_WIDTH, -TILE_HEIGHT, color)
    tile_group.add(tile)

# Create font
font = pygame.font.Font(None, 36)

# Create function to display score
def display_score(score: int, msg: str = '', x_coord: int = 10, y_coord: int = 10):
    score_text = font.render(f"{msg} Score: {score}", True, BLACK)
    screen.blit(score_text, (x_coord, y_coord))

# Initializes game variables
game_over = False
score = 0
add_tile_rate = 110

# Main game loop
while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            no_missed_hit = False  # Assumes keypress misses a tile
            for tile in tile_group:
                if tile.check_hit(event.key):
                    no_missed_hit = True  # If it actually hit something, it will change to True to keep the game going.
                    tile.kill()
                    score += 1
                elif not no_missed_hit:
                    screen.fill(RED)  # makes screen red if user inputs wrong button
                    display_score(score, "Game Over", (SCREEN_WIDTH // 2 - 120), (SCREEN_HEIGHT // 2))
                    pygame.display.flip()  # updates screen
            game_over = not no_missed_hit  # If True, game keeps going, If False, game ends

    if score > 10:
        add_tile_rate = 100
    elif score > 20:
        add_tile_rate = 90
    elif score > 30:
        add_tile_rate = 50
    elif score > 40:
        add_tile_rate = 20
    elif score > 50:
        add_tile_rate = 10

    # Add new tile every 110 frames
    if pygame.time.get_ticks() % add_tile_rate == 0:
        add_tile()
        
    # Update sprites
    tile_group.update()

    # Checks if update method ended game/loop to end game without error
    if game_over:
        break
    
    # Update screen
    screen.fill(WHITE)
    tile_group.draw(screen)
    display_score(score)
    pygame.display.flip()  # Update the display, is the equivalent of update() with no args
    
    # Set game frame rate
    clock.tick(FPS)

pygame.quit()
