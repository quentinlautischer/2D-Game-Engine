import pygame, unit#, effects
from engine import *

class BaseUnit(object):


	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		self.image = pygame.image.load("images/player1/stand1_Frame_0.png")
		self.faction = faction
		self.health_max  = 100
		self.health= self.health_max
		self.last_health = self.health
		self.energy_max = 100
		self.energy = self.energy_max
		self.xpos = xpos
		self.ypos = ypos
		self.number = number
		self.width = 60
		self.maps = maps
		self.step_vert = 16
		self.height = self.image.get_rect().size[1]
		self.step_horz = 16
		self.position = self.position_update()
		self.is_walking = 0
		self.direction = 'left'
		self.dead_time = 0
		self.unit_roster = unit_roster
		self.name = name
		self.dead = False
		self.dmg_dealt = True
		self.dmg_done_to_me = []
		self.attack_status = "none"
		self.attacks_dict = {"one": {"energy": 10, "dmg": 10, "x_range": 60, "y_range": 40},
						"two": {"energy": 10, "dmg": 10, "x_range": 40, "y_range": 40},
						"DOOM": {"energy": 0, "dmg": 100}}

	def get_position(self):
		return self.xpos, self.ypos
	
	def position_update(self):
		self.position = pygame.Rect(self.xpos, self.ypos-self.height, self.width, self.height)
	
	def move_left(self):
		self.is_walking = 1
		self.direction = 'left'
		
		grid_graph = self.maps.map_grids.get(self.maps.map_list[self.maps.current_map])[self.maps.current_grid][0]
		grid_get_vert = self.maps.map_grids.get(self.maps.map_list[self.maps.current_map])[self.maps.current_grid][2]

		if grid_graph.is_vertex(grid_get_vert.get((self.xpos-self.step_horz, self.ypos))):
			self.xpos -= self.step_horz

	def move_right(self):
		self.is_walking = 1
		self.direction = 'right'
		grid_graph = self.maps.map_grids.get(self.maps.map_list[self.maps.current_map])[self.maps.current_grid][0]
		grid_get_vert = self.maps.map_grids.get(self.maps.map_list[self.maps.current_map])[self.maps.current_grid][2]

		if grid_graph.is_vertex(grid_get_vert.get((self.xpos+self.step_horz*3, self.ypos))):
			self.xpos += self.step_horz

	def move_down(self):
		self.is_walking = 1
		
		grid_graph = self.maps.map_grids.get(self.maps.map_list[self.maps.current_map])[self.maps.current_grid][0]
		grid_get_vert = self.maps.map_grids.get(self.maps.map_list[self.maps.current_map])[self.maps.current_grid][2]

		if grid_graph.is_vertex(grid_get_vert.get((self.xpos, self.ypos+self.step_vert))):
			self.ypos += self.step_vert

	def move_up(self):
		self.is_walking = 1
		
		grid_graph = self.maps.map_grids.get(self.maps.map_list[self.maps.current_map])[self.maps.current_grid][0]
		grid_get_vert = self.maps.map_grids.get(self.maps.map_list[self.maps.current_map])[self.maps.current_grid][2]

		if grid_graph.is_vertex(grid_get_vert.get((self.xpos, self.ypos-self.step_vert*6))):

			self.ypos -= self.step_vert

	def is_walking(self):

		return self.is_walking

	def get_health(self):
		return self.health

	def gain_health(self, hp):
		if self.health < self.health_max:
			self.health += hp
		if self.health > 100:
			self.health = 100
	
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
			self.energy += gain
		if self.energy > 100:
			self.energy = 100

	def attack_spell(self, atk):
		if self.energy >= self.attacks_dict.get(atk).get("energy"):
			if self.attack_status == "none":
				self.attack_status = atk
				self.dmg_dealt = False
				self.lose_energy(self.attacks_dict.get(atk).get("energy"))

	def check_dmg_done(self, roster):
		x_range = self.attacks_dict.get(self.attack_status).get("x_range")
		y_range = self.attacks_dict.get(self.attack_status).get("y_range")

		for enemy in roster:
				if in_range_cross(self, enemy, x_range, y_range, self.direction):
					enemy.lose_health(self.attacks_dict.get(self.attack_status).get("dmg"))
					return self.attacks_dict.get(self.attack_status).get("dmg")

	def draw_walking(self, screen):
		rate = 5
		Animation(screen, self, 0, self.anim_walking, rate).animate()
		if self.anim_walking[-2] == len(self.anim_walking) - 3 and self.anim_walking[-1] == rate-1:
			Animation(screen, self, 0, self.anim_walking, 5).animate()
			self.anim_walking[-2] = 0
		self.is_walking = 0

	def draw_atk1(self, screen):
		rate = 3
		Animation(screen, self, 0, self.anim_atk1, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_atk2(self, screen):
		rate = 3
		Animation(screen, self, 0, self.anim_atk2, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

	def draw_death(self, screen):
		#Stab
		rate = 10
		Animation(screen, self, 0, self.anim_death, rate).animate()
		if self.anim_death[-2] == len(self.anim_death) - 3 and self.anim_death[-1] == rate-1:
			Animation(screen, self, 0, self.anim_death, 5).animate()
			self.anim_death[-2] = 0

	def queue_attack1(self):
		self.dmg_dealt = False
		self.attack_status = "one"