from engine import LoadImages
from unit.base_unit import BaseUnit
from animation import Animation
import unit

class GladiatorUnit(BaseUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dir, **keywords):
		super().__init__(unit_roster, xpos, ypos, name, number, dir, **keywords)
		self.anim_standing = LoadImages(dir, ["stand2_Frame_0.png", "stand2_Frame_1.png", "stand2_Frame_2.png"]).sequence
		self.anim_atk1 = LoadImages(dir, ["stabOF_Frame_0.png","stabOF_Frame_1.png","stabOF_Frame_2.png"]).sequence
		self.anim_atk2 = LoadImages(dir, ["swingT1_Frame_0.png","swingT1_Frame_1.png","swingT1_Frame_2.png"]).sequence
		self.anim_walking = LoadImages(dir, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence
		self.twoH_atk2_effect = LoadImages("images/", ["2h_atk_effect.png","2h_atk_effect.png","2h_atk_effect.png","2h_atk_effect.png"]).sequence
		self.attacks_dict = {"one": {"energy": 10, "dmg": 10, "x_range": 80, "y_range": 40},
						"two": {"energy": 10, "dmg": 10, "x_range": 50, "y_range": 40},
						"DOOM": {"energy": 0, "dmg": 100}}

	def draw_atk1(self, screen):
		#Stab
		rate = 5
		Animation(screen, self, 0, self.anim_atk1, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_atk2(self, screen):
		#Slam
		rate = 4
		Animation(screen, self, 0, self.anim_atk2, rate).animate()
		Animation(screen, self, self.width, self.twoH_atk2_effect, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

unit.unit_types["GladiatorUnit"] = GladiatorUnit