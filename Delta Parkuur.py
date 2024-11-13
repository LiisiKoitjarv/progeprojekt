################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Platformer mäng, kus tudeng, kes elab
# ühikas peab jõudma Deltasse õppima
#
# Autorid: Taavi Vähi, Liisi Koitjärv
#
# mõningane eeskuju: Donkey Kong (1981)
#
# Lisakommentaar (nt käivitusjuhend): lae alla pildid ja helid, 
# salvesta programm ja lihtsalt pane 'run' kas Thonnys või VSCode'is
##################################################

#import 
from time import sleep
import pygame
import random
pygame.init()

#väärtused jms
clock = pygame.time.Clock()
fps = 60
timer_running = True

ekraani_laius = 1000
ekraani_korgus = 800
ekraan = pygame.display.set_mode((ekraani_laius, ekraani_korgus))
pygame.display.set_caption('Delta Parkuur')

ruudu_suurus = 50
mang_labi = 0
level = 1
# main_menu = True --- tuleb veel!
roosa = (255, 0, 125)
sinine = (0, 0, 255)
roheline = (0, 128, 0)
punane = (255, 0, 0)
valge = (255, 255, 255)

# font
font = pygame.font.SysFont('Bauhaus 93', 50)
voidu_font = pygame.font.SysFont('Bauhaus93', 200)
timer_font = pygame.font.SysFont('Times New Roman', 50)

# pildid
taust_img = pygame.image.load('taustapilt.png')
orav_img = pygame.image.load('orav.png')
kast_img = pygame.image.load('kivi.png')
gclass_img = pygame.image.load('gclass.png')
jaapurikas_img = pygame.image.load('jaapurikas.png')
jaa_img = pygame.image.load('jaa.png')
tiksu = pygame.image.load('tiksu.png')

# sounds
pygame.mixer.music.load('taust.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
hype_sound = pygame.mixer.Sound('hype.wav')
hype_sound.set_volume(0.5)
surm_sound = pygame.mixer.Sound('surm.wav')
surm_sound.set_volume(0.5)
voit_sound = pygame.mixer.Sound('voit.wav')
voit_sound.set_volume(0.5)

# timer
minutid = 0
sekundid = 0
millisekundid = 0
image_size = (50, 50)
image_size2 = (145, 135)
image_size3 = (135, 91.5)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    ekraan.blit(img, (x, y))

def reset_level(level):
    player.reset(50, ekraani_korgus - 130)
    return world

# tudeng tegelane
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'tudeng{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.transform.scale(pygame.image.load('illuminati.png'), image_size)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self, mang_labi):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if mang_labi == 0:
            # klahvivajutused
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] or key[pygame.K_w] and self.jumped == False:
                hype_sound.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False and key[pygame.K_w] == False:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_a] == False and key[pygame.K_d] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # animatsioon
            if self.counter > walk_cooldown:
                # counter vaatab viimast pilti
                self.counter = 0
                # index vaatab mitmenda pildi juures on
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                # 1, vaatab paremale
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                # -1, vaatab vasakule
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # gravitatsioon
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            for ruut in world.tile_list:

                # funktsioon kontrollib kas oleksid jargmisel framel ruudu sees, kui jah siis kiirendus = 0
                if ruut[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # Kokkuporge y koordinaat
                if ruut[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    # Vaatab, kas hyppab
                    if self.vel_y < 0:

                        # tegelase ulemine ots ja ruudu alumine ots, tostab kohakuti need kaks
                        dy = ruut[1].bottom - self.rect.top
                        self.vel_y = 0

                    # Vaatab, kas tegelane langeb
                    elif self.vel_y >= 0:

                        # kui tegelane kukub ruudu sisse, siis ta jaab ruudu peale
                        dy = ruut[1].top - self.rect.bottom
                        self.vel_y = 0

           #asjadega kokkuporge
            if pygame.sprite.spritecollide(self, orav_grupp, False):
                mang_labi = 2
                surm_sound.play()

            if pygame.sprite.spritecollide(self, gclass_grupp, False):
                mang_labi = 2
                surm_sound.play()

            if pygame.sprite.spritecollide(self, jaapurikas_grupp, False):
                mang_labi = 2
                surm_sound.play()

            if pygame.sprite.spritecollide(self, jaa_grupp, False):
                self.image = pygame.transform.rotate(self.image, 90)
                mang_labi = 2
                surm_sound.play()

            if pygame.sprite.spritecollide(self, tiksu_grupp, False):
                mang_labi = 1
                pygame.mixer.music.stop()
                voit_sound.play()

            self.rect.x += dx
            self.rect.y += dy

        elif mang_labi == 2:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 10
                sleep(0.175)
        #mangija
        ekraan.blit(self.image, self.rect)

        return mang_labi

class Lumi:
    def __init__(self):
        self.x = random.randint(0, ekraani_laius)
        self.y = random.randint(-ekraani_korgus, 0)  # Alusta ekraani ylevalt
        self.size = random.randint(2, 5)
        self.speed = random.randint(1, 3) #Lumehelbe kiirus

    def update(self):
        self.y += self.speed  # Liigu alla
        if self.y > ekraani_korgus:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, ekraani_laius)
            self.speed = random.randint(1, 3)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.size)

