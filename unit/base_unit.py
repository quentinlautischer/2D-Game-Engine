import pygame, unit#, effects
from engine import *

class BaseUnit(object):


	def __init__(self, xpos, ypos, **keywords):
		self.health = 100
		self.health_max = self.health
		self.energy = 100
		self.energy_max = self.energy
		self.xpos = xpos
		self.ypos = ypos
		self.width = 60
		self.step_vert = 5
		self.height = 100
		self.step_horz = 10
		self.position = self.position_update()
		self.image = pygame.image.load("images/player.png")
		self.is_walking = 0
		self.direction = 'left'
		self.dead_time = 0

	def get_position(self):
		return self.xpos, self.ypos
	
	def position_update(self):
		self.position = pygame.Rect(self.xpos, self.ypos-self.height, self.width, self.height)
	
	def move_left(self):
		self.is_walking = 1
		self.direction = 'left'

		if not detect_collision(self, self.unit_roster):
			self.xpos -= self.step_horz
		

	def move_right(self):
		self.is_walking = 1
		self.direction = 'right'
		if not detect_collision(self, self.unit_roster):
			self.xpos += self.step_horz
		

	def move_down(self):
		self.is_walking = 1
		if self.ypos - self.step_vert < 650:
			self.ypos += self.step_vert


	def move_up(self):
		self.is_walking = 1
		if self.ypos - self.step_vert > 350:
			self.ypos -= self.step_vert

	def is_walking(self):

		return self.is_walking

	def get_health(self):
		return self.health
	
	def lose_health(self, dmg):
		if self.health > 0:
			self.health =  self.health - dmg
			if self.health < 0:
				self.health = 0

	def lose_energy(self, cost):
		if self.energy > 0:
			self.energy =  self.energy - cost

	def gain_energy(self, gain):
		if self.energy < 100:
			self.energy = self.energy + gain
		if self.energy > 100:
			self.energy = 100

