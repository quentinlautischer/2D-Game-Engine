import pygame, unit
from unit.base_unit import BaseUnit
from animation import Animation
from engine import *

class PlayerUnit(BaseUnit):
	
	def __init__(self, unit_roster, xpos, ypos, name, number, dir, **keywords):
		super().__init__(xpos, ypos, **keywords)
		self.number = number
		self.unit_roster = unit_roster
		self.name = name
		self.anim_standing = LoadImages(dir, ["stand1_Frame_0.png", "stand1_Frame_1.png", "stand1_Frame_2.png"]).sequence
		self.anim_atk_stab = LoadImages(dir, ["stabOF_Frame_0.png","stabOF_Frame_1.png","stabOF_Frame_2.png"]).sequence
		self.anim_atk_slash = LoadImages(dir, ["swingO1_Frame_0.png","swingO1_Frame_1.png","swingO1_Frame_2.png"]).sequence
		self.anim_walking = LoadImages(dir, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence
		self.anim_death = pygame.transform.rotate((pygame.image.load(dir + "rope_Frame_0.png")), 90)
		self.dead = False
		self.dmg_dealt = True
		self.attack_status = "none"
		self.attacks = {"stab": {"energy": 10, "dmg": 20},
						"slash": {"energy": 10, "dmg": 40},
						"DOOM": {"energy": 0, "dmg": 100}}


	def attack_spell(self, atk):
		if self.energy >= self.attacks.get(atk).get("energy"):
			if self.attack_status == "none":
				self.attack_status = atk
				self.dmg_dealt = False
				self.lose_energy(self.attacks.get(atk).get("energy"))

	def check_dmg_done(self, roster):
		for enemy in roster:
			if enemy.name != self.name:
				if in_range(self, enemy, 50, 25, self.direction):
					enemy.lose_health(self.attacks.get(self.attack_status).get("dmg"))

unit.unit_types["PlayerUnit"] = PlayerUnit