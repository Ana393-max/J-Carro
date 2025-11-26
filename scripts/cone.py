import pygame
import random

class Cone:
    def __init__(self, tela):
        self.tela = tela
        self.largura_tela = tela.get_width()
        self.velocidade = 5
        self.tamanho = [40, 60]
        
        # Posição inicial aleatória nas faixas
        self.posicao = [
            random.choice([100, 200, 300, 400]),
            -self.tamanho[1]
        ]
        
        self.rect = pygame.Rect(self.posicao, self.tamanho)
        
        # Tenta carregar imagem do cone
        try:
            self.imagem = pygame.image.load('assets/cone.png')
            self.imagem = pygame.transform.scale(self.imagem, self.tamanho)
        except:
            self.imagem = None

    def desenhar(self):
        if self.imagem:
            self.tela.blit(self.imagem, self.posicao)
        else:
            # Desenha um cone laranja
            pontos = [
                (self.posicao[0] + self.tamanho[0]//2, self.posicao[1]),
                (self.posicao[0], self.posicao[1] + self.tamanho[1]),
                (self.posicao[0] + self.tamanho[0], self.posicao[1] + self.tamanho[1])
            ]
            pygame.draw.polygon(self.tela, (255, 165, 0), pontos)
            # Base do cone
            pygame.draw.rect(self.tela, (200, 120, 0), (self.posicao[0], self.posicao[1] + self.tamanho[1] - 10, self.tamanho[0], 10))

    def atualizar(self):
        self.posicao[1] += self.velocidade
        self.rect = pygame.Rect(self.posicao, self.tamanho)
        
    def fora_da_tela(self):
        return self.posicao[1] > self.tela.get_height()
        
    def getRect(self):
        return pygame.Rect(self.posicao, self.tamanho)