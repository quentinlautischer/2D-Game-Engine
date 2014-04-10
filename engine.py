import sys, pygame, random, serial
from animation import Animation
from operator import itemgetter, attrgetter
from scripting import Script
from sounds import SoundManager


class ENGINE(object):
	"""
	Main Game Engine. Game loop uses methods within this engine this is the heart 
	of the operation.

	Logic loop and Draw loop are defined here along with controller update loops
	"""

	def __init__(self, screen, gui, unit_roster, maps, script):
		self.unit_roster = unit_roster
		self.screen = screen
		self.gui = gui
		self.maps = maps
		self.script = script
		self.game_over = True
		self.FPS = 25
		self.player1_port = "COM4"
		self.player2_port = "COM3"

		#Initialize Controllers
		#Enables both the keyboard controls and optional Arduino controllers under
		#Defined ports.

		# 2 Player
		if len(self.unit_roster.get("Players")) > 1:
			#init Keyboard Controllers
			self.controllers = [Controller1(unit_roster.get("Players")[0]),Controller2(unit_roster.get("Players")[1])]
			
			#Attempt to establish arduino Controllers
			try:
				self.controllers.append(Controller_Arduino(unit_roster.get("Players")[0], self.player1_port))
			except:
				print("No COM3")
			try:
				self.controllers.append(Controller_Arduino(unit_roster.get("Players")[1], self.player2_port))
			except:
				print("No COM4")

		# 1 Player
		else:
			#Init Keyboard Controller
			
			self.controllers = [Controller1(unit_roster.get("Players")[0])]
			#Attempt to establish arduino Controller
			try:
				self.controllers.append(Controller_Arduino(unit_roster.get("Players")[0], self.player1_port))
			except:
				print("No COM3")
	
	def update_logic(self):
		"""	
		Update Logic runs through all player movement, controller inputs,
		player attack_status, checks for game_over or map scroll advance.
		Anything that involves changing numbers is done here.
		"""
		#Limit logic loop by frames per second
		pygame.time.wait(int(1000/self.FPS))

		#If all players are dead game over is enabled.
		self.game_over = True
		for Players in self.unit_roster.get("Players"):
			if Players.dead == False:
				self.game_over = False

		# Update Script (Event Handler responsible for spawning monsters, printing quest text, enabling scroll)
		self.script.update_script()

		
		# Player Loop
		for player in self.unit_roster.get("Players"):

			# If scroll available and player at edge scroll change map
			if player.xpos > 900 and self.script.scroll_available:
				self.script.text_print = 0
				self.maps.is_map_scrolling = 1
				spawn_players(self.unit_roster.get("Players"))
				# If player has died remove from Roster
				for unit in self.unit_roster.get("Players"):
					if unit.dead:
						self.unit_roster.get("Players").remove(unit)

			#Player is still alive
			if player.get_health() > 0:	
				#Update Controller (Get input)
				for control in self.controllers:
					if control.player == player:
						control.update()
				#Check for defense
				if player.defending:
					player.defend_spell()
				else:
					player.armor = 1

				#passive health/energy restore
				player.gain_energy(0.3)
				player.gain_health(0.1)

				#If player has triggered attack in controller update
				#but not yet dealt possible dmg to surroundings do it.
				#Only if possible to dmg enemies, unless duel mode is active.
				if not player.dmg_dealt:
					SoundManager.play(player.atk1_sound)
					player.check_dmg_done(self.unit_roster.get("Enemies"))
					if self.script.duel_mode:
						player.check_dmg_done(self.unit_roster.get("Players"))
					player.dmg_dealt = True
			
			#Player is not alive
			else: # health < 0
				player.dead = True

		#Enemy Loop (Very similar to Player Loop)
		for unit in self.unit_roster.get("Enemies"):

			#Enemie is alive
			if unit.get_health() > 0:	
				unit.gain_energy(0.3)
				#This is basically AI version of Controller update
				unit.AI_update(self.screen)

				#If possible to deal dmg do it.
				if not unit.dmg_dealt:
					SoundManager.play(unit.atk1_sound)
					unit.check_dmg_done(self.unit_roster.get("Players"))
					unit.dmg_dealt = True
			else: # Enemy is dead
				#Remove from roster and feild after despawn time
				despawn_time = 2000
				if not unit.dead:
					unit.dead_time = pygame.time.get_ticks()
				unit.dead = True
				if unit.dead_time + despawn_time < pygame.time.get_ticks():
					self.unit_roster.get("Enemies").remove(unit)

	def draw_overhead_health(self, unit):
		"""
		Draw a health bar over enemy units.
		Uses a stored list of dmg done to display
		dmg dealt overhead
		"""
		bar_height = 10 #offset from unit image
		#Add dmg to dmg list
		if unit.health != unit.last_health:
			unit.dmg_done_to_me.append((unit.last_health-unit.health,1))
		#Draw Dmg Dealt over head
		for i in unit.dmg_done_to_me:
			dmg, count = i
			font = pygame.font.Font(None, 56)
			text = font.render(str(dmg), 1, (255, 255, 255))
			self.screen.blit(text, (unit.xpos, unit.ypos-unit.height-bar_height-bar_height-(10*count), unit.width, bar_height))
			unit.dmg_done_to_me.pop(0)
			if count < 10:
				unit.dmg_done_to_me.append((dmg, count+1))

		#Draw healthbar overhead
		pygame.draw.rect(self.screen, (200, 50, 50), (unit.xpos, unit.ypos-unit.height-bar_height, unit.width, bar_height), 0)
		pygame.draw.rect(self.screen, (0, 200, 50), (unit.xpos, unit.ypos-unit.height-bar_height, (unit.health / unit.health_max)*unit.width, bar_height), 0)
		unit.last_health = unit.health
	
	def update_draw(self):
		"""
		Big Draw Loop.
		Handles all the screen printing that runs the graphics for the game.
		From printing the map to the units.
		"""
		#Draw Sky farthest background
		self.maps.sky_draw()
		#Draw Walking Ground Backgroud
		self.screen.blit(self.maps.current_bg, (0, 0))

		"""
		Uncomment the following line to see grid printed
		on during the game. (Very demanding/ may slow game)
		"""
		#self.maps.draw_grid()

		# If one player is dead color the sky red
		for player in self.unit_roster.get("Players"):
			if player.dead:
				self.maps.sky_color_default = (150, 50, 50)

		#Scroll effect / Transition between map grids
		if self.maps.is_map_scrolling:
			self.maps.scroll_map_right()
			self.script.update_quest()
		
		# Draw Interface bar
		self.gui.draw(self.unit_roster)

		"""
		Appends all units to one list then sorts list by the y position which
		is used as depth to give the impression of a 2.5 Dimention.
		"""
		depth_sort = []
		for unit in self.unit_roster.get("Players"):
			depth_sort.append((unit, unit.ypos))
		for unit in self.unit_roster.get("Enemies"):
			depth_sort.append((unit, unit.ypos))	
		depth_sort = sorted(depth_sort, key=lambda unit: unit[1])
		for unit, ypos in depth_sort:
			self.draw_players(unit)
			if unit.name == 'enemy':
				self.draw_overhead_health(unit)

		#Draw any forground object. These are drawn ontop of everything else
		self.screen.blit(self.maps.current_fg, (0, 0))

		#If scroll available print an arrow indication allowed advancement
		if self.script.scroll_available:
			arrow = pygame.image.load("images/arrow_scroll.png")
			self.screen.blit(arrow, (975, 300))

		#Print Quest Text
		if self.script.text_print:
			self.script.update_quest_text()

		#Print Game Over screen
		if self.game_over:
			self.gui.gameover_draw()

		pygame.display.update()

	def draw_players(self, player):
		"""
		Draws players animation sequence for whatever
		attack_status he is currently in.
		"""

		if not player.dead:			
			player.position_update()
			if player.attack_status == "none" and player.is_walking == 0:			
				
				'''
				# Uncomment for hit box
				pygame.draw.rect(self.screen, (100, 100, 200), ((player.unit_box._xl, player.unit_box._yt), (3,3)), 0)
				pygame.draw.rect(self.screen, (100, 100, 200), ((player.unit_box._xl, player.unit_box._yb), (3,3)), 0)
				pygame.draw.rect(self.screen, (100, 100, 200), ((player.unit_box._xr, player.unit_box._yt), (3,3)), 0)
				pygame.draw.rect(self.screen, (100, 100, 200), ((player.unit_box._xr, player.unit_box._yb), (3,3)), 0)
				'''
				Animation(self.screen, player, 0,0, player.anim_standing, 10).animate()
			
			if player.is_walking and player.attack_status == "none" :
				player.draw_walking(self.screen)

			if player.attack_status == "one":
				player.draw_atk1(self.screen)
			
			if player.attack_status == "two":
				player.draw_atk2(self.screen)
			
			if player.attack_status == "warn1":
				player.draw_warn1(self.screen)

			if player.attack_status == "special":
				player.special_atk(self.screen)

			if player.defending:
				self.screen.blit(player.block_img, (player.xpos-player.width/2, player.ypos-player.height))
				player.defending = 0

		else:
			player.draw_death(self.screen)

