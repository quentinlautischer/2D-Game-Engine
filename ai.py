import pygame
import tools

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
		pass