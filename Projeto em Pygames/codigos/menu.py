import pygame
import sys
from jogo import jogo 

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BLUE = (135, 205, 250)

# Carrega imagens e redimensiona
novo_jogo_img = pygame.image.load("Sprites/bottons/NovoJogo.png").convert_alpha()
novo_jogo_img = pygame.transform.scale(novo_jogo_img, (200, 50))

sair_jogo_img = pygame.image.load("Sprites/bottons/SairJogo.png").convert_alpha()
sair_jogo_img = pygame.transform.scale(sair_jogo_img, (200, 50))

novo_jogo_rect = novo_jogo_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
sair_jogo_rect = sair_jogo_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

pygame.mixer.music.load("Sons/musicas/MenuMusica.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if novo_jogo_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    jogo()  # Chama a função jogo diretamente

                if sair_jogo_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        SCREEN.fill(BLUE)
        SCREEN.blit(novo_jogo_img, novo_jogo_rect)
        SCREEN.blit(sair_jogo_img, sair_jogo_rect)
        pygame.display.flip()