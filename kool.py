################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Platformer mäng
#
#
# Autorid: Taavi Vähi, Liisi Koitjärv
#
# mõningane eeskuju: Donkey Kong (1981)
#
# Lisakommentaar (nt käivitusjuhend): 
#
##################################################

#väärtused jms
import pygame
import sys

init()

clock = time.Clock()
fps = 60

ekraani_laius, ekraani_korgus = display.Info().current_w, display.Info().current_h
ekraan = display.set_mode((ekraani_laius, ekraani_korgus), FULLSCREEN)
display.set_caption('Kool')

ruudu_suurus = 50
mang_labi = 0
level = 1
main_menu = True
roosa = (255, 0, 125)
sinine = (0, 0, 255)
roheline = (0, 128, 0)
punane = (255, 0, 0)

font = font.SysFont('arial', 50)
voit_font = font.SysFont('Times New Roman', 200)
taimer_font = font.SysFont('Times New Roman', 50)

lopp_img = pygame.image.load('lopp.png')
auto_img = pygame.image.load('auto.png')
ratas_img = pygame.image.load('ratas.png')
jaa_img = pygame.image.load('jaa.png')
orav_img = pygame.image.load('orav.png')
kopter_img = pygame.image.load('kopter.png')



#muusika ja heli
mixer.music.load('muuuusika')
mixer.music.play(-1, 0.0, 5000)
jump_sound = mixer.Sound('hüpeee')
jump_sound.set_volume(0.5)
surm_sound = mixer.Sound('surmmmmm')
surm_sound.set_volume(0.5)
win_sound = mixer.Sound('võittttttt')
win_sound.set_volume(0.5)



#taimer
minutid = 0
sekundid = 0
m_sekundid = 0

def joonista_tekst(tekst, font, värv, x, y):
    img = font.render(tekst, True, värv)
    ekraan.blit(img, (x, y))
    
def level_uuesti(level):
    player.reset(50, ekraani_korgus - 130)
    return world

class Auto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = auto_img
        self.image = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 0.5
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Orav(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = orav_img
        self.image = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 0.5
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        
class Jaa(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = jaa_img
        self.image = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Ratas(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = ratas_img
        self.image = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 0.5
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        
class Kopter(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = kopter_img
        self.image = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 0.5
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
            
auto_grupp = pygame.sprite.Group()
orav_grupp = pygame.sprite.Group()
jaa_grupp = pygame.sprite.Group()
ratas_grupp = pygame.sprite.Group()
kopter_grupp = pygame.sprite.Group()




class Player():
    def __init__(self, x, y):
        self.reset(x, y)
        
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        #jnejne
        #lisa ka self.speed muutuja
        
    def update(self, mang_labi):
        dx = 0
        dy = 0
        walk_cooldown = 5
        
        if mang_labi == 0:
            key = key.get_pressed()
            if key[K_SPACE] or key[K_w] and self.jumperd == False:
                jump_sound.play()
                self.vel_y = -15
                self.jumped = True
            if key[K_SPACE] == False and key[K_w] == False:
                self.jumped = False
            if key[K_a]:
                dx -=5
                self.counter += 1
                self.direction = -1
            if key[K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[K_a] == False and key[K_d] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            #koodi veel
            #for loop
            
            if pygame.sprite.spritecollide(self, auto_group, False):
                mang_labi = 2
                surm_sound.play()
            if pygame.sprite.spritecollide(self, orav_grupp, False):
                mang_labi = 2
                surm_sound.play()
            if pygame.sprite.spritecollide(self, kopter_grupp, False):
                mang_labi = 2
                surm_sound.play()
            if pygame.sprite.spritecollide(self, jaa_grupp, False) and self.jumped = True:
                #tegelane nö kukub
                self.rect.angle = 90
                mang_labi = 2
                surm_sound.play()
            if pygame.sprite.spritecollide(self, jaa_grupp, False):
                self.speed *= 1.5
                jump_sound.play()
