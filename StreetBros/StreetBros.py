import pygame #type: ignore
import sys #type:ignore
import time
import random
pygame.init()
pygame.display.set_caption("StreetBros - Oskar Kopač, R2C")

# Setup zaslona in časa
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

udar1 = pygame.transform.scale(pygame.image.load("efekti\udar1.png"), (100, 100))
udar2 = pygame.transform.scale(pygame.image.load("efekti\udar2.png"), (100, 100))
udar3 = pygame.transform.scale(pygame.image.load("efekti\udar3.png"), (100, 100))

KO = pygame.transform.scale(pygame.image.load("efekti\KO.png"), (300,300))
game_over_bg = pygame.transform.scale(pygame.image.load("efekti\game_over.jpg"), (1280,720))
pritisni_enter = pygame.transform.scale(pygame.image.load("efekti\pritisni_enter.png"), (300,200))
game_over_icon = pygame.transform.scale(pygame.image.load("efekti\game_over_icon.png"),(500,500))
# Razred za borca

class Krogla:
    def __init__(self, x, y, smer):
        self.x = x
        self.y = y
        self.smer = smer  # 1 za desno, 0 za levo
        self.hitrost = 15
        self.slika = pygame.transform.scale(pygame.image.load("player1/special/ogenj_1.png"), (150, 150))
        
    def premik_desno(self):
        self.x += 10
    
    def premik_levo(self):
        self.x-= 10

    def posodobi(self):
        if self.smer == 1:
            self.premik_desno()
        else:
            self.premik_levo()
        
    def je_izven_zaslona(self, sirina_zaslona):
        #Preveri, če je krogla izven zaslona
        if self.x < -100 or self.x > sirina_zaslona + 100:
            return True
        return False
        
    def trk_z_igralcem(self, igralec):
        if igralec.x - 50 < self.x < igralec.x + 350 and igralec.y - 50 < self.y < igralec.y + 350:
            return True
        else:
            return False
class Strela:
    def __init__(self, x, y, smer):
        self.x = x
        self.y = y
        self.smer = smer  # 1 za desno, 0 za levo
        self.hitrost = 20  # Povečana hitrost strele
        self.slika = pygame.transform.scale(pygame.image.load("player2/strela/strela_1.png"), (150, 150))
        
    def premik_desno(self):
        self.x += 15  # Povečana hitrost premika
    
    def premik_levo(self):
        self.x -= 15  # Povečana hitrost premika

    def posodobi(self):
        if self.smer == 1:
            self.premik_desno()
        else:
            self.premik_levo()
        
    def je_izven_zaslona(self, sirina_zaslona):
        if self.x < -200 or self.x > sirina_zaslona + 200:
            return True
        return False
        
    def trk_z_igralcem(self, igralec):
        if igralec.x - 50 < self.x < igralec.x + 350 and igralec.y - 50 < self.y < igralec.y + 350 and igralec.crouch != True:
            return True
        else:
            return False