def initialize_serial(port, speed):
	"""
	Init serial port
	"""
	ser = serial.Serial(port, speed)
	return ser
		
class Controller(object):
	"""
	Controller receives inputs and acts on them
	accordingly.

	Calling Controller.update() will run through
	multiple methods which check for keypresses
	and then execute methods() based on the
	keypress.
	"""
	def __init__(self, player):
		self.player = player
		
	def update(self):
	#KEY DOWN REPEAT MOVES
		keys = pygame.key.get_pressed()
		self._LEFT(keys, self.player)
		self._RIGHT(keys, self.player)
		self._DOWN(keys, self.player)
		self._UP(keys, self.player)
		self._ENTER(keys, self.player)

	def _LEFT(self, keys, player):
		if keys[self.K_LEFT]:
			pass

	def _RIGHT(self, keys, player):	
		if keys[self.K_RIGHT]:  
			pass

	def _DOWN(self, keys, player):

		pygame.time.wait(1000)
		if keys[self.K_DOWN]:
			return 1

	def _UP(self, keys, player):
		if keys[self.K_UP]:
			return 1

	def _ENTER(self, keys, player):	
		if keys[self.K_1]:
			return 1

class Controller1(object):
#This is the keyboard controller for Player 1
		
	def __init__(self, player):
		self.player = player
		self.K_LEFT = pygame.K_a
		self.K_RIGHT = pygame.K_d
		self.K_DOWN = pygame.K_s
		self.K_UP = pygame.K_w

		self.K_1 = pygame.K_e
		self.K_2 = pygame.K_r
		self.K_3 = pygame.K_q
		
	def update(self):
		#Get keys pressed
		keys = pygame.key.get_pressed()
		#Check if keypress = move
		self._LEFT(keys, self.player)
		self._RIGHT(keys, self.player)
		self._DOWN(keys, self.player)
		self._UP(keys, self.player)
		self._1(keys, self.player)
		self._2(keys, self.player)
		self._3(keys, self.player)

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

	def _3(self, keys, player):	
		if keys[self.K_3]:
			player.defending = 1

