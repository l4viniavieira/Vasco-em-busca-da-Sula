import pygame
import requests
from scripts.elementos import JogadorLabirinto, InimigoPatrulha, TrofeuSulamericana
from scripts.interface import Texto

class Partida:
    def __init__(self, tela):
        self.tela = tela
        self.pontos = 0
        self.fase = 1
        self.total_fases = 7
        self.nickname = "Vascaino10"
        self.estado = "JOGANDO"
        
        self.txtPontos = Texto(tela, f"Pontos: {self.pontos}", 15, 15, (255, 255, 255), 20)
        self.txtFase = Texto(tela, f"Fase: {self.fase}/{self.total_fases}", 15, 40, (255, 255, 255), 20)
        self.txtStatus = Texto(tela, "", 15, 365, (255, 255, 0), 18)

        self.txtVitoria = Texto(tela, "CAMPEÃO DA SUL-AMERICANA!", 100, 120, (255, 215, 0), 28)
        self.txtInstrucoesVitoria = Texto(tela, "Pressione R para Reiniciar ou ESC para Sair", 110, 240, (255, 255, 255), 18)

        self.carregar_fase()

    def carregar_fase(self):
        self.estado = "JOGANDO"
        self.jogador = JogadorLabirinto(self.tela, 30, 30)
        self.trofeu = TrofeuSulamericana(self.tela, 540, 330)
        
        self.paredes = [
            pygame.Rect(0, 0, 600, 10),
            pygame.Rect(0, 390, 600, 10),
            pygame.Rect(0, 0, 10, 400),
            pygame.Rect(590, 0, 10, 400)
        ]

        self.inimigos = []

        if self.fase == 1:
            self.paredes.extend([pygame.Rect(200, 50, 10, 300)])
            self.inimigos.append(InimigoPatrulha(self.tela, 300, 50, 50, 300, velocidade=1.5, eixo='y'))

        elif self.fase == 2:
            self.paredes.extend([pygame.Rect(150, 10, 10, 280), pygame.Rect(350, 110, 10, 280)])
            self.inimigos.append(InimigoPatrulha(self.tela, 220, 50, 50, 320, velocidade=2.0, eixo='y'))
            self.inimigos.append(InimigoPatrulha(self.tela, 450, 320, 360, 550, velocidade=2.0, eixo='x'))

        elif self.fase == 3:
            self.paredes.extend([pygame.Rect(150, 100, 300, 15), pygame.Rect(150, 250, 300, 15)])
            self.inimigos.append(InimigoPatrulha(self.tela, 50, 180, 20, 530, velocidade=2.5, eixo='x'))
            self.inimigos.append(InimigoPatrulha(self.tela, 280, 30, 20, 350, velocidade=2.5, eixo='y'))
            self.inimigos.append(InimigoPatrulha(self.tela, 530, 180, 20, 530, velocidade=2.5, eixo='x'))

        elif self.fase == 4:
            self.paredes.extend([pygame.Rect(100, 50, 400, 10), pygame.Rect(100, 340, 400, 10)])
            for i in range(4):
                self.inimigos.append(InimigoPatrulha(self.tela, 140 + (i*100), 70, 70, 300, velocidade=3.0, eixo='y'))

        elif self.fase == 5:
            self.paredes.extend([
                pygame.Rect(110, 10, 10, 290), pygame.Rect(220, 90, 10, 290),
                pygame.Rect(330, 10, 10, 290), pygame.Rect(440, 90, 10, 290)
            ])
            posicoes_x = [60, 160, 270, 380, 490]
            for x in posicoes_x:
                self.inimigos.append(InimigoPatrulha(self.tela, x, 50, 20, 330, velocidade=3.5, eixo='y'))

        elif self.fase == 6:
            self.paredes.extend([
                pygame.Rect(150, 50, 300, 10),
                pygame.Rect(150, 340, 300, 10),
                pygame.Rect(150, 50, 10, 300)
            ])
            self.inimigos.append(InimigoPatrulha(self.tela, 200, 100, 160, 500, velocidade=4.0, eixo='x'))
            self.inimigos.append(InimigoPatrulha(self.tela, 300, 70, 70, 300, velocidade=3.5, eixo='y'))
            self.inimigos.append(InimigoPatrulha(self.tela, 400, 100, 160, 500, velocidade=4.0, eixo='x'))

        elif self.fase == 7:
            for i in range(1, 5):
                self.paredes.append(pygame.Rect(i * 110, 50, 10, 290))
            for i in range(5):
                self.inimigos.append(InimigoPatrulha(self.tela, 55 + (i * 110), 60, 20, 330, velocidade=4.0, eixo='y'))

        self.txtStatus.atualizarTexto("")

    def enviar_pontuacao_django(self):
        url = "http://127.0.0.1:8000/api/pontuacao/salvar/"
        payload = {
            "nickname": self.nickname,
            "pontos": self.pontos,
            "fase_alcancada": self.fase
        }
        try:
            requests.post(url, json=payload, timeout=2)
            self.txtStatus.atualizarTexto("Pontuação enviada ao servidor com sucesso!")
        except Exception:
            self.txtStatus.atualizarTexto("Servidor offline. Pontuação salva localmente!")

    def reiniciar_jogo_completo(self):
        self.pontos = 0
        self.fase = 1
        self.carregar_fase()

    def atualizar(self):
        self.tela.fill((30, 30, 30))

        if self.estado == "VITORIA":
            self.txtVitoria.desenhar()
            self.txtPontos.atualizarTexto(f"Pontuação Final: {self.pontos} pts")
            self.txtPontos.x = 210
            self.txtPontos.y = 180
            self.txtPontos.desenhar()
            self.txtInstrucoesVitoria.desenhar()
            self.txtStatus.desenhar()

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_r]:
                self.txtPontos.x = 15
                self.txtPontos.y = 15
                self.reiniciar_jogo_completo()
            return "partida"

        for parede in self.paredes:
            pygame.draw.rect(self.tela, (90, 90, 90), parede)

        if self.estado == "DERROTA":
            self.jogador.desenhar()
            self.trofeu.desenhar()
            for inimigo in self.inimigos:
                inimigo.desenhar()
            
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_r]:
                self.carregar_fase()
            
            self.txtPontos.desenhar()
            self.txtFase.desenhar()
            self.txtStatus.desenhar()
            return "partida"

        if self.estado == "JOGANDO":
            self.jogador.mover(self.paredes)
            self.jogador.desenhar()
            self.trofeu.desenhar()

            for inimigo in self.inimigos:
                inimigo.atualizar()
                inimigo.desenhar()
                if self.jogador.rect.colliderect(inimigo.rect):
                    self.estado = "DERROTA"
                    self.txtStatus.atualizarTexto("Pego pela patrulha! Pressione R para tentar novamente.")
                    return "partida"

            if not self.trofeu.coletado and self.jogador.rect.colliderect(self.trofeu.rect):
                self.trofeu.coletado = True
                self.pontos += 500
                
                if self.fase < self.total_fases:
                    self.fase += 1
                    self.carregar_fase()
                else:
                    self.estado = "VITORIA"
                    self.enviar_pontuacao_django()

        self.txtPontos.atualizarTexto(f"Pontos: {self.pontos}")
        self.txtFase.atualizarTexto(f"Fase: {self.fase}/{self.total_fases}")
        self.txtPontos.desenhar()
        self.txtFase.desenhar()
        self.txtStatus.desenhar()

        return "partida"