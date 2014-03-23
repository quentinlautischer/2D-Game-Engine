#Werewolf
from animation import LoadImages
from unit.base_unit import BaseUnit
from unit.base_enemy_unit import BaseEnemyUnit
from animation import Animation
import unit
from ai import AI

class WerewolfUnit(BaseEnemyUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand_frame0.png","stand_frame1.png", "stand_frame2.png"]).sequence
		self.anim_walking = LoadImages(dirr, ["walking_frame0.png","walking_frame1.png", "walking_frame2.png", "walking_frame3.png"]).sequence
		self.anim_warn1 = LoadImages(dirr, ["Slash0_Frame0.png","Slash0_Frame1.png","Slash0_Frame2.png","Slash0_Frame3.png","Slash0_Frame3.png","Slash0_Frame2.png","Slash0_Frame1.png","Slash0_Frame0.png"]).sequence 
		self.anim_atk1 = LoadImages(dirr, ["Slash0_Frame0.png","Slash0_Frame1.png","Slash0_Frame2.png","Slash0_Frame3.png","Slash0_Frame4.png","Slash0_Frame5.png","Slash0_Frame6.png","Slash0_Frame7.png","Slash0_Frame8.png","Slash0_Frame9.png"]).sequence
		self.anim_death = LoadImages(dirr, ["death_frame0.png","death_frame1.png","death_frame2.png","death_frame3.png","death_frame4.png","death_frame5.png","death_frame6.png","death_frame7.png"]).sequence	
		self.attacks_dict = {"one": {"energy": 10, "dmg": 50, "x_range": 150, "y_range": 120},
						"two": {"energy": 10, "dmg": 10, "x_range": 40, "y_range": 40},
						"DOOM": {"energy": 0, "dmg": 100, "x_range": 50, "y_range": 50}}

		self.width = 136  #self.anim_standing[0].get_rect().size[0] 
		self.height = 160 #self.anim_standing[0].get_rect().size[1]
		self.health_max = 1000
		self.health = self.health_max
		self.step_horz = 8
		self.step_vert = 8

		self.AI = AI(self,[])

		self.AI.sequence.append([self.Approach])

		#self.ai_Attack
		#self.ai_sequence0 = [self.move_right, self.move_right, self.move_right, self.queue_warn1, self.queue_warn1, self.queue_attack1]
		#self.ai_sequence1 = [self.move_left, self.move_left, self.move_left]

		#self.AI = AI(self, [self.ai_sequence0, self.ai_sequence1,self.ai_Approach])
	
	def draw_atk1(self, screen):
		#Stab
		rate = 1
		Animation(screen, self, 0, self.anim_atk1, rate).animate()
		#Animation(screen, self, self.width, self.stab_effect, rate).animate()
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

	def AI_update(self):
		#self.attack_status = "one"
		#self.check_dmg_done(self.unit_roster)
		self.AI.seq_execute(0)

	def queue_warn1(self):
		self.attack_status = "warn1"


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


unit.unit_types["WerewolfUnit"] = WerewolfUnit