class Borec:
    def __init__(self, ime, health, avatar, Tocka_na_udarec, hitrost, pozicija, blok, udarec, tek, x, y, smer, walk, skok, hitrost_skoka, special):
        self.tek = tek
        self.ime = ime
        self.health = health
        self.max_health = health  
        self.avatar = avatar
        self.Tocka_na_udarec = Tocka_na_udarec
        self.hitrost = hitrost
        self.pozicija = pozicija
        self.blok = blok
        self.udarec = udarec
        self.smer = smer
        self.walk = walk
        self.skok = skok
        self.hitrost_skoka = 0
        self.special = special
        self.x = x
        self.y = y
        self.krogle = []  
        self.cooldown = 0  
        self.krogle = []  
        self.cooldown_krogle = 0
        self.strele = []
        self.cooldown_strela = 0
        self.hitbox = (self.x - 200, self.y-200)
        self.crouch = False
        self.udarec_animacija = False
        self.udarec_frame = 0
        self.udarec_cooldown = 0
        self.zadnji_udarec_frame = -1 
        self.score = 0
        self.udarec_animacija = False
    
    def zbij_health(self, vrednost):
        self.health -= vrednost

    def ustvari_strelo(self):
        if self.cooldown_strela <= 0:
            zacetni_x = self.x + 150 if self.smer == 1 else self.x - 50
            nova_strela = Strela(zacetni_x, self.y + 100, self.smer)
            self.strele.append(nova_strela)
            self.cooldown_strela = 100 
            return True
        return False

    def ustvari_kroglo(self):
        if self.cooldown_krogle <= 0:
            zacetni_x = self.x + 150 if self.smer == 1 else self.x - 50
            nova_krogla = Krogla(zacetni_x, self.y + 100, self.smer)
            self.krogle.append(nova_krogla)
            self.cooldown_krogle = 30  
            return True
        return False

    def posodobi_krogle(self, sirina_zaslona):
        if self.cooldown_krogle > 0:
            self.cooldown_krogle -= 1
        
        # Posodobi vse krogle -> premakne jo v njeno smer glede na smer igralca
        for krogla in self.krogle[:]:
            krogla.posodobi()
            
            
            if krogla.je_izven_zaslona(sirina_zaslona):
                self.krogle.remove(krogla)
                continue
                
            
            if krogla.trk_z_igralcem(Player2):
                Player1.special= False

                if Player2.blok == False or (Player2.blok == True and Player2.smer == Player1.smer):
                    Player2.zbij_health(10)
                else:
                    pass
                    
                self.krogle.remove(krogla)

    def posodobi_strele(self, sirina_zaslona):
        if self.cooldown_strela > 0:
            self.cooldown_strela -= 1
        
       
        for strela in self.strele[:]:
            strela.posodobi()
            
            # Preveri, če je strela izven zaslona
            if strela.je_izven_zaslona(sirina_zaslona):
                self.strele.remove(strela)
                continue
                
            # Preveri trk z nasprotnikom
            if strela.trk_z_igralcem(Player1):
                Player2.special = False
                if Player1.blok == False or (Player1.blok == True and Player1.smer == Player2.smer):
                    Player1.zbij_health(10)
                else:
                    pass
                self.strele.remove(strela)
    

    def get_rezilo_pozicija(self):
        if self.smer == 1:  # Desno
            return (self.x + 200, self.y + 100, self.x + 300, self.y + 250)  # x1, y1, x2, y2
        else:  # Levo
            return (self.x, self.y + 100, self.x + 100, self.y + 250)  # x1, y1, x2, y2



    

    def premik_levo(self):
        self.x -= 20
        
    def premik_desno(self):
        self.x += 20
    
    def poklekni(self):
        self.y += 10
        
    def blok(self):
        self.blok = True
        
    def konec_bloka(self):
        self.blok = False
        
    def hoja(self):
        self.walk = True
        
    def skoci(self):
        if not self.skok:
            self.skok = True
            self.hitrost_skoka = -15

    def udari(self, other):
        if (other.x > self.x and 30 < (other.x - self.x) < 60) or (other.x < self.x and  30 < (self.x - other.x) < 60):
            if other.blok == False or(self. smer == other.smer and other.blok == True):
                other.zbij_health()

    def preveri_border(self):
        if self.x <= -50:
            self.x = -50
        elif self.x >= length-300:
            self.x = length-300


    def preveri_health(self):
        if self.health <= 0:
                screen.blit()
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
class UdarEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.images = [udar1, udar2, udar3]
class SPECIAL:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def premik_desno(self):
        self.x += 10
        
    def premik_levo(self):
        self.x -= 10
udar_effects = []