class Controller2(Controller1):
#This is the keyboard controller for Player 2
	def __init__(self, player):
		self.player = player
		self.K_LEFT = pygame.K_j
		self.K_RIGHT = pygame.K_l
		self.K_DOWN = pygame.K_k
		self.K_UP = pygame.K_i

		self.K_1 = pygame.K_o
		self.K_2 = pygame.K_p
		self.K_3 = pygame.K_u

class Controller_Arduino(Controller1):
#This is the Arduino controller
	def __init__(self, player, port):
		self.ser = initialize_serial(port, 9600)
		self.key_queue = []
		self.player = player
		self.K_LEFT = pygame.K_j
		self.K_RIGHT = pygame.K_l
		self.K_DOWN = pygame.K_k
		self.K_UP = pygame.K_i

		self.K_1 = pygame.K_7
		self.K_2 = pygame.K_8
		self.K_3 = pygame.K_9

	def update(self):
		#Receive Keystroke from arduino
		keyStroke = 'None'
		if self.ser.inWaiting():
			Arduino_input = self.ser.read()
			keyStroke = Arduino_input.decode(encoding='UTF-8')
		current_action = keyStroke
		
		#Check is code corresponds to an action
		if current_action == 'L':
			self.player.move_left()
		elif current_action == 'R':
			self.player.move_right()
		elif current_action == 'D':
			self.player.move_down()
		elif current_action == 'U':
			self.player.move_up()

		elif current_action == 'A':
			self.player.attack_spell("one")
		elif current_action == 'B':
			self.player.attack_spell("two")
		elif current_action == 'C':
			self.player.defending = 1
		try:
			#Flush buffer
			#This keeps the controls responsive
			self.ser.flushInput()
		except:
			pass

def in_range_cross(unit, target, range_x, range_y, direction):
	"""
	Checks if a target is within the units range.
	"""
	xdist = abs(unit.xpos - target.xpos)
	ydist = abs(unit.ypos - target.ypos)


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
	
	return False

def detect_collision(unit, objects, offsetx, offsety):
	"""
	Detect if collision between object boxes will occur.
	"""
	for obj in objects:
		if unit != obj:
			if unit.unit_box.collidesWith(obj.unit_box, offsetx, offsety):
				return True
	return False

def straight_line_dist(x1, y1, x2, y2):
	return ((x2-x1)**2 + (y2-y1)**2)**0.5

def is_grid(grid_graph, grid_verts, points):
	"""
	Check if all points are vertices on the current grid
	"""
	for i in points:
		if not grid_graph.is_vertex(grid_verts.get(i)):
			return False
	return True

def spawn_players(player_roster):
	"""
	Spawns players to a pre-determined location
	!!Ran out of time but it should include a collision
	detection
	"""
	player_reposition = 360
	for player in player_roster:
		if not player.dead:
			player.xpos = 80
			player.ypos = player_reposition
			player_reposition += 64

def spawn_enemy_specified_loc(unit_roster, maps, enemy_type, number, enemy_sprites, xpos, ypos):
	"""
	Spawns enemies to a pre-determined location
	Do not use a number greater than 4.
	"""
	if number > 4:
		number = 4
	for i in range(number):
		unit_roster.get("Enemies").append(enemy_type(unit_roster, xpos, ypos, "enemy", -2, enemy_sprites, "Bad", maps))
