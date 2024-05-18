import pygame
import sys
import random

def iniciarJogo():

    x = 1280
    y = 720

    screen = pygame.display.set_mode((x,y))

    bg = pygame.image.load('./imagens/fundo_laranja.png').convert_alpha()
    bg = pygame.transform.scale(bg, (x,y))

    inimigo = pygame.image.load('./imagens/enemy_small.png').convert_alpha()
    inimigo = pygame.transform.scale(inimigo, (120,120))

    personagem = pygame.image.load('./imagens/cat_idle_small.png').convert_alpha()
    personagem = pygame.transform.scale(personagem, (300,300))
    personagem = pygame.transform.rotate(personagem, 0)
    personagemUp = pygame.image.load('./imagens/cat_up_small.png').convert_alpha()
    personagemUp = pygame.transform.scale(personagemUp, (300,300))
    personagemUp = pygame.transform.rotate(personagemUp, 0)
    personagemDown = pygame.image.load('./imagens/cat_down_small.png').convert_alpha()
    personagemDown = pygame.transform.scale(personagemDown, (300,300))
    personagemDown = pygame.transform.rotate(personagemDown, 0)

    personagemAtual = personagem

    pos_inimigo_x = 500
    pos_inimigo_y = 360

    pos_personagem_x = 200
    pos_personagem_y = 300

    rodando = True

    ultima_tecla_disparo = {}

    delay_tecla = 500  # 500 milissegundos (0.5 segundos)

    class Projetil(pygame.sprite.Sprite) :
        def __init__(self, posx, posy) :
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('./imagens/luzt.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40,40))
            self.rect = self.image.get_rect()
            self.rect.center = (posx,posy)
            self.velocidadade = -6

        def update(self) :
            self.rect.x = self.rect.x - self.velocidadade
        
    all_sprites = pygame.sprite.Group()

    def respawn():
        x = 1350
        y = random.randint(1, 640)
        return [x,y]

    while rodando:
        for event in pygame.event.get(): #fecha ao clicar em X
            if event.type == pygame.QUIT:
                rodando = False

        screen.blit(bg, (0,0)) 

        #cria background
        rel_x = x % bg.get_rect().width
        screen.blit(bg,(rel_x - bg.get_rect().width,0)) 
        if rel_x < 1280:
            screen.blit(bg, (rel_x,0))
        
        #movimento personagem
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and pos_personagem_y > -23 :
            pos_personagem_y -= velocidade_personagem
            personagemAtual = personagemUp
        elif tecla[pygame.K_DOWN] and pos_personagem_y < 490 :
            pos_personagem_y +=velocidade_personagem 
            personagemAtual = personagemDown
        elif tecla[pygame.K_RIGHT] and pos_personagem_x < 1020 :
            pos_personagem_x +=velocidade_personagem
        elif tecla[pygame.K_LEFT] and pos_personagem_x  > -10 :
            pos_personagem_x -= (velocidade_personagem + 0.5)
        else:
            personagemAtual = personagem

        # inimigo
        if pos_inimigo_x <= -40:
            pos_inimigo_x, pos_inimigo_y = respawn()

        #luz
        if tecla[pygame.K_SPACE]:
            if pygame.K_SPACE not in ultima_tecla_disparo or pygame.time.get_ticks() - ultima_tecla_disparo[pygame.K_SPACE] > delay_tecla:
                proj_luz = Projetil(pos_personagem_x +245, pos_personagem_y +129)
                all_sprites.add(proj_luz)
                #ultima_tecla_disparo[pygame.K_SPACE] = pygame.time.get_ticks()
                
        #velocidade dos movimentos
        x-=1 
        velocidade_personagem = 2
        pos_inimigo_x -=3

        #Atualização e desenho do projétil de luz
        all_sprites.update()
        all_sprites.draw(screen)

        #mostra na tela
        screen.blit(inimigo,(pos_inimigo_x, pos_inimigo_y))
        screen.blit(personagemAtual, (pos_personagem_x, pos_personagem_y))
            
        pygame.display.update()

    pygame.quit()
