import pygame
import tools
import engine

class AI(object):

	def __init__(self, unit, sequence_list):
		self.unit = unit
		self.set_time = 0
		self.sequence = sequence_list
		self.seq_count = 0
		#MAKE A LIST CONTAINING AI MOVES

	def seq_execute(self, seq_num):
		if self.set_time == 0:
			self.set_time = pygame.time.get_ticks()

		if pygame.time.get_ticks() > self.set_time + 500:
			self.sequence[seq_num][self.seq_count]()
			self.seq_count += 1
			self.seq_count %= len(self.sequence[seq_num])
			self.set_time = 0

	def find_closest_player(self):
		dist_enm_to_player = {}
		unit_x,unit_y = self.unit.get_position()

		for player in self.unit.unit_roster.get("Players"):
			pl_x, pl_y = player.get_position()
			dist = engine.straight_line_dist(unit_x, unit_y, pl_x, pl_y)
			dist_enm_to_player[dist] = player
		return dist_enm_to_player[min(dist_enm_to_player.keys())]

	



	#def Attack(self):