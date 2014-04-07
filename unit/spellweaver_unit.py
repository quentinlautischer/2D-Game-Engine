from animation import LoadImages
from unit.base_unit import BaseUnit
from animation import Animation
import unit, pygame
class SpellWeaverUnit(BaseUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps,  **keywords):
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand1_Frame_0.png", "stand1_Frame_1.png", "stand1_Frame_2.png"]).sequence
		self.anim_atk1 = LoadImages(dirr, ["stabO1_Frame_0.png","shootF_Frame_0.png","shootF_Frame_1.png","shootF_Frame_2.png"]).sequence
		self.anim_atk2 = LoadImages(dirr, ["swingO3_Frame_0.png","swingO3_Frame_1.png","swingO3_Frame_2.png"]).sequence
		self.anim_walking = LoadImages(dirr, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence
		self.anim_death = LoadImages(dirr, ["rope_Frame_0.png"], 90).sequence
		self.firearrow_effect = LoadImages("images/", ["firearrow.png","firearrow.png","firearrow.png","firearrow.png"]).sequence
		self.firearrow_move = -40
		self.attacks_dict = {"one": {"energy": 5, "dmg": 40, "x_range": 1000, "y_range": 70},
						"two": {"energy": 30, "dmg": 50, "x_range": 70, "y_range": 100},
						"DOOM": {"energy": 0, "dmg": 100, "x_range": 50, "y_range": 50}}


	def draw_atk1(self, screen):
		#Bow
		rate = 2
		Animation(screen, self, 0,0, self.anim_atk1, rate).animate()
		Animation(screen, self, self.width + self.firearrow_move,0, self.firearrow_effect, rate).animate()
		self.firearrow_move += 60
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"
			self.firearrow_move = -20

	def draw_atk2(self, screen):
		#Spell Sweep
		rate = 5
		Animation(screen, self, 0,0, self.anim_atk2, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

unit.unit_types["SpellWeaverUnit"] = SpellWeaverUnit