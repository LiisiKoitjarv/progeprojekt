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
from pygame import*
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