# Naloži mape
NightCity = MAP("wp5418813-anime-pixel-art-wallpapers.png", length, 0, width, 0, "music\Seek & Destroy (Remastered).mp3")
Forest_Map = MAP("8-bit-graphics-pixels-scene-with-forest (1).jpg", length, 0, width, 0, "music\Master of Puppets (Remastered).mp3")  

# Naloži slike za igralca 1
player1_crouch_desno = pygame.transform.scale(pygame.image.load("player1/crouch/player1_crouch_desno.png"), (350, 350))
player1_crouch_levo = pygame.transform.scale(pygame.image.load("player1\crouch\player1_crough_levo.png"), (350, 350))
player1_stand_levo = pygame.transform.scale(pygame.image.load("player1/stand/player1_stand_levo.png"), (350, 350))
player1_stand_desno = pygame.transform.scale(pygame.image.load("player1/stand/player1_stand_desno.jpg"), (350, 350))
player1_walk_desno_2 = pygame.transform.scale(pygame.image.load("player1/walk-desno/player1_walk_desno_2.png"), (350, 350))
player1_walk_desno_3 = pygame.transform.scale(pygame.image.load("player1/walk-desno/player1_walk_desno_3.png"), (350, 350))
player1_blok_desno = pygame.transform.scale(pygame.image.load("player1/defend/player1_blok_desno.png"), (350, 350))
player1_blok_levo = pygame.transform.scale(pygame.image.load("player1/defend/player1_blok_levo.png"), (350, 350))
player1_walk_levo_2 = pygame.transform.scale(pygame.image.load("player1\walk-levo\player1_walk_levo_2.png"), (350, 350))
player1_walk_levo_3 = pygame.transform.scale(pygame.image.load("player1\walk-levo\player1_walk_levo_3.png"), (350, 350))
player1_fireball_desno = pygame.transform.scale(pygame.image.load("player1\special\player1_fireball_desno.png"), (350, 350))
player1_fireball_levo = pygame.transform.scale(pygame.image.load("player1\special\player1_fireball_levo.png"), (350, 350))

# Naloži slike za igralca 2
player2_crouch_levo = pygame.transform.scale(pygame.image.load("player2/crouch/player2_crouch_levo.png"), (350, 350))
player2_crouch_desno = pygame.transform.scale(pygame.image.load("player2/crouch/player2_crouch_desno.png"), (350, 350))
player2_stand_levo = pygame.transform.scale(pygame.image.load("player2/stand/player2_stand_levo.png"), (350, 350))
player2_stand_desno = pygame.transform.scale(pygame.image.load("player2/stand/player2_stand_desno.png"), (350, 350))
Player2_walk_levo_2 = pygame.transform.scale(pygame.image.load("player2\walk-levo\player1_walk_levo_2.png"), (350, 350))
Player2_walk_levo_3 = pygame.transform.scale(pygame.image.load("player2\walk-levo\player1_walk_levo_3.png"), (350, 350))
Player2_walk_levo_1 = pygame.transform.scale(pygame.image.load("player2\walk-levo\player2_walk_levo_1.png"), (350, 350))
Player2_walk_desno_1 = pygame.transform.scale(pygame.image.load("player2\walk-desno\Player2_walk_desno_1.png"), (350, 350))
Player2_walk_desno_2 = pygame.transform.scale(pygame.image.load("player2\walk-desno\Player2_walk_desno_2.png"), (350, 350))
Player2_walk_desno_3 = pygame.transform.scale(pygame.image.load("player2\walk-desno\Player2_walk_desno_3.png"), (350, 350))
player2_blok_desno = pygame.transform.scale(pygame.image.load("player2\defend\player2_blok_desno.png"), (350, 350))
player2_blok_levo = pygame.transform.scale(pygame.image.load("player2\defend\player2_blok_levo.png"), (350, 350))


player2_strela_desno = pygame.transform.scale(pygame.image.load("player2\strela\player2_strela_desno.png"), (350, 350))
player2_strela_levo = pygame.transform.scale(pygame.image.load("player2\strela\player2_strela_levo.png"), (350, 350))


