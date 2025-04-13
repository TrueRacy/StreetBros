import pygame #type: ignore
import sys #type:ignore
import time
pygame.init()
pygame.display.set_caption("StreetBros - Oskar Kopač, R2C")
#setupamo display in čas

length = 1280
width = 720

screen = pygame.display.set_mode((length, width))
clock = pygame.time.Clock()
Borba = True
Menu = False
Nastavitve = False
frame_counter = 0 
temno_mesto = pygame.image.load("wp5418813-anime-pixel-art-wallpapers.png")


#razred borec z atributi bojevalca 
#Tocka na udarec pomeni koliko točk se zbije nasprotniku ko ga uspesno udaris
class Borec:
    def __init__(self, ime, health, avatar, Tocka_na_udarec, hitrost, pozicija, blok, udarec, tek, x, y, smer,walk, skok, hitrost_skoka):
        self.tek = tek
        self.ime = ime
        self.health = health
        self.avatar = avatar
        self.Tocka_na_udarec = Tocka_na_udarec
        self.hitrost = hitrost
        self.pozicija = pozicija #Coutch/Stand/Stand+Block/Crouch+Block/Stand+Hit/Crouch+Hit -> pove trenutno stanje igralca
        self.blok = blok #True alpa False -> zaradi animacij
        self.udarec = udarec #True alpa False -> zaradi animacij
        self.smer = smer
        self.walk = walk
        self.skok = skok
        self.hitrost_skoka = 0

        #koordinate:
        self.x = x
        self.y = y

    def zbij_health(self, Tocka_za_udarec):
        if self.health - Tocka_za_udarec >0:
            self.health -= Tocka_za_udarec
        elif self.health - Tocka_za_udarec <= 0:
            self.health = 0

    def premik_levo(self):
        self.x -= 20
    def premik_desno(self):
        self.x += 20
    
    def poklekni(self):
        self.y +=10

    def blok(self):
        self.blok = True

    def konec_bloka(self):
        self.blok = False

    def hoja(self):
        self.walk= True

    def skoci(self):
        if not self.skok:  # Skok lahko izvede le, če ni že v zraku
            self.skok = True
            self.hitrost_skoka = -15

class MAP:
    def __init__(self, picture, max_x, min_x, max_y, min_y, sound):
        self.url = pygame.image.load(picture)
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y
        self.sound = sound
    def __str__(self):
        return self.url

NightCity =  MAP("wp5418813-anime-pixel-art-wallpapers.png", length, 0, width, 0, "music\Seek & Destroy (Remastered).mp3")
Forest_Map = MAP("8-bit-graphics-pixels-scene-with-forest (1).jpg", length, 0, width, 0, "music\Master of Puppets (Remastered).mp3")  
    


#ikone pozicij playerjev glede na poticijo (player{i}_pozicija)   

player2_crouch_levo = pygame.transform.scale(pygame.image.load("player2/crouch/player2_crouch_levo.png"), (350, 350))
player2_crouch_desno = pygame.transform.scale(pygame.image.load("player2/crouch/player2_crouch_desno.png"), (350, 350))
player1_crouch_desno = pygame.transform.scale(pygame.image.load("player1/crouch/player1_crouch_desno.png"), (350, 350))
player1_crouch_levo = pygame.transform.scale(pygame.image.load("player1\crouch\player1_crough_levo.png"), (350, 350))

player2_stand_levo = pygame.transform.scale(pygame.image.load("player2/stand/player2_stand_levo.png"), (350, 350))
player2_stand_desno = pygame.transform.scale(pygame.image.load("player2/stand/player2_stand_desno.png"), (350, 350))
player1_stand_levo = pygame.transform.scale(pygame.image.load("player1/stand/player1_stand_levo.png"), (350, 350))
player1_stand_desno = pygame.transform.scale(pygame.image.load("player1/stand/player1_stand_desno.jpg"), (350, 350))

