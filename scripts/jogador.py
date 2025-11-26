import pygame

class Carro:
    def __init__(self, tela, x, y):
        self.tela = tela
        self.posicao = [x, y]
        self.tamanho = [60, 100]
        self.rect = pygame.Rect(self.posicao, self.tamanho)
        self.velocidade = 8
        
        # Tenta carregar imagem, senão cria um retângulo
        try:
            self.imagem = pygame.image.load('assets/carro.png')
            self.imagem = pygame.transform.scale(self.imagem, self.tamanho)
        except:
            self.imagem = None

    def desenhar(self):
        if self.imagem:
            self.tela.blit(self.imagem, self.posicao)
        else:
            # Desenha um carro retangular se não tiver imagem
            pygame.draw.rect(self.tela, (255, 0, 0), (self.posicao[0], self.posicao[1], self.tamanho[0], self.tamanho[1]))
            # Janelas do carro
            pygame.draw.rect(self.tela, (100, 100, 255), (self.posicao[0] + 5, self.posicao[1] + 5, self.tamanho[0] - 10, 20))
            pygame.draw.rect(self.tela, (100, 100, 255), (self.posicao[0] + 5, self.posicao[1] + 35, self.tamanho[0] - 10, 20))

    def atualizar(self):
        # Movimento horizontal com teclas A/D ou setas
        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and self.posicao[0] > 50:
            self.posicao[0] -= self.velocidade
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and self.posicao[0] < 400:
            self.posicao[0] += self.velocidade
            
        self.rect = pygame.Rect(self.posicao, self.tamanho)

    def getRect(self):
        return pygame.Rect(self.posicao, self.tamanho)