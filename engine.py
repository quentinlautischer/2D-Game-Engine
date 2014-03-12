import sys, pygame, random
from animation import Animation
from operator import itemgetter, attrgetter

class ENGINE(object):

	def __init__(self, screen, gui, unit_roster, maps):
		self.unit_roster = unit_roster
		self.screen = screen
		self.gui = gui
		self.maps = maps

		self.FPS = 30
		self.controller1 = self.Controller1(unit_roster[0])
		self.controller2 = self.Controller2(unit_roster[1])

	def update_logic(self):
		pygame.time.wait(int(1000/self.FPS))

		player1 = self.unit_roster[0]
		player2 = self.unit_roster[1]

		if (player1.xpos > 800 or player2.xpos > 800) and 1:#scroll_available <- comes from game script
			self.maps.is_map_scrolling = 1
			player1.xpos = 100
			player2.xpos = 100


		#current_time  = pygame.time.get_ticks()
		if player1.get_health() > 0:	
			#player1.lose_health(0.1)
			self.controller1.update(player1)
			player1.gain_energy(0.3)
			if not player1.dmg_dealt:
				player1.check_dmg_done(self.unit_roster)
				player1.dmg_dealt = True
		else:
			player1.dead = True

			#current_time  = pygame.time.get_ticks()
		if player2.get_health() > 0:	
			#player2.lose_health(0.1)
			self.controller2.update(player2)
			player2.gain_energy(0.3)
			if not player2.dmg_dealt:
				player2.check_dmg_done(self.unit_roster)
				player2.dmg_dealt = True
		else:
			player2.dead = True

		for unit in self.unit_roster[2::]:

			#current_time  = pygame.time.get_ticks()
			if unit.get_health() > 0:	
				unit.gain_energy(0.3)
				if not unit.dmg_dealt:
					unit.check_dmg_done(self.unit_roster)
					unit.dmg_dealt = True
			else:
				if not unit.dead:
					unit.dead_time = pygame.time.get_ticks()
				unit.dead = True
				if unit.dead_time + 5000 < pygame.time.get_ticks():
					self.unit_roster.remove(unit)

	def draw_overhead_health(self, unit):
		bar_height = 10
		pygame.draw.rect(self.screen, (200, 50, 50), (unit.xpos, unit.ypos-unit.height-bar_height, unit.width, bar_height), 0)
		pygame.draw.rect(self.screen, (0, 200, 50), (unit.xpos, unit.ypos-unit.height-bar_height, (unit.health / unit.health_max)*unit.width, bar_height), 0)

	def update_draw(self):

		self.maps.sky_draw()
		self.screen.blit(self.maps.current_bg, (0, 150))

		if self.unit_roster[0].dead and self.unit_roster[1].dead:
			self.maps.sky_color_default = (150, 50, 50)

		if self.maps.is_map_scrolling:
			self.maps.scroll_map_right()
		
		# Draw GUI
		self.gui.draw(self.unit_roster)
		#self.gui.draw_update(self.unit_roster)

		#Sort Roster from smallest ypos to largest This enable depth drawing.
		depth_sort = []
		for unit in self.unit_roster:
			depth_sort.append((unit, unit.ypos))
		depth_sort = sorted(depth_sort, key=lambda unit: unit[1])
		for unit, ypos in depth_sort:
			self.draw_players(unit)
			if unit.name == 'enemy':
				self.draw_overhead_health(unit)


		#self.draw_players(self.unit_roster[0])
		#self.draw_players(self.unit_roster[1])
		#Update whole screen
		pygame.display.update()

	def draw_players(self, player):

		if not player.dead:
			if player.attack_status == "none" and player.is_walking == 0:
				
				player.position_update()
				
				#Uncomment for hitbox

				#pygame.draw.rect(self.screen, (200, 200, 200), ((player.xpos, player.ypos-player.height), (player.width, player.height)), 0)
				#pygame.draw.rect(self.screen, (100, 100, 200), ((player.xpos, player.ypos), (3, 3)), 0)
				#self.screen.blit(player.anim_standing[0], (player.xpos, player.ypos-player.height))
				Animation(self.screen, player, 0, player.anim_standing, 10).animate()
			
			if player.is_walking and player.attack_status == "none" :
				player.draw_walking(self.screen)

			if player.attack_status == "one":
				player.draw_atk1(self.screen)
			
			if player.attack_status == "two":
				player.draw_atk2(self.screen)
			
			if player.attack_status == "DOOM":
				for i in self.unit_roster:
					if i.name != "Switch" and i.name != "If":
						i.health = 0
				player.attack_status = "none"
		else:
			self.screen.blit(player.anim_death, (player.xpos, player.ypos-player.height))


	class Controller1(object):
	#This is the keyboard controller for Player 1
		
		def __init__(self, player):
			self.player = player
			self.K_LEFT = pygame.K_LEFT
			self.K_RIGHT = pygame.K_RIGHT
			self.K_DOWN = pygame.K_DOWN
			self.K_UP = pygame.K_UP

			self.K_1 = pygame.K_1
			self.K_2 = pygame.K_2
			self.K_9 = pygame.K_9
		
		
		def update(self, player):
			
			#KEY DOWN REPEAT MOVES
			keys=pygame.key.get_pressed()
			self._LEFT(keys, player)
			self._RIGHT(keys, player)
			self._DOWN(keys, player)
			self._UP(keys, player)
			self._1(keys, player)
			self._2(keys, player)
			self._9(keys, player)

		def _LEFT(self, keys, player):
			if keys[self.K_LEFT]:
			        player.move_left()

		def _RIGHT(self, keys, player):	
			if keys[self.K_RIGHT]:  
			        player.move_right()

		def _DOWN(self, keys, player):
			if keys[self.K_DOWN]:
			        player.move_down()

		def _UP(self, keys, player):	
			if keys[self.K_UP]:
			        player.move_up()

		def _1(self, keys, player):	
			if keys[self.K_1]:
				player.attack_spell("one")
		
		def _2(self, keys, player):	
			if keys[self.K_2]:
				player.attack_spell("two")

		def _9(self, keys, player):
			if keys[self.K_9]:
				player.attack_spell("DOOM")


	class Controller2(Controller1):
		#This is the arduino server controller
		def __init__(self, player):
			self.player = player
			self.K_LEFT = pygame.K_j
			self.K_RIGHT = pygame.K_l
			self.K_DOWN = pygame.K_k
			self.K_UP = pygame.K_i

			self.K_1 = pygame.K_7
			self.K_2 = pygame.K_8
			self.K_9 = pygame.K_9

class LoadImages(object):

	def __init__(self, dir, images):
		self.dir = dir
		self.images = images
		self.sequence = self.load_images()
	
	def load_images(self):
		sequence = []

		for i in self.images:
			sequence.append(pygame.image.load(self.dir + i))
		sequence.append(0) #frame tracker
		sequence.append(1) #rate tracker
		return sequence

def in_range_cross(unit, target, range_x, range_y, direction):
	xdist = abs(unit.xpos - target.xpos)
	ydist = abs(unit.ypos - target.ypos)
	print("xdist: " + str(xdist) + " ydist: " + str(ydist))

	if ydist < range_y:
		if direction == 'right':
			if target.xpos > unit.xpos:
				if range_x + unit.width > abs(xdist) :
					return True
				return False

		else: #Directection == 'left'
			if target.xpos < unit.xpos:
				if xdist < range_x + target.width:
					return True
				return False

def detect_collision(unit, objects):
	for obj in objects:
		if obj != unit:
			return in_range_cross(unit, obj, 0, 40, unit.direction)
		return False

def straight_line_dist(x1, y1, x2, y2):
	return ((x2-x1)**2 + (y2-y1)**2)**0.5