p1_cl_1 = pygame.transform.scale(pygame.image.load("StreetBros/player1/attack/player1_hit_levo_1.png"), (350, 350))
p1_cl_2 = pygame.transform.scale(pygame.image.load("StreetBros/player1/attack/player1_hit_levo_2.png"), (350, 350))
p1_cl_3 = pygame.transform.scale(pygame.image.load("StreetBros/player1/attack/player1_hit_levo_3.png"), (350, 350))

p1_cd_1 = pygame.transform.scale(pygame.image.load("StreetBros/player1/attack/player1_hit_desno_1.png"), (350, 350))
p1_cd_2 = pygame.transform.scale(pygame.image.load("StreetBros/player1/attack/player1_hit_desno_2.png"), (350, 350))
p1_cd_3 = pygame.transform.scale(pygame.image.load("StreetBros/player1/attack/player1_hit_desno_3.png"), (350, 350))

player1_attack_levo = [p1_cl_1,p1_cl_2,p1_cl_3]
player1_attack_desno = [p1_cd_1,p1_cd_2,p1_cd_3]





#slike za p2 attack na blizu
p2_cd_1=pygame.transform.scale(pygame.image.load("player2\cross\player2_attack_desno_1.png"), (350, 350))
p2_cd_2=pygame.transform.scale(pygame.image.load("player2\cross\player2_attack_desno_2.png"), (350, 350))
p2_cd_3=pygame.transform.scale(pygame.image.load("player2\cross\player2_attack_desno_3.png"), (350, 350))

p2_cl_1=pygame.transform.scale(pygame.image.load("player2\cross\player2_attack_levo_1.png"), (350, 350))
p2_cl_2=pygame.transform.scale(pygame.image.load("player2\cross\player2_attack_levo_2.png"), (350, 350))
p2_cl_3=pygame.transform.scale(pygame.image.load("player2\cross\player2_attack_levo_3.png"), (350, 350))

player2_attack_desno = [p2_cd_1,p2_cd_2,p2_cd_3]
player2_attack_levo = [p2_cl_1,p2_cl_2,p2_cl_3]




strela = pygame.transform.scale(pygame.image.load("player2\strela\strela_1.png"), (150, 150))

# Seznami za animacije hoje
Player1_hoja_desno = [player1_stand_desno, player1_walk_desno_2, player1_walk_desno_3]
Player1_hoja_levo = [player1_stand_levo, player1_walk_levo_2, player1_walk_levo_3]
Player2_hoja_levo = [Player2_walk_levo_2, Player2_walk_levo_1, Player2_walk_levo_3]
Player2_hoja_desno = [Player2_walk_desno_1, Player2_walk_desno_2, Player2_walk_desno_3]

# Ustvari igralce
Player1 = Borec("Bro Num 1", 100, None, 5, 50, "Stand", False, False, False, -30, 370, 1, False, False, 0, False)
Player2 = Borec("Bro Num 2", 100, None, 5, 50, "Stand", False, False, False, 850, 370, 0, False, False, 0, False)

# Začetne pozicije za skoke
Player1_y_start = Player1.y
Player2_y_start = Player2.y

# Trenutne slike
Current_slika_1 = pygame.transform.scale(player1_stand_desno, (350,350))
Current_slika_2 = pygame.transform.scale(player2_stand_levo,(350,350))

KO = pygame.transform.scale(pygame.image.load("efekti\KO.png"), (300,300))



# Izberi mapo
izbrana_mapa = NightCity.url

krogla1 = pygame.transform.scale(pygame.image.load("player1\special\ogenj_1.png"), (150,150))
krogla2 = pygame.transform.scale(pygame.image.load("player1\special\ogenj_2.png"), (150,150))
krogle_frames = [krogla1, krogla2]


