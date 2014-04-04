import pygame
import math
from graph_module import Graph
from animation import *
import engine
from unit.teddyghost_unit import TeddyGhostUnit
from unit.werewolf_unit import WerewolfUnit
from unit.goblin_unit import GoblinUnit

class Script(object):

	def __init__(self, unit_roster, maps, screen):
		self.unit_roster = unit_roster
		self.screen = screen
		self.maps = maps
		self.scroll_available = 0
		self.text_print = 1
		self.quest_text = ""
	

		self.current_grid_quests = {
			0: [("Welcome to the game", "quest text"),(self.release_wave,"release wave", 1, TeddyGhostUnit, "images/teddyghost/")],
			1: [("Defeat the Monsters!", "quest text"),(self.release_wave,"release wave", 4, GoblinUnit, "images/enemy/"), (None, "defeat wave")],
			2: [("Keep Going", "quest text")],
			3: [("Defeat the Monsters!", "quest text"),(self.release_wave,"release wave", 4, GoblinUnit, "images/enemy/"), (None, "defeat wave")],
			4: [("A stronger enemy approaches...", "quest text"), (self.release_wave, "release wave", 2, WerewolfUnit, "images/werewolf/")],
			5: [("Death Teddy Asks that you leave...!", "quest text"),(self.release_wave,"release wave", 1, TeddyGhostUnit, "images/teddyghost/"), (None, "defeat wave"),("You Win", "quest text"),("Keep Going", "STALL FULLER")]
		}

		self.quest = self.current_grid_quests.get(self.maps.current_grid)

	def update_script(self):
		if self.quest:
			self.scroll_available = 0
			if self.quest[0][1] == "release wave":
				a,b,c,d,e = self.quest.pop(0)
				a(d, e, c)
			elif self.quest[0][1] == "defeat wave":
				if self.unit_roster.get("Enemies"):
					pass
				else:
					self.quest.pop(0)
			elif self.quest[0][1] == "quest text":
				self.quest_text, b = self.quest.pop(0)
				self.text_timer = pygame.time.get_ticks()
				self.text_print = 1
		else:
			self.scroll_available = 1

		if pygame.time.get_ticks() > self.text_timer + 4000:
			self.text_print = 0
			self.quest_text = "" 

	def release_wave(self, enemy_type, enemy_img, num):
		#Only allows 4 mobs at a time.
		for i in range(num%5):
			engine.spawn_enemy_specified_loc(self.unit_roster, self.maps, enemy_type, 1, enemy_img, 800, 400+(i*64))
		
	def update_quest(self):
		self.quest = self.current_grid_quests.get(self.maps.current_grid)

	def update_quest_text(self):
		font = pygame.font.SysFont("monospace", 50)
		label = font.render(self.quest_text, 1, (255, 255, 255))
		self.screen.blit(label, (100, 125))		