player1_walk_desno_2 = pygame.transform.scale(pygame.image.load("player1/walk-desno/player1_walk_desno_2.png"), (350, 350))
player1_walk_desno_3 = pygame.transform.scale(pygame.image.load("player1/walk-desno/player1_walk_desno_3.png"), (350, 350))

player1_blok_desno = pygame.transform.scale(pygame.image.load("player1/defend/player1_blok_desno.png"), (350, 350))
player1_blok_levo = pygame.transform.scale(pygame.image.load("player1/defend/player1_blok_levo.png"), (350, 350))


player1_walk_levo_2 = pygame.transform.scale(pygame.image.load("player1\walk-levo\player1_walk_levo_2.png"), (350, 350))
player1_walk_levo_3 = pygame.transform.scale(pygame.image.load("player1\walk-levo\player1_walk_levo_3.png"), (350, 350))


Player1_hoja_desno = [player1_stand_desno, player1_walk_desno_2, player1_walk_desno_3]
Player1_hoja_levo = [player1_stand_levo, player1_walk_levo_2, player1_walk_levo_3]


player1_pozicija = None
player2_pozicija = None

#delanje borcev (objekti)
Player1 = Borec("", 100, player1_pozicija, 5, 50, "Stand", False, False, False, -30, 370, 1, False, False,0)
Player2 = Borec("", 100, player2_pozicija, 5, 50, "Stand", False, False, False, 850, 370, 0, False, False,0)

Player1_hoja = [pygame.transform.scale(player1_stand_desno, (350, 350)),pygame.transform.scale(player1_walk_desno_2, (350,350)), pygame.transform.scale(player1_walk_desno_3,(350,350))]

Player1_y_start = Player1.y
Current_slika_1 = pygame.transform.scale(player1_stand_desno, (350,350))
Current_slika_2 = pygame.transform.scale(player2_stand_levo,(350,350))


izbrana_mapa = Forest_Map.url


while Borba:

   while Borba:

    # animacija:

    # v kakšni poziciji sta 2 igralca

    # prvi igralec:
        # premikanje levo:
            # hoja levo:

    # nastavljanje velikosti

    # setupam da se okno zapre
    for event in pygame.event.get():

        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            Borba = False
        
        
        
        elif event.type == pygame.KEYDOWN:
 #p1 -----------------------------------------------------------------           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # Skok za Player1
                    Player1.skoci()
                


            if event.key == pygame.K_s and Player1.smer == 1:
                Player1.y += 20 
                Current_slika_1 = player1_crouch_desno
            if event.key == pygame.K_s and Player1.smer == 0:
                Player1.y += 20                
                Current_slika_1 = player1_crouch_levo
            

            # obračanje P1
            
            
        if keys[pygame.K_a]:
            Player1.smer = 0
            Current_slika_1 = player1_stand_levo
            Player1.hoja()
            Player1.premik_levo()

        if keys[pygame.K_d]:
            Player1.smer = 1
            Current_slika_1 = player1_stand_desno
            Player1.hoja()
            Player1.premik_desno()



        if keys[pygame.K_e]and Player1.smer == 1:
            Current_slika_1 = player1_blok_desno

        if keys[pygame.K_e]and Player1.smer == 0:
            Current_slika_1 = player1_blok_levo
        
        
#p1 -----------------------------------------------------------------



#p2 -----------------------------------------------------------------
    

        if keys[pygame.K_i]:
            Player2.skoci()

        if keys[pygame.K_l]:
            Player2.premik_desno()
            Player2.hoja()

        if keys[pygame.K_j]:
            Player2.premik_levo()
            Player2.hoja()

            if event.key == pygame.K_k and Player2.smer == 1:
                Player2.y -= 20 
                Current_slika_2 = player2_crouch_desno

            if event.key == pygame.K_k and Player2.smer == 0:
                Player2.y -= 20 
                Current_slika_2 = player2_crouch_levo

        
        
        
        if keys[pygame.K_j]:
            Player2.smer = 0
            Current_slika_2 = player2_stand_levo
            Player2.hoja()
            Player2.premik_levo()
        if keys[pygame.K_l]:
            Player2.smer = 1
            Current_slika_2 = player2_stand_desno
            Player2.hoja()
            Player2.premik_desno()
            
            

            
            
        