# Lumi
lumi = [Lumi() for _ in range(100)]

class World():
    def __init__(self, data):
        self.tile_list = []
        rida_count = 0
        for rida in data:
            col_count = 0
            for ruut in rida:
                if ruut == 1:
                    img = pygame.transform.scale(kast_img, (ruudu_suurus, ruudu_suurus))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * ruudu_suurus
                    img_rect.y = rida_count * ruudu_suurus
                    ruut = (img, img_rect)
                    self.tile_list.append(ruut)
                '''
                if ruut == 2: #tuleb libe block
                    img = pygame.transform.scale(libe_img, (ruudu_suurus, ruudu_suurus))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * ruudu_suurus
                    img_rect.y = rida_count * ruudu_suurus
                    ruut = (img, img_rect)
                    self.tile_list.append(ruut)
                '''
                if ruut == 4:
                    gclass = Gclass(col_count * ruudu_suurus, rida_count * ruudu_suurus + 15)
                    gclass_grupp.add(gclass)
                if ruut == 6:
                    orav = Orav(col_count * ruudu_suurus, rida_count * ruudu_suurus + 15)
                    orav_grupp.add(orav)
                if ruut == 8:
                    jaapurikas = Jaapurikas(col_count * ruudu_suurus, rida_count * ruudu_suurus)
                    jaapurikas_grupp.add(jaapurikas)
                if ruut == 10:
                    jaa = Jaa(col_count * ruudu_suurus, rida_count * ruudu_suurus)
                    jaa_grupp.add(jaa)
                if ruut == 12:
                    tiksu = Tiksu(col_count * ruudu_suurus, rida_count * ruudu_suurus)
                    tiksu_grupp.add(tiksu)

                col_count += 1
            rida_count += 1

    #lisab listist ruudud. ruut[0] on asukoht, ruut[1] on pilt
    def draw(self):
        for ruut in self.tile_list:
            ekraan.blit(ruut[0], ruut[1])

class Jaapurikas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('jaapurikas.png')
        self.image = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Jaa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('jaa.png')
        self.image = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Orav(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('orav.png').convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Gclass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.transform.scale(pygame.image.load('gclass.png'), image_size3)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 2
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Tiksu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('tiksu.png')
        flipped = pygame.transform.flip(img, True, False)
        self.image = pygame.transform.scale(flipped, (ruudu_suurus * 2, ruudu_suurus * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#map, igale numbrile vastab pilt
world_data = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 11, 1, 0, 0, 0, 10, 0, 0, 0, 0, 11, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 10, 10, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 10, 0, 0, 10, 1, 10, 10, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 6, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 6, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


#mangija, tema asukoht.
player = Player(50, ekraani_korgus - 190)

#grupid. sprited voetakse gruppidesse kokku
orav_grupp = pygame.sprite.Group()
gclass_grupp = pygame.sprite.Group()
jaapurikas_grupp = pygame.sprite.Group()
jaa_grupp = pygame.sprite.Group()
tiksu_grupp = pygame.sprite.Group()

world = World(world_data)

run = True
while run:
    if timer_running:
        dt = clock.tick(fps)
        millisekundid += dt
        if millisekundid >= 1000:
            sekundid += 1
            millisekundid -= 1000
        if sekundid >= 60:
            minutid += 1
            sekundid -= 60

    ekraan.blit(taust_img, (0, 0))
    aeg = str(minutid) + ":" + str(sekundid) + ":" + str(round(millisekundid, 1))
    draw_text(aeg, timer_font, (255, 0, 0), 50, 50)

    # mangu algus
    world.draw()

    # koik grupid joonistatakse ekraanile
    orav_grupp.update()
    orav_grupp.draw(ekraan)
    gclass_grupp.update()
    gclass_grupp.draw(ekraan)
    jaapurikas_grupp.update()
    jaapurikas_grupp.draw(ekraan)
    jaa_grupp.update()
    jaa_grupp.draw(ekraan)
    tiksu_grupp.update()
    tiksu_grupp.draw(ekraan)

    mang_labi = player.update(mang_labi)

    # mang_labi == 2 : tegelane saab surma.
    if mang_labi == 2:
        key = pygame.key.get_pressed()
        if key[pygame.K_r] == True:
            world_data = []
            world = reset_level(level)
            mang_labi = 0
            score = 0

    # mang_labi == 1 : tegelane joudis leveli lõppu ja võitis
    if mang_labi == 1:
        timer_running = False #timer jääb seisma
        draw_text('võitja', voidu_font, roosa, 200, 400)

    for lumehelbed in lumi:
        lumehelbed.update()
        lumehelbed.draw(ekraan)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