# Specialni efekti
fireball = SPECIAL(Player1.x, Player1.y)
fireball_slika = pygame.transform.scale(pygame.image.load("player1\special\ogenj_1.png"), (150,150))
Max_frames = 10
special_frames = 0

frames_krogle = []
odzadje = pygame.image.load("efekti/waitingPic.jpg")
logo = pygame.transform.scale(pygame.image.load("efekti\logo.png"),(600,600))



def izberi_mapo():
    global NightCity, Forest_Map
    pygame.mixer.music.load("music\lobby.mp3")  
    pygame.mixer.music.set_volume(0.5) 
    pygame.mixer.music.play()
    screen.blit(odzadje, (0,0))
    screen.blit(logo, logo.get_rect(center = screen.get_rect().center))
    screen.blit(pritisni_enter, (0, 500))
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()
                izbrana = random.choice([NightCity, Forest_Map])
                pygame.mixer.music.load(izbrana.sound)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                return izbrana
                
        clock.tick(60)
            

pygame.mixer.music.stop()
izbrana_mapa_ = izberi_mapo()

if izbrana_mapa_ == NightCity:
    izbrana_mapa = NightCity.url

if izbrana_mapa_ == Forest_Map:
    izbrana_mapa = Forest_Map.url




# Glavna zanka igre
pygame.mixer.music.play(-1)





def konec_igre():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("music\pixel-dreams-259187.mp3")
    pygame.mixer.music.play(-1)  # Dodano, da se glasba dejansko predvaja
    
    while True:
        screen.blit(odzadje, (0,0))
        screen.blit(game_over_icon, game_over_icon.get_rect(center = screen.get_rect().center))
        
        # Prikaz zmagovalca
    
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Ponastavitev igre
                Player1.health = Player1.max_health
                Player2.health = Player2.max_health
                Player1.x, Player1.y = -30, 370
                Player2.x, Player2.y = 850, 370
                Player1.blok = False
                Player2.blok = False
                Player1.special = False
                Player2.special = False
                Player1.krogle = []
                Player2.strele = []
                game_over = False
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load(izbrana_mapa_.sound)
                pygame.mixer.music.play(-1)
                return  # Izhod iz funkcije in nadaljevanje igre
                
        clock.tick(60)




