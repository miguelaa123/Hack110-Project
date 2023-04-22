import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Define tile dimensions
TILE_WIDTH = SCREEN_WIDTH // 3
TILE_HEIGHT = 100

# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set screen title
pygame.display.set_caption("Piano Tiles")

# Set screen background color
screen.fill(WHITE)

# Create font
font = pygame.font.Font(None, 36)

# Create clock
clock = pygame.time.Clock()

# Create empty sprite group for tiles
tile_group = pygame.sprite.Group()

# Create class for tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()
        
    def check_hit(self, key):
        if key == pygame.K_LEFT and self.rect.x == 0:
            return True
        elif key == pygame.K_DOWN and self.rect.x == TILE_WIDTH:
            return True
        elif key == pygame.K_RIGHT and self.rect.x == 2*TILE_WIDTH:
            return True
        else:
            return False

# Create function to add a new tile
def add_tile():
    color = random.choice([BLACK, RED])
    tile = Tile(random.randint(0, 2)*TILE_WIDTH, -TILE_HEIGHT, color)
    tile_group.add(tile)

# Create function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Initialize game variables
score = 0
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
                    if tile.image.get_at((1, 1)) == BLACK:
                        score += 1
                        tile.kill()
                    else:
                        game_over = True
    
    # Add new tile every 30 frames
    if pygame.time.get_ticks() % 30 == 0:
        add_tile()
        
    # Update sprites
    tile_group.update()
    
    # Update screen
    screen.fill(WHITE)
    tile_group.draw(screen)
    display_score(score)
    pygame.display.flip()
    
    # Set game frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()