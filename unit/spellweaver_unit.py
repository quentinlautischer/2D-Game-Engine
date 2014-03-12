from engine import LoadImages
from unit.base_unit import BaseUnit
from animation import Animation
import unit

class SpellWeaverUnit(BaseUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dir, **keywords):
		super().__init__(unit_roster, xpos, ypos, name, number, dir, **keywords)
		self.anim_standing = LoadImages(dir, ["stand1_Frame_0.png", "stand1_Frame_1.png", "stand1_Frame_2.png"]).sequence
		self.anim_atk1 = LoadImages(dir, ["stabO1_Frame_0.png","shootF_Frame_0.png","shootF_Frame_1.png","shootF_Frame_2.png"]).sequence
		self.anim_atk2 = LoadImages(dir, ["swingO3_Frame_0.png","swingO3_Frame_1.png","swingO3_Frame_2.png"]).sequence
		self.anim_walking = LoadImages(dir, ["walk1_Frame_0.png","walk1_Frame_1.png","walk1_Frame_2.png","walk1_Frame_3.png"]).sequence
		self.firearrow_effect = LoadImages("images/", ["firearrow.png","firearrow.png","firearrow.png","firearrow.png"]).sequence
		self.firearrow_move = -20
		self.attacks_dict = {"one": {"energy": 10, "dmg": 50, "x_range": 1000, "y_range": 40},
						"two": {"energy": 10, "dmg": 70, "x_range": 70, "y_range": 40},
						"DOOM": {"energy": 0, "dmg": 100, "x_range": 50, "y_range": 50}}


	def draw_atk1(self, screen):
		#Bow
		rate = 4
		Animation(screen, self, 0, self.anim_atk1, rate).animate()
		Animation(screen, self, self.width + self.firearrow_move, self.firearrow_effect, rate).animate()
		self.firearrow_move += 60
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"
			self.firearrow_move = -20

	def draw_atk2(self, screen):
		#Spell Sweep
		rate = 5
		Animation(screen, self, 0, self.anim_atk2, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

unit.unit_types["SpellWeaverUnit"] = SpellWeaverUnit