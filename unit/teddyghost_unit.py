from animation import LoadImages
from unit.base_unit import BaseUnit
from unit.base_enemy_unit import BaseEnemyUnit
from animation import Animation
import unit
from ai import AI

class TeddyGhostUnit(BaseEnemyUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png"]).sequence
		self.anim_walking = LoadImages(dirr, ["stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png"]).sequence
		self.anim_atk1 = LoadImages(dirr, ["attack1.11.png","attack1.10.png", "attack1.9.png","attack1.8.png","attack1.7.png", "attack1.6.png","attack1.5.png","attack1.4.png", "attack1.3.png","attack1.2.png","attack1.1.png", "attack1.0.png"]).sequence
		self.anim_warn1 = LoadImages(dirr, ["attack1.11.png","attack1.10.png", "attack1.9.png","attack1.8.png","attack1.7.png", "attack1.6.png","attack1.5.png","attack1.4.png", "attack1.3.png","attack1.2.png","attack1.1.png", "attack1.0.png"]).sequence
		
		self.deathbeam_effect = LoadImages(dirr, ["Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png"]).sequence
		self.attacks_dict = {"one": {"energy": 10, "dmg": 10, "x_range": 1000, "y_range": 20},
						"two": {"energy": 10, "dmg": 10, "x_range": 40, "y_range": 40},
						"DOOM": {"energy": 0, "dmg": 100, "x_range": 50, "y_range": 50}}

		self.width = 136  #self.anim_attack1ing[0].get_rect().size[0] 
		self.height = 160 #self.anim_standing[0].get_rect().size[1]
		self.health_max = 1000
		self.health = self.health_max
		self.step_horz = 32
		self.step_vert = 32

		self.AI = AI(self,[])
		self.AI.sequence.append([self.Approach])
		self.AI.sequence.append([self.queue_warn1, self.queue_attack1])
		self.AI.sequence.append([self.queue_warn1, self.queue_attack1])

	def draw_atk1(self, screen):
		#Stab
		rate = 1
		Animation(screen, self, 0, self.anim_atk1, rate).animate()
		Animation(screen, self, 550, self.deathbeam_effect, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_warn1(self, screen):
		#Stab
		rate = 4
		Animation(screen, self, 0, self.anim_warn1, rate).animate()
		#Animation(screen, self, self.width, self.stab_effect, rate).animate()
		if self.anim_warn1[-2] == len(self.anim_warn1) - 3 and self.anim_warn1[-1] == rate-1:
			Animation(screen, self, 0, self.anim_warn1, 5).animate()
			self.anim_warn1[-2] = 0
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

	def special_atk1(self, screen):
		# extra fog rolls in boss disapears claws attack
		pass


	def queue_warn1(self):
		self.attack_status = "warn1"

	def Dance(self):
		pass

	def Approach(self):

		unit_x,unit_y = self.get_position()
		player_ofa = self.AI.find_closest_player()
		pl_x, pl_y = player_ofa.get_position()

		if unit_x < pl_x:
			self.move_right()
		elif unit_x > pl_x:
			self.move_left()

		if unit_y < pl_y:
			self.move_down()
		elif unit_y > pl_y:
			self.move_up()


unit.unit_types["TeddyGhostUnit"] = TeddyGhostUnit