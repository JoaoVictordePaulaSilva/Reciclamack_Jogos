import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RogueLike game")

BLUE = (135, 205, 250)
WHITE = (255, 255, 255)
GREEN = (35, 140, 35)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("Arial", 40)

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 70
GRAVITY, JUMP_STRENGTH, SPEED = 1, 15, 3
ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED = 50, 30, 2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - PLAYER_HEIGHT))
        self.vel_y, self.on_ground = 0, False

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += SPEED

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                if self.rect.bottom <= platform.rect.top + 25:
                    self.rect.bottom = platform.rect.top
                    self.vel_y, self.on_ground = 0, True

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y, self.on_ground = 0, True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_STRENGTH

    def reset_position(self):
        self.rect.center = (WIDTH // 2, HEIGHT - PLAYER_HEIGHT)
        self.vel_y, self.on_ground = 0, False

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1

    def update(self, *args):
        self.rect.x += ENEMY_SPEED * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

class Enemy02(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT + 40))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y, self.on_ground = 0, False
        self.direction = 1

    def update(self, *args):
        self.rect.x += ENEMY_SPEED * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                if self.rect.bottom <= platform.rect.top + 25:
                    self.rect.bottom = platform.rect.top
                    self.vel_y, self.on_ground = 0, True
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom, self.vel_y, self.on_ground = HEIGHT, 0, True

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

clock = pygame.time.Clock()

# Menu buttons
play_button = pygame.Rect(WIDTH//2 - 100, 200, 200, 60)
quit_button = pygame.Rect(WIDTH//2 - 100, 300, 200, 60)

# Pause menu buttons
resume_button = pygame.Rect(WIDTH//2 - 100, 200, 200, 60)
mainmenu_button = pygame.Rect(WIDTH//2 - 100, 280, 200, 60)
quit_game_button = pygame.Rect(WIDTH//2 - 100, 360, 200, 60)

# States
menu_active = True
pause_active = False
running = True

while running:
    if menu_active:
        SCREEN.fill(BLUE)
        draw_text("RogueLike", FONT, BLACK, SCREEN, WIDTH//2, 100)
        pygame.draw.rect(SCREEN, GREEN, play_button)
        draw_text("Jogar", FONT, BLACK, SCREEN, WIDTH//2, 230)
        pygame.draw.rect(SCREEN, RED, quit_button)
        draw_text("Sair", FONT, BLACK, SCREEN, WIDTH//2, 330)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    menu_active = False
                    player = Player()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)
                    platforms = pygame.sprite.Group()
                    platform_list = [
                        Platform(200, 500, 200, 30),
                        Platform(500, 450, 200, 30),
                        Platform(300, 350, 150, 30)
                    ]
                    platforms.add(platform_list)
                    all_sprites.add(platform_list)
                    enemy = Enemy(300, 400)
                    enemy02 = Enemy02(100, 200)
                    all_sprites.add(enemy, enemy02)
                if quit_button.collidepoint(event.pos):
                    running = False

    elif pause_active:
        SCREEN.fill(BLUE)
        draw_text("PAUSADO", FONT, BLACK, SCREEN, WIDTH//2, 100)
        pygame.draw.rect(SCREEN, GREEN, resume_button)
        draw_text("Continuar", FONT, BLACK, SCREEN, WIDTH//2, 230)
        pygame.draw.rect(SCREEN, WHITE, mainmenu_button)
        draw_text("Menu Principal", FONT, BLACK, SCREEN, WIDTH//2, 310)
        pygame.draw.rect(SCREEN, RED, quit_game_button)
        draw_text("Sair do Jogo", FONT, BLACK, SCREEN, WIDTH//2, 390)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    pause_active = False
                if mainmenu_button.collidepoint(event.pos):
                    menu_active, pause_active = True, False
                if quit_game_button.collidepoint(event.pos):
                    running = False

    else:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_active = True

        all_sprites.update(keys)
        if pygame.sprite.collide_rect(player, enemy) or pygame.sprite.collide_rect(player, enemy02):
            player.reset_position()

        SCREEN.fill(BLUE)
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
sys.exit()
