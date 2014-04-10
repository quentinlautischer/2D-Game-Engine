from animation import LoadImages
from unit.base_unit import BaseUnit
from unit.base_enemy_unit import BaseEnemyUnit
from animation import Animation
from ai import AI
import engine, box, pygame, random, unit

class TeddyGhostUnit(BaseEnemyUnit):
	"""
	Final Boss AI. Contains a few special attacks that make for a challanging fight.
	"""

	def __init__(self, unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords):
		
		super().__init__(unit_roster, xpos, ypos, name, number, dirr, faction, maps, **keywords)
		self.anim_standing = LoadImages(dirr, ["stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png"]).sequence
		self.anim_walking = LoadImages(dirr, ["stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png"]).sequence
		self.anim_atk = LoadImages(dirr, ["stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png","stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png","stand.0.png","stand.1.png", "stand.2.png","stand.3.png","stand.4.png", "stand.5.png"]).sequence
		self.anim_warn1 = LoadImages(dirr, ["attack1.11.png","attack1.10.png", "attack1.9.png","attack1.8.png","attack1.7.png", "attack1.6.png","attack1.5.png","attack1.4.png", "attack1.3.png","attack1.2.png","attack1.1.png", "attack1.0.png"]).sequence
		self.anim_death = LoadImages(dirr, ["die1.0.png","die1.1.png","die1.2.png","die1.3.png","die1.4.png"]).sequence
		self.deathbeam_effect = LoadImages(dirr, ["Deathbeam.png","Deathbeam1.png","Deathbeam.png","Deathbeam1.png","Deathbeam.png","Deathbeam1.png","Deathbeam.png","Deathbeam1.png","Deathbeam.png","Deathbeam1.png","Deathbeam.png","Deathbeam1.png","Deathbeam.png","Deathbeam1.png","Deathbeam.png","Deathbeam1.png"]).sequence
		self.special_atk1 = LoadImages("images/teddyghost/", ["skill.12111006.ball.0.png","skill.12111006.ball.1.png", "skill.12111006.ball.2.png","skill.12111006.ball.3.png","skill.12111006.ball.4.png", "skill.12111006.ball.5.png","skill.12111006.ball.6.png", "skill.12111006.ball.7.png"]).sequence
		self.attacks_dict = {"one": {"energy": 10, "dmg": 5, "x_range": 1000, "y_range": 50},
						"two": {"energy": 10, "dmg": 10, "x_range": 40, "y_range": 50}}

		self.width = 136  #self.anim_attack1ing[0].get_rect().size[0] 
		self.height = 160 #self.anim_skill.12111006.balling[0].get_rect().size[1]
		self.health_max = 1000
		self.health = self.health_max
		self.step_horz = 32
		self.step_vert = 32
		self.special_casting = 0
		self.special_counter = pygame.time.get_ticks() - 20000
		self.atk1_sound = "death_beam_sound"
		self.special_offset = 50
		self.special_dmg = 2
		self.AI = AI(self,[[self.Approach],[self.queue_special],[self.queue_warn1]])
		
		self.wave_position = [300,375,450,525,600]
		self.temp_wave = []
		#I HAVE NO IDEA WHY BUT THIS NUMBER MUST BE A MULTIPLE OF 3 FOR ANIMATION TO WORK PROPER
		for i in range(12):
			self.temp_wave.append(random.sample(self.wave_position, len(self.wave_position)-1))
	
	def special_atk(self, screen):
		"""
		Spawns players at one side of map and himself at the other then
		creates waves of fire missles that must be dodged by the players.

		"""
		if not self.special_casting:
			engine.spawn_players(self.unit_roster.get("Players"))
			self.xpos = 750
			self.ypos = 450
			self.special_casting = 1
			self.special_cast_time = pygame.time.get_ticks()
			self.special_missles_box = []
			for j in range(len(self.temp_wave)):
				for i in range(len(self.temp_wave[j])):
					self.special_missles_box.append(self.FireMissle(self.unit_roster, 900+(j*300), self.temp_wave[j][i]))

		else:
			Animation(screen, self, 0,0, self.anim_standing, 1).animate()

			for missle in self.special_missles_box:
				Animation(screen, missle , 0,0, self.special_atk1, 10).animate()
				missle.move_left()

			#check for dmgs.
			for unit in self.unit_roster.get("Players"):
				if engine.detect_collision(unit, self.special_missles_box, 0, 0):
					unit.lose_health(self.special_dmg)

			if pygame.time.get_ticks() > self.special_cast_time + 20000:
				self.special_casting = 0
				self.special_offset = 0
				self.attack_status = "none"

	def update_box(self):
		return box.Box(self.xpos,self.ypos-self.height,self.xpos+self.width,self.ypos)

	def detect_collision_with_fire_missle(self, unit, objects, offsetx, offsety):

		for obj in objects:
			if unit != obj:
				if unit.unit_box.collidesWith(obj, offsetx, offsety):
					return True
		return False



	def AI_update(self, screen):
	
		if not self.special_casting:
			if self.attack_status == "none":
				if self.special_counter + 30000 < pygame.time.get_ticks():
					self.special_counter = pygame.time.get_ticks()
					self.queue_special()
				else:
					if self.check_attack_1():
						self.AI.seq_execute(2)
					else:
						self.attack_status = "none"
						self.AI.seq_count = 0
						self.AI.seq_execute(0)


	def draw_atk1(self, screen):
		#Stab
		self.dmg_dealt = False
		rate = 1
		Animation(screen, self, 0,0, self.anim_atk, 1).animate()
		Animation(screen, self, 550, 0, self.deathbeam_effect, rate).animate()
		if self.deathbeam_effect[-2] == len(self.deathbeam_effect) - 3 and self.deathbeam_effect[-1] == rate-1:
			Animation(screen, self, 550,0, self.deathbeam_effect, 5).animate()
			self.deathbeam_effect[-2] = 0
			self.attack_status = "none"
			self.dmg_dealt = True

	def draw_warn1(self, screen):
		#Stab
		rate = 4
		Animation(screen, self, 0,0, self.anim_warn1, rate).animate()
		if self.anim_warn1[-2] == len(self.anim_warn1) - 3 and self.anim_warn1[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_warn1, 5).animate()
			self.anim_warn1[-2] = 0
			self.attack_status = "one"


	def draw_atk2(self, screen):
		#slash
		rate = 3
		Animation(screen, self, 0,0, self.anim_atk2, rate).animate()
		Animation(screen, self, self.width,0, self.slash_effect, rate).animate()
		if self.anim_atk2[-2] == len(self.anim_atk2) - 3 and self.anim_atk2[-1] == rate-1:
			Animation(screen, self, 0,0, self.anim_atk2, 5).animate()
			self.anim_atk2[-2] = 0
			self.attack_status = "none"

	def queue_warn1(self):
		self.attack_status = "warn1"

	def queue_special(self):
		self.attack_status = "special"
		engine.spawn_players(self.unit_roster.get("Players"))
		self.xpos = 750
		self.ypos = 450
		self.special_casting = 1
		self.special_cast_time = pygame.time.get_ticks()
		self.special_missles_box = []
		for j in range(len(self.temp_wave)):
			for i in range(len(self.temp_wave[j])):
				self.special_missles_box.append(self.FireMissle(self.unit_roster, 900+(j*300), self.temp_wave[j][i]))

	class FireMissle(object):
		"""
		The Fire missles are objects with hitboxes used to determine
		collision with opposing players.
		"""

		def __init__(self, unit_roster, xpos, ypos):
			self.unit_roster = unit_roster
			self.height = 60
			self.width = 145
			self.speed = 12
			self.direction = 'left'
			self.xpos = xpos
			self.ypos = ypos
			self.unit_box = self.update_box()
			self.special_atk1 = LoadImages("images/teddyghost/", ["skill.12111006.ball.0.png","skill.12111006.ball.1.png", "skill.12111006.ball.2.png","skill.12111006.ball.3.png","skill.12111006.ball.4.png", "skill.12111006.ball.5.png","skill.12111006.ball.6.png", "skill.12111006.ball.7.png"]).sequence

		def update_box(self):
			return box.Box(self.xpos+20, self.ypos-self.height+20, self.xpos+self.width-20, self.ypos+30)

		def move_left(self):
			self.xpos -= self.speed
			self.unit_box = self.update_box()

unit.unit_types["TeddyGhostUnit"] = TeddyGhostUnit