while Borba:
    starter_x_fireball = Player1.x
    
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        
        if event.type == pygame.QUIT:
            Borba = False
        
        elif event.type == pygame.KEYDOWN:
            # Igralec 1

            if event.key == pygame.K_r:  # Udarec s tipko 'r'
                Player1.udarec_animacija = True
                Player1.udarec_frame = 0
                Player1.udarec_cooldown = 15
                Player1.zadnji_udarec_frame = -1


            if event.key == pygame.K_q and Player1.smer == 1 and Player1.blok == False: 
                Player1.special = True
                Current_slika_1 = player1_fireball_desno
                Player1.ustvari_kroglo()
              
            if event.key == pygame.K_q and Player1.smer == 0 and Player1.blok == False: 
                Player1.special = True
                Current_slika_1 = player1_fireball_levo
                Player1.ustvari_kroglo()
            Player1.posodobi_krogle(length)

            if event.key == pygame.K_p:
                Player2.udarec_animacija = True
                Player2.udarec_frame = 0
                Player2.udarec_cooldown = 15
                

            if event.key == pygame.K_w:
                Player1.skoci()

            if keys[pygame.K_e] and Player1.smer == 1:
                Current_slika_1 = player1_blok_desno
                Player1.blok = True
             
            if keys[pygame.K_e] and Player1.smer == 0:
                Current_slika_1 = player1_blok_levo
                Player1.blok = True
            
            if event.key == pygame.K_s and Player1.smer == 1:
                Player1.y += 20 
                Current_slika_1 = player1_crouch_desno
                
            if event.key == pygame.K_s and Player1.smer == 0:
                Player1.y += 20                
                Current_slika_1 = player1_crouch_levo
            
            if event.key == pygame.K_a:
                Player1.smer = 0
                Current_slika_1 = player1_stand_levo
                Player1.hoja()
                
            if event.key == pygame.K_d:
                Player1.smer = 1
                Current_slika_1 = player1_stand_desno
                Player1.hoja()

            # Igralec 2
            if event.key == pygame.K_u and Player2.smer == 1: 
                Player2.special = True
                Current_slika_2 = player2_strela_desno
                Player2.ustvari_strelo()
              
            if event.key == pygame.K_u and Player2.smer == 0: 
                Player2.special = True
                Current_slika_2 = player2_strela_levo
                Player2.ustvari_strelo()

            if event.key == pygame.K_i:
                Player2.skoci()

            if keys[pygame.K_o] and Player2.smer == 1:
                Current_slika_2 = player2_blok_desno
                Player2.blok = True
             
            if keys[pygame.K_o] and Player2.smer == 0:
                Current_slika_2 = player2_blok_levo
                Player2.blok = True

            if event.key == pygame.K_k and Player2.smer == 1:
                Player2.y += 15 
                Current_slika_2 = player2_crouch_desno
                Player2.crouch = True
                
            if event.key == pygame.K_k and Player2.smer == 0:
                Player2.y += 15                
                Current_slika_2 = player2_crouch_levo            
            if event.key == pygame.K_j:
                Player2.smer = 0
                Current_slika_2 = player2_stand_levo
                Player2.hoja()
                
            if event.key == pygame.K_l:
                Player2.smer = 1
                Current_slika_2 = player2_stand_desno
                Player2.hoja()

        # Spuščanje tipk
        elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_r:
                Player1.udarec_animacija = False
                if Player1.smer == 1:
                    Current_slika_1 = player1_stand_desno
                else:
                    Current_slika_1 = player1_stand_levo

            if event.key == pygame.K_p:
                Player2.udarec_animacija = False
                if Player2.smer == 1:
                    Current_slika_2 = player2_stand_desno
                else:
                    Current_slika_2 = player2_stand_levo
            

            # Igralec 1
            if event.key == pygame.K_q and Player1.smer == 1: 
                Current_slika_1 = player1_stand_desno
                
            if event.key == pygame.K_q and Player1.smer == 0: 
                Current_slika_1 = player1_stand_levo

            if event.key == pygame.K_s and Player1.smer == 1:
                Player1.y -= 20
                Current_slika_1 = player1_stand_desno
                Player1.walk = False
                
            if event.key == pygame.K_s and Player1.smer == 0:
                Player1.y -= 20
                Current_slika_1 = player1_stand_levo
                Player1.walk = False
            
            if event.key == pygame.K_e and Player1.smer == 1:
                Current_slika_1 = player1_stand_desno
                Player1.blok = False

            if event.key == pygame.K_e and Player1.smer == 0:
                Current_slika_1 = player1_stand_levo
                Player1.blok = False

            if event.key == pygame.K_d and Player1.smer == 0:
                Current_slika_1 = player1_stand_levo
                Player1.walk = False
                
            if event.key == pygame.K_d and Player1.smer == 1:
                Current_slika_1 = player1_stand_desno
                Player1.walk = False
            
            if event.key == pygame.K_a:
                Current_slika_1 = player1_stand_levo
                Player1.walk = False

            # Igralec 2
            if event.key == pygame.K_u and Player2.smer == 1: 
                Current_slika_2 = player2_stand_desno
                
            if event.key == pygame.K_u and Player2.smer == 0: 
                Current_slika_2 = player2_stand_levo

            if event.key == pygame.K_o and Player2.smer == 0:
                Current_slika_2 = player2_stand_levo
                Player2.blok = False

            if event.key == pygame.K_o and Player2.smer == 1:
                Current_slika_2 = player2_stand_desno
                Player2.blok = False

            if event.key == pygame.K_k and Player2.smer == 1:
                Player2.y -= 15
                Current_slika_2 = player2_stand_desno
                Player2.walk = False
                Player2.crouch = False
                
            if event.key == pygame.K_k and Player2.smer == 0:
                Player2.y -= 15
                Current_slika_2 = player2_stand_levo
                Player2.walk = False
                Player2.crouch = False
            
            if event.key == pygame.K_l and Player2.smer == 0:
                Current_slika_2 = player2_stand_levo
                Player2.walk = False
                
            if event.key == pygame.K_l and Player2.smer == 1:
                Current_slika_2 = player2_stand_desno
                Player2.walk = False
            
            if event.key == pygame.K_j:
                Current_slika_2 = player2_stand_levo
                Player2.walk = False

    Player1.posodobi_krogle(1280)
    Player2.posodobi_strele(1280)

    # Premikanje igralcev
    keys = pygame.key.get_pressed()
    if keys[pygame.K_l]:
        Player2.premik_desno()
        Player2.hoja()

    if keys[pygame.K_j]:
        Player2.premik_levo()
        Player2.hoja()

    if keys[pygame.K_d]:
        Player1.premik_desno()
        Player1.hoja()

    if keys[pygame.K_a]:
        Player1.premik_levo()
        Player1.hoja()

    # Risanje
    screen.fill("black")
    screen.blit(izbrana_mapa, (0,0))
    
    # Nariši health bare in imena
    # Health bar za Player1
    pygame.draw.rect(screen, (255,0,0), (50, 45, 300, 30))
    pygame.draw.rect(screen, (0,255,0), (50, 45, 300 * (Player1.health/Player1.max_health), 30))
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"{Player1.ime}: {Player1.health}/{Player1.max_health}", True, (255,255,255))
    screen.blit(text, (50, 10))
    
    # Health bar za Player2
    pygame.draw.rect(screen, (255,0,0), (length - 350, 45, 300, 30))
    pygame.draw.rect(screen, (0,255,0), (length - 350,45, 300 * (Player2.health/Player2.max_health), 30))
    text = font.render(f"{Player2.ime}: {Player2.health}/{Player2.max_health}", True, (255,255,255))
    screen.blit(text, (length - 350, 10))
    
    # Specialni udarci
    for krogla in Player1.krogle:
        screen.blit(krogla.slika, (krogla.x, krogla.y))
    
    for strela in Player2.strele:
        screen.blit(strela.slika, (strela.x, strela.y))
    
    # Animacija hoje za igralca 1
    if Player1.walk:
        if frame_counter % 8 == 0:  
            if Player1.smer == 1:  
                Current_slika_1 = Player1_hoja_desno[(frame_counter // 8) % len(Player1_hoja_desno)]
            else:
                Current_slika_1 = Player1_hoja_levo[(frame_counter // 8) % len(Player1_hoja_levo)]
    
    # Animacija hoje za igralca 2
    if Player2.walk:
        if frame_counter % 8 == 0:  
            if Player2.smer == 1:  
                Current_slika_2 = Player2_hoja_desno[(frame_counter // 8) % len(Player2_hoja_desno)]
            else:
                Current_slika_2 = Player2_hoja_levo[(frame_counter // 8) % len(Player2_hoja_levo)]

    # Posodobi animacijo udarca za Player2
    # V glavni zanki igre, v delu za animacijo udarca
    if Player2.udarec_animacija:
        if Player2.udarec_cooldown > 0:
            Player2.udarec_cooldown -= 1
            
            # Določimo območje rezila
            x1, y1, x2, y2 = Player2.get_rezilo_pozicija()
            
            # Preverimo trk samo v aktivnih frameih animacije (npr. 1 in 2)
            if Player2.udarec_frame in [1, 2] and Player2.zadnji_udarec_frame != Player2.udarec_frame:
                # Preverimo prekrivanje območij
                if (x1 < Player1.x + 200 and x2 > Player1.x and
                    y1 < Player1.y + 300 and y2 > Player1.y):
                    
                    # Preverimo blok
                    if not Player1.blok or (Player1.blok and Player1.smer != Player2.smer):
                        Player1.zbij_health(15)
                        udar_effects.append(UdarEffect((x1+x2)//2, (y1+y2)//2))
                        Player2.zadnji_udarec_frame = Player2.udarec_frame
            
            # Prikaz animacije
            if Player2.smer == 1:
                Current_slika_2 = player2_attack_desno[Player2.udarec_frame]
            else:
                Current_slika_2 = player2_attack_levo[Player2.udarec_frame]
            
            # Posodobimo frame
            if frame_counter % 5 == 0:
                Player2.udarec_frame = (Player2.udarec_frame + 1) % len(player2_attack_desno)
        else:
            Player2.udarec_animacija = False
            Player2.zadnji_udarec_frame = -1
            # Vrnitev v osnovno pozicijo
            if Player2.smer == 1:
                Current_slika_2 = player2_stand_desno
            else:
                Current_slika_2 = player2_stand_levo


    # Nariši igralce
    screen.blit(Current_slika_1, (Player1.x, Player1.y))
    screen.blit(Current_slika_2, (Player2.x, Player2.y))

    # Fizika skokov
    if Player1.skok:
        Player1.y += Player1.hitrost_skoka
        Player1.hitrost_skoka += 1
        
        if Player1.y >= Player1_y_start:
            Player1.y = Player1_y_start
            Player1.skok = False
            Player1.hitrost_skoka = 0

    if Player2.skok:
        Player2.y += Player2.hitrost_skoka
        Player2.hitrost_skoka += 1
        
        if Player2.y >= Player2_y_start:
            Player2.y = Player2_y_start
            Player2.skok = False
            Player2.hitrost_skoka = 0


    if Player1.udarec_animacija:
        if Player1.udarec_cooldown > 0:
            Player1.udarec_cooldown -= 1
            
            # Določimo območje udarca
            x1, y1, x2, y2 = Player1.get_rezilo_pozicija()
            
            # Preverimo trk samo v aktivnih delih animacije
            if Player1.udarec_frame in [1, 2] and Player1.zadnji_udarec_frame != Player1.udarec_frame:
                # Preverimo prekrivanje z nasprotnikom
                if (x1 < Player2.x + 200 and x2 > Player2.x and
                    y1 < Player2.y + 300 and y2 > Player2.y):
                    
                    # Preverimo blok
                    if not Player2.blok or (Player2.blok and Player2.smer != Player1.smer):
                        Player2.zbij_health(15)
                        udar_effects.append(UdarEffect((x1+x2)//2, (y1+y2)//2))
                        Player1.zadnji_udarec_frame = Player1.udarec_frame
            
            # Prikažemo pravo sliko za animacijo
            if Player1.smer == 1:
                Current_slika_1 = player1_attack_desno[Player1.udarec_frame]
            else:
                Current_slika_1 = player1_attack_levo[Player1.udarec_frame]
            
            # Posodobimo frame animacije
            if frame_counter % 5 == 0:
                Player1.udarec_frame = (Player1.udarec_frame + 1) % len(player1_attack_desno)
        else:
            Player1.udarec_animacija = False
            Player1.zadnji_udarec_frame = -1
            # Vrnitev v osnovno pozicijo
            if Player1.smer == 1:
                Current_slika_1 = player1_stand_desno
            else:
                Current_slika_1 = player1_stand_levo

    
    if game_over:
        konec_igre()
        game_over = False
        


    if Player1.health <= 0:
        game_over = True
        winner = Player2
        Player2.score += 1
        Player1.health = 0
    
    if Player2.health <= 0:
        game_over = True
        winner = Player1
        Player1.score += 1
        Player2.health = 0


    Player1.preveri_border()
    Player2.preveri_border()


    frame_counter += 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()