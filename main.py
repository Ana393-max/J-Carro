import pygame
import sys
from scripts.cenas import Partida, Menu, GameOver

class Jogo:
    def __init__(self):
        pygame.init()
        self.largura = 500
        self.altura = 700
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Desvie dos Cones!")
        
        self.relogio = pygame.time.Clock()
        
        # Sistema de cenas
        self.cena_atual = "menu"
        self.menu = Menu(self.tela)
        self.partida = None
        self.game_over = None
        
        # Pontuação entre cenas
        self.pontuacao_final = 0

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Gerencia as transições entre cenas
            self.gerenciar_cenas()
            
            pygame.display.flip()
            self.relogio.tick(60)
    
    def gerenciar_cenas(self):
        if self.cena_atual == "menu":
            estado = self.menu.atualizar()
            if estado == "partida":
                self.partida = Partida(self.tela)
                self.cena_atual = "partida"
                
        elif self.cena_atual == "partida":
            estado = self.partida.atualizar()
            if estado == "gameover":
                self.pontuacao_final = self.partida.pontosValor
                self.menu.atualizar_record(self.pontuacao_final)
                self.game_over = GameOver(self.tela, self.pontuacao_final)
                self.cena_atual = "gameover"
                
        elif self.cena_atual == "gameover":
            estado = self.game_over.atualizar()
            if estado == "partida":
                self.partida.reiniciar()
                self.cena_atual = "partida"
            elif estado == "menu":
                self.cena_atual = "menu"

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()