import pygame

class Texto:
    def __init__(self, tela, texto, x, y, cor, tamanho):
        self.tela = tela
        self.texto = texto
        self.posicao = (x, y)
        self.cor = cor
        self.tamanho = tamanho

        pygame.font.init()
        self.fonte = pygame.font.Font(None, self.tamanho)
        self.imagemTexto = self.fonte.render(self.texto, True, self.cor)

    def desenhar(self):
        self.tela.blit(self.imagemTexto, self.posicao)
    
    def atualizarTexto(self, novoTexto):
        self.texto = novoTexto
        self.imagemTexto = self.fonte.render(self.texto, True, self.cor)

class Botao:
    def __init__(self, tela, texto, x, y, largura, altura, corFundo, corTexto, tamanhoFonte=36):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.posicao = (x, y)
        self.corFundo = corFundo
        self.corTexto = corTexto
        
        # Centralizar o texto no botão
        texto_x = x + (largura // 2)
        texto_y = y + (altura // 2)
        self.texto = Texto(tela, texto, texto_x, texto_y, corTexto, tamanhoFonte)
        
        # Centralizar o texto
        texto_rect = self.texto.imagemTexto.get_rect(center=(texto_x, texto_y))
        self.texto.posicao = (texto_rect.x, texto_rect.y)

    def desenhar(self):
        rect = pygame.Rect(self.posicao[0], self.posicao[1], self.largura, self.altura)
        pygame.draw.rect(self.tela, self.corFundo, rect)
        pygame.draw.rect(self.tela, (255, 255, 255), rect, 2)
        self.texto.desenhar()

    def get_click(self):
        posicaoMouse = pygame.mouse.get_pos()
        rect = pygame.Rect(self.posicao[0], self.posicao[1], self.largura, self.altura)
        
        if rect.collidepoint(posicaoMouse) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def get_hover(self):
        posicaoMouse = pygame.mouse.get_pos()
        rect = pygame.Rect(self.posicao[0], self.posicao[1], self.largura, self.altura)
        return rect.collidepoint(posicaoMouse)