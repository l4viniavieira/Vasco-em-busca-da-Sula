import pygame

class JogadorLabirinto:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.tamanho = (30, 30)
        self.rect = pygame.Rect(x, y, self.tamanho[0], self.tamanho[1])
        self.velocidade = 3
        try:
            self.imagem = pygame.image.load('assets/mascote.png')
            self.imagem = pygame.transform.scale(self.imagem, self.tamanho)
        except:
            self.imagem = None

    def mover(self, paredes):
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0

        if teclas[pygame.K_LEFT]:  dx = -self.velocidade
        if teclas[pygame.K_RIGHT]: dx = self.velocidade
        if teclas[pygame.K_UP]:    dy = -self.velocidade
        if teclas[pygame.K_DOWN]:  dy = self.velocidade

        # Eixo X
        self.rect.x += dx
        for parede in paredes:
            if self.rect.colliderect(parede):
                if dx > 0: self.rect.right = parede.left
                if dx < 0: self.rect.left = parede.right

        # Eixo Y
        self.rect.y += dy
        for parede in paredes:
            if self.rect.colliderect(parede):
                if dy > 0: self.rect.bottom = parede.top
                if dy < 0: self.rect.top = parede.bottom

    def desenhar(self):
        if self.imagem:
            self.tela.blit(self.imagem, self.rect)
        else:
            pygame.draw.rect(self.tela, (255, 255, 255), self.rect)


class InimigoPatrulha:
    def __init__(self, tela, x, y, p_inicio, p_fim, velocidade=2.0, eixo='y'):
        self.tela = tela
        self.tamanho = (30, 30)
        self.rect = pygame.Rect(x, y, self.tamanho[0], self.tamanho[1])
        self.velocidade = velocidade
        self.p_inicio = p_inicio
        self.p_fim = p_fim
        self.eixo = eixo
        try:
            self.imagem = pygame.image.load('assets/rival.png')
            self.imagem = pygame.transform.scale(self.imagem, self.tamanho)
        except:
            self.imagem = None

    def atualizar(self):
        if self.eixo == 'x':
            self.rect.x += self.velocidade
            if self.rect.x >= self.p_fim:
                self.rect.x = self.p_fim
                self.velocidade = -abs(self.velocidade)
            elif self.rect.x <= self.p_inicio:
                self.rect.x = self.p_inicio
                self.velocidade = abs(self.velocidade)
        else:
            self.rect.y += self.velocidade
            if self.rect.y >= self.p_fim:
                self.rect.y = self.p_fim
                self.velocidade = -abs(self.velocidade)
            elif self.rect.y <= self.p_inicio:
                self.rect.y = self.p_inicio
                self.velocidade = abs(self.velocidade)

    def desenhar(self):
        if self.imagem:
            self.tela.blit(self.imagem, self.rect)
        else:
            pygame.draw.rect(self.tela, (255, 0, 0), self.rect)


class TrofeuSulamericana:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.tamanho = (25, 35)
        self.rect = pygame.Rect(x, y, self.tamanho[0], self.tamanho[1])
        self.coletado = False
        try:
            self.imagem = pygame.image.load('assets/trofeu.png')
            self.imagem = pygame.transform.scale(self.imagem, self.tamanho)
        except:
            self.imagem = None

    def desenhar(self):
        if not self.coletado:
            if self.imagem:
                self.tela.blit(self.imagem, self.rect)
            else:
                pygame.draw.rect(self.tela, (255, 215, 0), self.rect)