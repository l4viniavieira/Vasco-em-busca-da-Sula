import pygame

class Texto:
    def __init__(self, tela, texto, x, y, cor=(255, 255, 255), tamanho=24):
        self.tela = tela
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.fonte = pygame.font.SysFont("arial", tamanho, bold=True)

    def atualizarTexto(self, novo_texto):
        self.texto = novo_texto

    def desenhar(self):
        superficie = self.fonte.render(self.texto, True, self.cor)
        self.tela.blit(superficie, (self.x, self.y))