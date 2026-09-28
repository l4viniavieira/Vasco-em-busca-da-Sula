import sys
import pygame
from scripts.cenas import Partida

pygame.init()

LARGURA, ALTURA = 600, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Vasco: Em Busca da Sul-Americana")

relogio = pygame.time.Clock()
cena_atual = Partida(tela)

executando = True
while executando:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                executando = False

    cena_atual.atualizar()
    pygame.display.flip()

pygame.quit()
sys.exit()                       