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
		self.scroll_available = 1
		self.quest = [self.release_wave_6(WerewolfUnit, "images/werewolf/"), self.release_wave_6(GoblinUnit, "images/enemy/")]

	def update_script(self):
		if self.quest:
			self.quest.pop(0)

	def release_wave_6(self, enemy_type, enemy_img):
		for i in range(2):
			engine.spawn_enemy_specified_loc(self.unit_roster, self.maps, enemy_type, 1, enemy_img, 800, 256+(i*256))
		