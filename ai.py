import pygame, engine

class AI(object):
	"""
	This object in creted within any unit needing AI controls
	self.sequence is a list of unit methods that will be executed 
	sequencially.

	"""

	def __init__(self, unit, sequence_list):
		self.unit = unit
		self.set_time = 0
		self.sequence = sequence_list #List of Unit Methods.
		self.seq_count = 0

	def seq_execute(self, seq_num):
		"""
		Iterates over the method sequence and executes if the given time
		has been elapsed.
		"""
		SEQ_TIMER = 500

		#Check time if greater than SEQ_TIMER then execute.
		if self.set_time == 0:
			self.set_time = pygame.time.get_ticks()

		if pygame.time.get_ticks() > self.set_time + SEQ_TIMER:
			self.sequence[seq_num][self.seq_count]()
			self.seq_count += 1
			self.seq_count %= len(self.sequence[seq_num])
			self.set_time = 0

	def find_closest_player(self):
		"""
		Returns closest unit object.
		"""
		dist_enm_to_player = {}
		unit_x,unit_y = self.unit.get_position()


		for player in self.unit.unit_roster.get("Players"):
			if player.dead == True:
				dist_enm_to_player[float('inf')] = player
			else:
				pl_x, pl_y = player.get_position()
				dist = engine.straight_line_dist(unit_x, unit_y, pl_x, pl_y)
				dist_enm_to_player[dist] = player
		return dist_enm_to_player[min(dist_enm_to_player.keys())]

	



	#def Attack(self):