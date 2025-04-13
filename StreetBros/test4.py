import pygame
import sys
import random
pygame.init()
pygame.display.set_caption("StreetBros - Oskar Kopač, R2C")

length = 1280
width = 720
screen = pygame.display.set_mode((length, width))
clock = pygame.time.Clock()
center = screen.get_rect().center
# Stanja igre
Borba = True
Menu = False
frame_counter = 0 
game_over = False  # Novo stanje za konec igre
winner = None  # Shrani zmagovalca

udar1 = pygame.transform.scale(pygame.image.load("efekti\\udar1.png"), (100, 100)),
udar2 = pygame.transform.scale(pygame.image.load("efekti\\udar1.png"), (100, 100)),
udar3 = pygame.transform.scale(pygame.image.load("efekti\\udar1.png"), (100, 100))

KO = pygame.transform.scale(pygame.image.load("efekti\KO.png"), (300,300))
game_over_bg = pygame.transform.scale(pygame.image.load("efekti\game_over.jpg"), (1280,720))
pritisni_enter = pygame.transform.scale(pygame.image.load("efekti\pritisni_enter.png"), (300,200))

def izberi_mapo():
    global NightCity, Forest_Map
    pygame.mixer.music.load("music\lobby.mp3")  
    pygame.mixer.music.set_volume(0.5) 
    pygame.mixer.music.play()
    

    while True:
        screen.blit(pritisni_enter, (0, 500))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 
                
        clock.tick(60)
            
izberi_mapo()