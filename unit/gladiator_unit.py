from animation import LoadImages
from unit.base_unit import BaseUnit
from animation import Animation
import unit, pygame

class GladiatorUnit(BaseUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand2_Frame_0.png", "stand2_Frame_1.png", "stand2_Frame_2.png"]).sequence
		self.anim_atk1 = LoadImages(dirr, ["stabOF_Frame_0.png","stabOF_Frame_1.png","stabOF_Frame_2.png"]).sequence
		self.anim_atk2 = LoadImages(dirr, ["swingT1_Frame_0.png","swingT1_Frame_1.png","swingT1_Frame_2.png"]).sequence
		self.anim_walking = LoadImages(dirr, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence
		self.twoH_atk2_effect = LoadImages("images/", ["2h_atk_effect.png","2h_atk_effect.png","2h_atk_effect.png","2h_atk_effect.png"]).sequence
		self.anim_death = LoadImages(dirr, ["rope_Frame_0.png"], 90).sequence
		self.attacks_dict = {"one": {"energy": 10, "dmg": 20, "x_range": 100, "y_range": 40},
						"two": {"energy": 50, "dmg": 40, "x_range": 100, "y_range": 40}}

		self.health_max = 300
		self.health = self.health_max

	def draw_atk1(self, screen):
		print(self.health)
		#Stab
		rate = 5
		Animation(screen, self, 0,0, self.anim_atk1, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_atk2(self, screen):
		#Slam
		rate = 4
		Animation(screen, self, 0,0, self.anim_atk2, rate).animate()
		Animation(screen, self, self.width,0, self.twoH_atk2_effect, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

unit.unit_types["GladiatorUnit"] = GladiatorUnit