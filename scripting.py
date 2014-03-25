import pygame
import math
from graph_module import Graph
from animation import *
import engine
from unit.werewolf_unit import WerewolfUnit
from unit.goblin_unit import GoblinUnit

class Script(object):

	def __init__(self, unit_roster, maps):
		self.unit_roster = unit_roster
		self.maps = maps
		self.scroll_available = 0
	

		self.current_grid_quests = {0: [(self.release_wave_6,"release wave"), (None, "defeat wave")],
		1: [(self.release_wave_6,"release wave")]}

		self.quest = self.current_grid_quests.get(self.maps.current_grid)
		print(self.quest)
	def update_script(self):
		if self.quest:
			if self.quest[0][1] == "release wave":
				a,b = self.quest.pop(0)
				a(GoblinUnit, "images/enemy/")
			elif self.quest[0][1] == "defeat wave":
				if self.unit_roster.get("Enemies"):
					pass
				else:
					self.quest.pop(0)
		else:
			self.scroll_available = 1
	def release_wave_6(self, enemy_type, enemy_img):
		for i in range(2):
			engine.spawn_enemy_specified_loc(self.unit_roster, self.maps, enemy_type, 1, enemy_img, 800, 400+(i*64))
		
	def update_quest(self):
		self.quest = self.current_grid_quests.get(self.maps.current_grid)