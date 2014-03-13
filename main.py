# Main File

import pygame, random
from pygame.locals import *
from gui import GUI
from engine import ENGINE
from unit.spellweaver_unit import SpellWeaverUnit
from unit.armsmen_unit import ArmsmenUnit
from unit.gladiator_unit import GladiatorUnit
from unit.werewolf_unit import WerewolfUnit
from unit.golem_unit import GolemUnit
from maps import Maps

RESOLUTION_SCALE  = 1
RESOLUTION_X = 1024 * RESOLUTION_SCALE
RESOLUTION_Y = 600 * RESOLUTION_SCALE

def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y))
	pygame.display.set_caption('Switch & If')

	unit_roster = []
	unit_roster.append(ArmsmenUnit(unit_roster, 500, 400, "Switch", 1, "images/player1/"))
	unit_roster.append(SpellWeaverUnit(unit_roster, 500, 600, "If", 2, "images/player2/"))
	unit_roster.append(WerewolfUnit(unit_roster, random.randint(0, 900), random.randint(350, 600), "enemy", -2, "images/werewolf/"))

	gui = GUI(screen, unit_roster)
	maps = Maps(screen)
	engine = ENGINE(screen, gui, unit_roster, maps)
	
	#init
	gui.draw(unit_roster)

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		#MAIN LOOPER BRAH
		#if random.randint(0, 1000) > 990:
			#unit_roster.append(WerewolfUnit(unit_roster, random.randint(0, 900), random.randint(350, 600), "enemy", -2, "images/werewolf/"))

		engine.update_logic()
		engine.update_draw()

if __name__ == '__main__': main()





