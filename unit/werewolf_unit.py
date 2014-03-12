#Werewolf
from engine import LoadImages, LoadImagesSheet
from unit.base_unit import BaseUnit
from animation import Animation
import unit

class WerewolfUnit(BaseUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, **keywords):
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand_frame0.png","stand_frame1.png", "stand_frame2.png"]).sequence
		self.anim_walking = LoadImages(dirr, ["walking_frame0.png","walking_frame1.png", "walking_frame2.png", "walking_frame3.png"]).sequence
		self.anim_atk1 = LoadImages(dirr, ["Slash0_Frame0.png","Slash0_Frame1.png","Slash0_Frame2.png","Slash0_Frame3.png","Slash0_Frame4.png","Slash0_Frame5.png","Slash0_Frame6.png","Slash0_Frame7.png","Slash0_Frame8.png","Slash0_Frame9.png"]).sequence
		self.anim_death = LoadImages(dirr, ["death_frame0.png","death_frame1.png","death_frame2.png","death_frame3.png","death_frame4.png","death_frame5.png","death_frame6.png","death_frame7.png"]).sequence	
		self.attacks_dict = {"one": {"energy": 10, "dmg": 200, "x_range": 150, "y_range": 120},
						"two": {"energy": 10, "dmg": 10, "x_range": 40, "y_range": 40},
						"DOOM": {"energy": 0, "dmg": 100, "x_range": 50, "y_range": 50}}

		self.width = 150
		self.height = 200
	
	def draw_atk1(self, screen):
		#Stab
		rate = 1
		Animation(screen, self, 0, self.anim_atk1, rate).animate()
		#Animation(screen, self, self.width, self.stab_effect, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_atk2(self, screen):
		#slash
		rate = 3
		Animation(screen, self, 0, self.anim_atk2, rate).animate()
		Animation(screen, self, self.width, self.slash_effect, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"


unit.unit_types["WerewolfUnit"] = WerewolfUnit