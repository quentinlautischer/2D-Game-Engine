from animation import LoadImages
from unit.base_unit import BaseUnit
from unit.base_enemy_unit import BaseEnemyUnit
from animation import Animation
import unit
from ai import AI
import engine
import box
import pygame

class TeddyGhostUnit(BaseEnemyUnit):

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png"]).sequence
		self.anim_walking = LoadImages(dirr, ["stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png"]).sequence
		self.anim_atk1 = LoadImages(dirr, ["attack1.11.png","attack1.10.png", "attack1.9.png","attack1.8.png","attack1.7.png", "attack1.6.png","attack1.5.png","attack1.4.png", "attack1.3.png","attack1.2.png","attack1.1.png", "attack1.0.png"]).sequence
		self.anim_warn1 = LoadImages(dirr, ["attack1.11.png","attack1.10.png", "attack1.9.png","attack1.8.png","attack1.7.png", "attack1.6.png","attack1.5.png","attack1.4.png", "attack1.3.png","attack1.2.png","attack1.1.png", "attack1.0.png"]).sequence
		self.anim_death = LoadImages(dirr, ["die1.0.png","die1.1.png","die1.2.png","die1.3.png","die1.4.png"]).sequence
		self.deathbeam_effect = LoadImages(dirr, ["Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png","Deathbeam.png"]).sequence
		self.special_atk1 = LoadImages(dirr, ["skill.12111006.ball.0.png","skill.12111006.ball.1.png", "skill.12111006.ball.2.png","skill.12111006.ball.3.png","skill.12111006.ball.4.png", "skill.12111006.ball.5.png","skill.12111006.ball.6.png", "skill.12111006.ball.7.png"]).sequence
		self.attacks_dict = {"one": {"energy": 10, "dmg": 10, "x_range": 1000, "y_range": 20},
						"two": {"energy": 10, "dmg": 10, "x_range": 40, "y_range": 40},
						"DOOM": {"energy": 0, "dmg": 100, "x_range": 50, "y_range": 50}}

		self.width = 136  #self.anim_attack1ing[0].get_rect().size[0] 
		self.height = 160 #self.anim_skill.12111006.balling[0].get_rect().size[1]
		self.health_max = 1000
		self.health = self.health_max
		self.step_horz = 32
		self.step_vert = 32
		self.special_casting = 0
		self.atk1_sound = "death_beam_sound"
		self.special_offset = 50
		self.AI = AI(self,[])
		self.AI.sequence.append([self.Approach])
		self.AI.sequence.append([self.queue_special])
		self.AI.sequence.append([self.queue_warn1, self.queue_attack1])
		self.AI.sequence.append([self.queue_warn1, self.queue_attack1])
		
		self.imgar = pygame.image.load("images/teddyghost/attack1.info.hit.0.png")

	def special_atk(self, screen):
		#Fire Wall
		if not self.special_casting:
			engine.spawn_players(self.unit_roster.get("Players"))
			self.xpos = 800
			self.ypos = 400
			self.special_casting = 1
			self.special_cast_time = pygame.time.get_ticks()

		else:
			Animation(screen, self, 0,0, self.anim_standing, 10).animate()
			Animation(screen, self, self.special_offset+ 64,20, self.special_atk1, 5).animate()
			self.special_offset += 5
			Animation(screen, self, self.special_offset,-30, self.special_atk1, 5).animate()
			Animation(screen, self, self.special_offset,-140, self.special_atk1, 5).animate()
			Animation(screen, self, self.special_offset,130, self.special_atk1, 5).animate()


			if pygame.time.get_ticks() > self.special_cast_time + 10000:
				self.special_casting = 0
				self.special_offset = 0
				self.attack_status = "none"


	def AI_update(self, screen):
		#self.attack_status = "one"
		#self.check_dmg_done(self.unit_roster)
		if not self.special_casting:
			self.AI.seq_execute(1)
			if self.check_attack_2():
				self.AI.seq_execute(2)
			elif self.check_attack_1():
				self.AI.seq_execute(1)
			else:
				self.AI.seq_count = 0
				self.AI.seq_execute(0)
		if self.special_casting:
			self.special_atk(screen)

	def draw_atk1(self, screen):
		#Stab
		rate = 20
		Animation(screen, self, 0,0, self.anim_atk1, rate).animate()
		Animation(screen, self, 550, self.deathbeam_effect, rate).animate()
		if self.anim_atk1[-2] == len(self.anim_atk1) - 3 and self.anim_atk1[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk1, 5).animate()
			self.anim_atk1[-2] = 0
			self.attack_status = "none"

	def draw_warn1(self, screen):
		#Stab
		rate = 4
		Animation(screen, self, 0,0, self.anim_warn1, rate).animate()
		#Animation(screen, self, self.width, self.stab_effect, rate).animate()
		if self.anim_warn1[-2] == len(self.anim_warn1) - 3 and self.anim_warn1[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_warn1, 5).animate()
			self.anim_warn1[-2] = 0
			self.attack_status = "none"


	def draw_atk2(self, screen):
		#slash
		rate = 3
		Animation(screen, self, 0,0, self.anim_atk2, rate).animate()
		Animation(screen, self, self.width, self.slash_effect, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

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

	def queue_special(self):
		self.attack_status = "special"


unit.unit_types["TeddyGhostUnit"] = TeddyGhostUnit