#p2 -----------------------------------------------------------------
        

        # crouchi
        elif event.type == pygame.KEYUP:

#p1 -----------------------------------------------------------------

            if event.key == pygame.K_s and Player1.smer == 1:
                Player1.y -= 20
                Current_slika_1 = player1_stand_desno
                Player1.walk = False
            if event.key == pygame.K_s and Player1.smer == 0:
                Player1.y -= 20
                Current_slika_1 = player1_stand_levo
                Player1.walk = False
            
            if event.key == pygame.K_d and Player1.smer == 0:
                Current_slika_1 = player1_stand_levo
                Player1.walk = False
            if event.key == pygame.K_d and Player1.smer == 1:
                Current_slika_1 = player1_stand_desno
                Player1.walk = False

            if event.key == pygame.K_a:
                Current_slika_1 = player1_stand_levo
                Player1.walk = False

            if event.key == pygame.K_e and Player1.smer == 1:
                Current_slika_1 = player1_stand_desno

            if event.key == pygame.K_e and Player1.smer == 0:
                Current_slika_1 = player1_stand_levo


#p1 -----------------------------------------------------------------






#p2 -----------------------------------------------------------------
   
            if event.key == pygame.K_k and Player2.smer == 1:
                Player2.y += 20
                Current_slika_2 = player2_stand_desno
               
            if event.key == pygame.K_k and Player2.smer == 0:
                Player2.y += 20
                Current_slika_2 = player2_stand_levo
                



            if event.key == pygame.K_l and Player2.smer == 0:
                Current_slika_2 = player2_stand_levo
                Player2.walk = False
            if event.key == pygame.K_l and Player2.smer == 1:
                Current_slika_2 = player2_stand_desno
                Player2.walk = False
            
            if event.key == pygame.K_j:
                Current_slika_2 = player2_stand_levo
                Player2.walk = False

#p2 -----------------------------------------------------------------
   
            

            
            
            


        #premikanje

    
    
    #za jutr (player1 crouch x premikanje):
    
        #player2

    

    screen.fill("black")
    screen.blit(izbrana_mapa, (0,0))
    screen.blit(Current_slika_2, (Player2.x, Player2.y))
    
  

# V glavni while zanki:
    if Player1.walk:
        if frame_counter % 8 == 0:  # Zamenja sliko vsakih 'animation_speed' frame-ov
            if Player1.smer == 1:  # Hoja desno
                Current_slika_1 = Player1_hoja_desno[(frame_counter // 8) % len(Player1_hoja_desno)]
            else:  # Hoja levo
                Current_slika_1 = Player1_hoja_levo[(frame_counter // 8) % len(Player1_hoja_levo)]

        screen.blit(Current_slika_1, (Player1.x, Player1.y))
    else:
        screen.blit(Current_slika_1, (Player1.x, Player1.y))


    for player in [Player1, Player2]:
        if player.skok:
            player.y += player.hitrost_skoka
            player.hitrost_skoka += 1
            if player.y >= 370:
                player.y = 370
                player.skok = False
                player.hitrost_skoka = 0


    frame_counter += 1


    #naredimo tako, da se zamenja frame
    pygame.display.flip()
    #nastavimo FPS
    clock.tick(60)

pygame.quit()




#odprte nastavitve
'''
while Nastavitve == True and Menu == False and Borba == False:
    pass
pygame.quit()

#Prvi menu
while Menu == True and Nastavitve == False and Borba == False:
    pass

pygame.quit()
'''