# Main File

import pygame, random
from pygame.locals import *
from gui import GUI
from engine import ENGINE, Controller
from unit.spellweaver_unit import SpellWeaverUnit
from unit.armsmen_unit import ArmsmenUnit
from unit.gladiator_unit import GladiatorUnit
from unit.werewolf_unit import WerewolfUnit
from unit.golem_unit import GolemUnit
from unit.cleric_unit import ClericUnit
from maps import Maps

RESOLUTION_SCALE  = 1
RESOLUTION_X = 1024 * RESOLUTION_SCALE
RESOLUTION_Y = 600 * RESOLUTION_SCALE

def menu_screen(screen):
	bg = pygame.image.load("images/menu.jpg")
	screen.blit(bg, (0,0))
	font = pygame.font.Font(None, 56)
	default = ((255, 255, 255), False)
	highlight = ((255, 255, 0), True)
	control = Controller(None)
	game_mode_text_pos = (700, 100)

	mode = [[highlight, init_1p], [default, init_2p], [default, init_3p], [default, init_1v1]]
	current_mode = 0



	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(font.render("Game Mode", 1, default[0]), game_mode_text_pos)
		screen.blit(font.render("1 Player", 1, mode[0][0][0]), (game_mode_text_pos[0], game_mode_text_pos[1]+50))
		screen.blit(font.render("2 Player", 1,mode[1][0][0]), (game_mode_text_pos[0], game_mode_text_pos[1]+100))
		screen.blit(font.render("3 Player", 1,mode[2][0][0]), (game_mode_text_pos[0], game_mode_text_pos[1]+150))
		screen.blit(font.render("1v1 Duel", 1,mode[3][0][0]), (game_mode_text_pos[0], game_mode_text_pos[1]+200))

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


def init_3p(screen, unit_roster, maps):
	unit_roster.get("Players").append(ArmsmenUnit(unit_roster, 32, 256, "Switch", 1, "images/player1/", "Good", maps))
	unit_roster.get("Players").append(SpellWeaverUnit(unit_roster, 500, 300, "If", 2, "images/player2/", "Good", maps))
	unit_roster.get("Players").append(ClericUnit(unit_roster, 500, 600, "Elly", 3, "images/healer/", "Good", maps))
	unit_roster.get("Enemies").append(WerewolfUnit(unit_roster, random.randint(0, 900), random.randint(350, 600), "enemy", -2, "images/werewolf/", "Bad", maps))

def init_2p(screen, unit_roster, maps):
	unit_roster.get("Players").append(ArmsmenUnit(unit_roster, 64, 512, "Switch", 1, "images/player1/", "Good", maps))
	unit_roster.get("Players").append(SpellWeaverUnit(unit_roster, 500, 600, "If", 2, "images/player2/", "Good", maps))
	unit_roster.get("Enemies").append(WerewolfUnit(unit_roster, random.randint(0, 900), random.randint(350, 600), "enemy", -2, "images/werewolf/", "Bad", maps))

def init_1p(screen, unit_roster, maps):
	unit_roster.get("Players").append(ArmsmenUnit(unit_roster, 500, 400, "Switch", 1, "images/player1/", "Good"))	
	unit_roster.get("Enemies").append(WerewolfUnit(unit_roster, random.randint(0, 900), random.randint(350, 600), "enemy", -2, "images/werewolf/", "Bad", maps))

def init_1v1(screen, unit_roster, maps):
	unit_roster.get("Players").append(ArmsmenUnit(unit_roster, 500, 400, "Switch", 1, "images/player1/", "Good", maps))
	unit_roster.get("Enemies").append(SpellWeaverUnit(unit_roster, 500, 600, "If", 2, "images/player2/", "Bad", maps))

def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y))
	pygame.display.set_caption('Switch & If')

	unit_roster = {"Players": [], "Enemies": []}

	maps = Maps(screen)
	menu_screen(screen)(screen, unit_roster, maps)
	
	gui = GUI(screen, unit_roster)
	
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
			#unit_roster.append(WerewolfUnit(unit_roster, random.randint(0, 900), random.randint(350, 600), "enemy", -2, "images/werewolf/", maps))
		#script
		
		engine.update_logic()
		engine.update_draw()

if __name__ == '__main__': main()





