# Main File

import pygame, random, sys
from pygame.locals import *
from gui import GUI
from engine import ENGINE, Controller
from unit.spellweaver_unit import SpellWeaverUnit
from unit.armsmen_unit import ArmsmenUnit
from unit.gladiator_unit import GladiatorUnit
from unit.werewolf_unit import WerewolfUnit
from maps import Maps
from scripting import Script

#Scaling is not actually yet implemented. 
RESOLUTION_SCALE  = 1
RESOLUTION_X = 1024 * RESOLUTION_SCALE
RESOLUTION_Y = 600 * RESOLUTION_SCALE



def main():
	# Initialise screen and sound
	pygame.init()
	pygame.mixer.pre_init(22050, -16, 2, 512) # Small buffer for less sound lag
	screen = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y))
	pygame.display.set_caption('Switch & If')

	# Initialise Data structures and engine objects
	unit_roster = {"Players": [], "Enemies": []}

	maps = Maps(screen)

	# Enter menu screen to collect needed info to generate rest of objects
	menu_screen(screen)(screen, unit_roster, maps)
	
	gui = GUI(screen, unit_roster)

	script = Script(unit_roster, maps, screen)
	
	engine = ENGINE(screen, gui, unit_roster, maps, script)

	#init gui interface
	gui.draw(unit_roster)

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
		#Main Events
		engine.update_logic()
		engine.update_draw()

def menu_screen(screen):

	bg = pygame.image.load("images/menu.jpg")
	screen.blit(bg, (0,0))
	font = pygame.font.Font(None, 56)
	default = ((255, 255, 255), False)
	highlight = ((255, 255, 0), True)
	control = Controller(None)
	game_mode_text_pos = (700, 100)

	mode = [[highlight, init_1p], [default, init_2p]]
	current_mode = 0

	#Selection Loop (Toggles between selections)
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(font.render("Game Mode", 1, default[0]), game_mode_text_pos)
		screen.blit(font.render("1 Player", 1, mode[0][0][0]), (game_mode_text_pos[0], game_mode_text_pos[1]+50))
		screen.blit(font.render("2 Player", 1,mode[1][0][0]), (game_mode_text_pos[0], game_mode_text_pos[1]+100))

		pygame.display.update()

		#Wait for Menu scroll
		while (pygame.event.wait().type != KEYDOWN): pass

		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			mode[current_mode][0] = default
			current_mode -= 1
			current_mode %= len(mode)
			mode[current_mode][0] = highlight
		if keys[pygame.K_DOWN]:
			mode[current_mode][0] = default
			current_mode += 1
			current_mode %= len(mode)
			mode[current_mode][0] = highlight
		if keys[pygame.K_RETURN]:
			for m in mode:
				if m[0] == highlight:
					return m[1]


def init_2p(screen, unit_roster, maps):
	#Adds players to unit roster
	unit_roster.get("Players").append(GladiatorUnit(unit_roster, 64, 512, "Switch", 1, "images/Josh/", "Good", maps))
	unit_roster.get("Players").append(SpellWeaverUnit(unit_roster, 136, 512, "If", 2, "images/Quentin/", "Good", maps))

def init_1p(screen, unit_roster, maps):
	#Adds player to unit roster
	unit_roster.get("Players").append(SpellWeaverUnit(unit_roster, 64, 512, "Switch", 1, "images/Quentin/", "Good", maps))	

if __name__ == '__main__': main()