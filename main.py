# Main File

import pygame, random
from pygame.locals import *
from gui import GUI
from engine import ENGINE
from unit.spellweaver_unit import SpellWeaverUnit
from unit.armsmen_unit import ArmsmenUnit
from unit.gladiator_unit import GladiatorUnit
from unit.player_unit import PlayerUnit
from map import Map

def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((1024, 600))
	pygame.display.set_caption('Switch & If')

	unit_roster = []
	unit_roster.append(GladiatorUnit(unit_roster, 500, 400, "Switch", 1, "images/Josh_Switch/"))
	unit_roster.append(SpellWeaverUnit(unit_roster, 500, 600, "If", 2, "images/Quentin/"))

	gui = GUI(screen, unit_roster)
	map = Map(screen)
	engine = ENGINE(screen, gui, unit_roster, map)
	
	#init
	gui.draw(unit_roster)

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		#MAIN LOOPER BRAH
		if random.randint(0, 1000) > 990:
			unit_roster.append(PlayerUnit(unit_roster, random.randint(0, 900), random.randint(350, 600), "enemy", -2, "images/enemy/"))

		engine.update_logic()
		engine.update_draw()

if __name__ == '__main__': main()





