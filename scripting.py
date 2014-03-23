import pygame
import math
from graph_module import Graph
from animation import *
import engine
from unit.werewolf_unit import WerewolfUnit

class Script(object):

	def __init__(self, unit_roster, maps):
		self.unit_roster = unit_roster
		self.maps = maps
		self.scroll_available = 1


	def update_script(self):
		engine.spawn_enemy(self.unit_roster, self.maps, WerewolfUnit, 3, "images/werewolf/")
		pass

	