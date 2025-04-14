import pygame

# Start pygame
pygame.init()

# Screen Settings
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RogueLike game")

# Colors
BLUE = (135, 205, 250)
WHITE = (255, 255, 255)
GREEN = (35, 140, 35)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

# Player Settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 70
GRAVITY = 1
JUMP_STRENGHT = 15
SPEED = 3

# Enemy Settings
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 30
ENEMY_SPEED = 2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - PLAYER_HEIGHT)
        self.vel_y = 0
        self.on_ground = False

    def update(self, keys):
        # Horizontal movements
        if keys[pygame.K_LEFT]:
            self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += SPEED

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # reset on_ground flag
        self.on_ground = False

        # Platform collision
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                if self.rect.bottom <= platform.rect.top + 25:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Prevent falling below the screen
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_STRENGHT

    def reset_position(self):
        self.rect.center = (WIDTH // 2, HEIGHT - PLAYER_HEIGHT)
        self.vel_y = 0
        self.on_ground = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1  # 1 means moving right, -1 means moving left

    def update(self, *args):
        # Move enemy
        self.rect.x += ENEMY_SPEED * self.direction

        # if hits the wall
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

class Enemy02(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT + 40))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.direction = 1

    def update(self, *args):
        self.rect.x += ENEMY_SPEED * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Reset on_ground flag
        self.on_ground = False

        # Platform collision
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                if self.rect.bottom <= platform.rect.top + 25:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Prevent falling below the screen
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

# Create player
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create platform
platforms = pygame.sprite.Group()
platform_list = [
    Platform(200, 500, 200, 30),
    Platform(500, 450, 200, 30),
    Platform(300, 350, 150, 30)
]
platforms.add(platform_list)
all_sprites.add(platform_list)

# Create enemies
enemy = Enemy(300, 400)
enemy02 = Enemy02(100,200)
all_sprites.add(enemy, enemy02)

# Clock for frame rate
clock = pygame.time.Clock()

# Main Loop
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites with keys
    all_sprites.update(keys)

    # check collision player X enemies
    if pygame.sprite.collide_rect(player, enemy) or pygame.sprite.collide_rect(player, enemy02):
        player.reset_position()

    # Fill background
    SCREEN.fill(BLUE)

    # Draw all sprites
    all_sprites.draw(SCREEN)

    pygame.display.flip()

    # Frame Rate
    clock.tick(60)

# Quit Game
pygame.quit()