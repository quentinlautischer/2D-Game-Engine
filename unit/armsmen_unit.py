from animation import LoadImages
from unit.base_unit import BaseUnit
from animation import Animation
import unit, pygame
	
class ArmsmenUnit(BaseUnit):
	"""
	Melee range unit with high health and moderate dmg.
	1 hand sword and sheild
	"""

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand1_Frame_0.png", "stand1_Frame_1.png", "stand1_Frame_2.png"]).sequence
		self.anim_atk1 = LoadImages(dirr, ["stabOF_Frame_0.png","stabOF_Frame_1.png","stabOF_Frame_2.png"]).sequence
		self.anim_atk2 = LoadImages(dirr, ["swingO1_Frame_0.png","swingO1_Frame_1.png","swingO1_Frame_2.png","swingO1_Frame_2.png"]).sequence
		self.anim_walking = LoadImages(dirr, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence
		self.slash_effect = LoadImages(dirr, ["sword_effect.png","sword_effect.png","sword_effect.png"]).sequence
		self.stab_effect = LoadImages(dirr, ["stab_effect.png","stab_effect.png","stab_effect.png"]).sequence
		self.anim_death = LoadImages(dirr, ["rope_Frame_0.png"], 90).sequence
		self.attacks_dict = {"one": {"energy": 0, "dmg": 20, "x_range": 60, "y_range": 40},
						"two": {"energy": 0, "dmg": 50, "x_range": 40, "y_range": 40}}

		self.health_max = 300
		self.health = self.health_max
	
	def draw_atk1(self, screen):
		#Stab
		rate = 1
		Animation(screen, self, 0,0, self.anim_atk1, rate).animate()
		Animation(screen, self, self.width,0, self.stab_effect, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_atk2(self, screen):
		#slash
		rate = 3
		Animation(screen, self, 0,0, self.anim_atk2, rate).animate()
		Animation(screen, self, self.width,0, self.slash_effect, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

unit.unit_types["ArmsmenUnit"] = ArmsmenUnit