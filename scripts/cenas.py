import pygame
import random
from scripts.jogador import Carro
from scripts.cone import Cone
from scripts.interfaces import Texto, Botao

class Partida:
    def __init__(self, tela):
        self.tela = tela
        self.largura = tela.get_width()
        self.altura = tela.get_height()
        
        # Cria o carro do jogador
        self.carro = Carro(tela, self.largura//2 - 30, self.altura - 150)
        self.cones = []
        self.estado = 'partida'

        self.pontosValor = 0
        self.tempo_ultimo_cone = 0
        self.velocidade_cone = 5
        
        # Elementos de interface
        self.pontosTexto = Texto(tela, f"Pontos: {self.pontosValor}", 10, 10, (255, 255, 255), 36)
        
        # Timer para aumentar dificuldade
        self.contador_dificuldade = 0

    def atualizar(self):
        self.estado = 'partida'
        
        # Atualiza elementos do jogo
        self.carro.atualizar()
        
        # Gera novos cones
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_cone > 1500:
            self.cones.append(Cone(self.tela))
            self.tempo_ultimo_cone = tempo_atual
        
        # Atualiza cones e verifica colisões
        for cone in self.cones[:]:
            cone.atualizar()
            if cone.fora_da_tela():
                self.cones.remove(cone)
                self.pontosValor += 1
                self.pontosTexto.atualizarTexto(f"Pontos: {self.pontosValor}")
            
            # Verifica colisão com o carro
            if self.carro.getRect().colliderect(cone.getRect()):
                self.estado = "gameover"
                return self.estado
        
        # Aumenta dificuldade a cada 10 pontos
        if self.pontosValor > 0 and self.pontosValor % 10 == 0 and self.contador_dificuldade < self.pontosValor:
            self.velocidade_cone += 0.5
            for cone in self.cones:
                cone.velocidade = self.velocidade_cone
            self.contador_dificuldade = self.pontosValor
        
        # Desenha o jogo
        self.desenhar()
        
        return self.estado

    def desenhar(self):
        # Fundo da estrada
        self.tela.fill((80, 80, 80))
        
        # Desenha faixas da estrada (animadas)
        tempo = pygame.time.get_ticks() // 50
        for i in range(5):
            y_offset = tempo % 40
            for j in range(0, self.altura + 40, 40):
                pygame.draw.rect(self.tela, (255, 255, 255), 
                               (100 + i*100, j - y_offset, 10, 20))
        
        # Desenha elementos do jogo
        for cone in self.cones:
            cone.desenhar()
        self.carro.desenhar()
        self.pontosTexto.desenhar()
        
        # Desenha velocidade atual (dificuldade)
        if self.velocidade_cone > 5:
            velocidade_texto = Texto(self.tela, f"Velocidade: {self.velocidade_cone:.1f}", 
                                   self.largura - 150, 10, (255, 255, 0), 24)
            velocidade_texto.desenhar()

    def reiniciar(self):
        """Reinicia a partida para o estado inicial"""
        self.carro = Carro(self.tela, self.largura//2 - 30, self.altura - 150)
        self.cones = []
        self.pontosValor = 0
        self.tempo_ultimo_cone = 0
        self.velocidade_cone = 5
        self.contador_dificuldade = 0
        self.pontosTexto.atualizarTexto(f"Pontos: {self.pontosValor}")

class Menu:
    def __init__(self, tela):
        self.tela = tela
        self.largura = tela.get_width()
        self.altura = tela.get_height()
        
        self.estado = "menu"
        
        # Elementos de interface do menu
        self.titulo = Texto(tela, "DESVIE DOS CONES!", 
                          self.largura//2, 150, (255, 255, 255), 64)
        self.titulo.posicao = (self.largura//2 - self.titulo.imagemTexto.get_width()//2, 150)
        
        self.botao_jogar = Botao(tela, "INICIAR JOGO", 
                               self.largura//2 - 100, 250, 200, 50, 
                               (0, 200, 0), (255, 255, 255), 36)
        
        self.instrucoes = Texto(tela, "Use SETAS ← → ou A/D para mover o carro", 
                              self.largura//2, 350, (200, 200, 200), 28)
        self.instrucoes.posicao = (self.largura//2 - self.instrucoes.imagemTexto.get_width()//2, 350)
        
        self.record = Texto(tela, "Melhor Pontuação: 0", 
                          self.largura//2, 420, (255, 255, 0), 32)
        self.record.posicao = (self.largura//2 - self.record.imagemTexto.get_width()//2, 420)
        
        # Sistema de recorde
        self.melhor_pontuacao = 0

    def atualizar(self):
        self.estado = "menu"
        
        # Verifica clique no botão
        if self.botao_jogar.get_click():
            self.estado = "partida"
        
        # Efeito hover no botão
        cor_original = (0, 200, 0)
        cor_hover = (0, 230, 0)
        self.botao_jogar.corFundo = cor_hover if self.botao_jogar.get_hover() else cor_original
        
        # Desenha o menu
        self.desenhar()
        
        return self.estado

    def desenhar(self):
        # Fundo do menu
        self.tela.fill((30, 30, 60))
        
        # Desenha elementos do menu
        self.titulo.desenhar()
        self.botao_jogar.desenhar()
        self.instrucoes.desenhar()
        self.record.desenhar()
        
        # Desenha um carro decorativo
        carro_decorativo = Carro(self.tela, self.largura//2 - 30, 500)
        carro_decorativo.desenhar()

    def atualizar_record(self, pontuacao):
        """Atualiza a melhor pontuação se necessário"""
        if pontuacao > self.melhor_pontuacao:
            self.melhor_pontuacao = pontuacao
            self.record.atualizarTexto(f"Melhor Pontuação: {self.melhor_pontuacao}")
            self.record.posicao = (self.largura//2 - self.record.imagemTexto.get_width()//2, 420)

class GameOver:
    def __init__(self, tela, pontuacao_final):
        self.tela = tela
        self.largura = tela.get_width()
        self.altura = tela.get_height()
        self.pontuacao_final = pontuacao_final
        
        self.estado = "gameover"
        
        # Elementos de interface do game over
        self.titulo = Texto(tela, "GAME OVER", 
                          self.largura//2, 150, (255, 0, 0), 72)
        self.titulo.posicao = (self.largura//2 - self.titulo.imagemTexto.get_width()//2, 150)
        
        self.pontuacao_texto = Texto(tela, f"Pontuação: {self.pontuacao_final}", 
                                   self.largura//2, 250, (255, 255, 255), 48)
        self.pontuacao_texto.posicao = (self.largura//2 - self.pontuacao_texto.imagemTexto.get_width()//2, 250)
        
        self.botao_reiniciar = Botao(tela, "JOGAR NOVAMENTE", 
                                   self.largura//2 - 120, 350, 240, 50, 
                                   (200, 0, 0), (255, 255, 255), 36)
        
        self.botao_menu = Botao(tela, "VOLTAR AO MENU", 
                              self.largura//2 - 100, 420, 200, 50, 
                              (0, 100, 200), (255, 255, 255), 36)
        
        self.instrucoes = Texto(tela, "Ou pressione R para reiniciar", 
                              self.largura//2, 500, (200, 200, 200), 24)
        self.instrucoes.posicao = (self.largura//2 - self.instrucoes.imagemTexto.get_width()//2, 500)

    def atualizar(self):
        self.estado = "gameover"
        
        # Verifica teclas pressionadas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            self.estado = "partida"
            return self.estado
        
        # Verifica cliques nos botões
        if self.botao_reiniciar.get_click():
            self.estado = "partida"
        elif self.botao_menu.get_click():
            self.estado = "menu"
        
        # Efeitos hover nos botões
        self.botao_reiniciar.corFundo = (230, 0, 0) if self.botao_reiniciar.get_hover() else (200, 0, 0)
        self.botao_menu.corFundo = (0, 130, 230) if self.botao_menu.get_hover() else (0, 100, 200)
        
        # Desenha a tela de game over
        self.desenhar()
        
        return self.estado

    def desenhar(self):
        # Fundo escuro
        self.tela.fill((20, 20, 40))
        
        # Desenha elementos do game over
        self.titulo.desenhar()
        self.pontuacao_texto.desenhar()
        self.botao_reiniciar.desenhar()
        self.botao_menu.desenhar()
        self.instrucoes.desenhar()