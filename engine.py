import sys, pygame, random, serial
from animation import Animation
from operator import itemgetter, attrgetter
from scripting import Script
from sounds import SoundManager


class ENGINE(object):

	def __init__(self, screen, gui, unit_roster, maps, script):
		self.unit_roster = unit_roster
		self.screen = screen
		self.gui = gui
		self.maps = maps
		self.script = script
		self.game_over = True

		self.FPS = 25
		self.controllers = [Controller_Arduino(unit_roster.get("Players")[0], "COM3"),Controller_Arduino(unit_roster.get("Players")[1],"COM4")]
		
	def update_logic(self):
		pygame.time.wait(int(1000/self.FPS))
		#Check if current grid quests are complete, if yes then allow scroll
		self.game_over = True
		for Players in self.unit_roster.get("Players"):
			if Players.dead == False:
				self.game_over = False

		self.script.update_script()

		for player in self.unit_roster.get("Players"):
			if player.xpos > 900 and self.script.scroll_available:
				self.script.text_print = 0
				self.maps.is_map_scrolling = 1
				spawn_players(self.unit_roster.get("Players"))


			#current_time  = pygame.time.get_ticks()
			if player.get_health() > 0:	
				#player.lose_health(0.1)
				self.controllers[player.number-1].update(player)
				if player.defending:
					player.defend_spell()
				else:
					player.armor = 1
				player.gain_energy(0.3)
				player.gain_health(0.1)
				if not player.dmg_dealt:
					SoundManager.play(player.atk1_sound)
					player.check_dmg_done(self.unit_roster.get("Enemies"))
					player.dmg_dealt = True
			else:
				player.dead = True


		for unit in self.unit_roster.get("Enemies"):
			#current_time  = pygame.time.get_ticks()
			if unit.get_health() > 0:	
				unit.gain_energy(0.3)
				unit.AI_update(self.screen)

				if not unit.dmg_dealt:
					SoundManager.play(unit.atk1_sound)
					unit.check_dmg_done(self.unit_roster.get("Players"))
					unit.dmg_dealt = True
			else:
				if not unit.dead:
					unit.dead_time = pygame.time.get_ticks()
				unit.dead = True
				unit.is_passable = 1
				if unit.dead_time + 2000 < pygame.time.get_ticks():
					self.unit_roster.get("Enemies").remove(unit)

	def draw_overhead_health(self, unit):
		bar_height = 10
		if unit.health != unit.last_health:
			unit.dmg_done_to_me.append((unit.last_health-unit.health,1))
		for i in unit.dmg_done_to_me:
			dmg, count = i
			font = pygame.font.Font(None, 56)
			text = font.render(str(dmg), 1, (255, 255, 255))
			self.screen.blit(text, (unit.xpos, unit.ypos-unit.height-bar_height-bar_height-(10*count), unit.width, bar_height))
			unit.dmg_done_to_me.pop(0)
			if count < 10:
				unit.dmg_done_to_me.append((dmg, count+1))

		pygame.draw.rect(self.screen, (200, 50, 50), (unit.xpos, unit.ypos-unit.height-bar_height, unit.width, bar_height), 0)
		pygame.draw.rect(self.screen, (0, 200, 50), (unit.xpos, unit.ypos-unit.height-bar_height, (unit.health / unit.health_max)*unit.width, bar_height), 0)
		unit.last_health = unit.health
	
	def update_draw(self):

		self.maps.sky_draw()
		self.screen.blit(self.maps.current_bg, (0, 0))

		#self.maps.draw_grid()

		for player in self.unit_roster.get("Players"):
			if player.dead:
				self.maps.sky_color_default = (150, 50, 50)

		if self.maps.is_map_scrolling:
			self.maps.scroll_map_right()
			self.script.update_quest()
		
		# Draw GUI
		self.gui.draw(self.unit_roster)
		#self.gui.draw_update(self.unit_roster)

		#Sort Roster from smallest ypos to largest This enable depth drawing.
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

		self.screen.blit(self.maps.current_fg, (0, 0))

		if self.script.scroll_available:
			arrow = pygame.image.load("images/arrow_scroll.png")
			self.screen.blit(arrow, (975, 300))

		if self.script.text_print:
			self.script.update_quest_text()

		if self.game_over:
			self.gui.gameover_draw()

		#self.draw_players(self.unit_roster[0])
		#self.draw_players(self.unit_roster[1])
		#Update whole screen
		#pygame.transform.scale2x()



		pygame.display.update()

	def draw_players(self, player):

		if not player.dead:			
			player.position_update()
			if player.attack_status == "none" and player.is_walking == 0:
				
				
				
				#Uncomment for hitbox

				#pygame.draw.rect(self.screen, (200, 200, 200), ((player.xpos, player.ypos-player.height), (player.width, player.height)), 0)
				#pygame.draw.rect(self.screen, (100, 100, 200), ((player.xpos, player.ypos), (3, 3)), 0)
				#grid = player.generate_unit_grid_frame(0, 0)
				#for i in grid:
				#	pygame.draw.rect(self.screen, (100, 100, 200), (i, (3,3)), 0)
				#self.screen.blit(player.anim_standing[0], (player.xpos, player.ypos-player.height))
				
				pygame.draw.rect(self.screen, (100, 100, 200), ((player.unit_box._xl, player.unit_box._yt), (3,3)), 0)
				pygame.draw.rect(self.screen, (100, 100, 200), ((player.unit_box._xl, player.unit_box._yb), (3,3)), 0)
				pygame.draw.rect(self.screen, (100, 100, 200), ((player.unit_box._xr, player.unit_box._yt), (3,3)), 0)
				pygame.draw.rect(self.screen, (100, 100, 200), ((player.unit_box._xr, player.unit_box._yb), (3,3)), 0)

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


# Some little helper functions to help ease readability
def initialize_serial(port, speed):
    ser = serial.Serial(port, speed)
    return ser
		
class Controller(object):
	def __init__(self, player):
		pass
		
	def update(self, player):
	#KEY DOWN REPEAT MOVES
		keys = pygame.key.get_pressed()
		self._LEFT(keys, player)
		self._RIGHT(keys, player)
		self._DOWN(keys, player)
		self._UP(keys, player)
		self._ENTER(keys, player)

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
		self.K_LEFT = pygame.K_LEFT
		self.K_RIGHT = pygame.K_RIGHT
		self.K_DOWN = pygame.K_DOWN
		self.K_UP = pygame.K_UP

		self.K_1 = pygame.K_1
		self.K_2 = pygame.K_2
		self.K_3 = pygame.K_3
		
	def update(self, player):
			
		#KEY DOWN REPEAT MOVES
		keys = pygame.key.get_pressed()
		self._LEFT(keys, player)
		self._RIGHT(keys, player)
		self._DOWN(keys, player)
		self._UP(keys, player)
		self._1(keys, player)
		self._2(keys, player)
		self._3(keys, player)

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
#This is the arduino server controller
	def __init__(self, player):
		self.ser = initialize_serial("COM4", 9600)

		self.player = player
		self.K_LEFT = pygame.K_j
		self.K_RIGHT = pygame.K_l
		self.K_DOWN = pygame.K_k
		self.K_UP = pygame.K_i

		self.K_1 = pygame.K_7
		self.K_2 = pygame.K_8
		self.K_3 = pygame.K_9

class Controller_Arduino(Controller1):
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

	def update(self, player):
		keyStroke = 'None'
		if self.ser.inWaiting():
			Arduino_input = self.ser.read()
			keyStroke = Arduino_input.decode(encoding='UTF-8')
			self.key_queue.append(keyStroke)
			
		#KEY DOWN REPEAT MOVES
		current_action = keyStroke
		
		print(current_action)
		if current_action == 'L':
			player.move_left()
		elif current_action == 'R':
			player.move_right()
		elif current_action == 'D':
			player.move_down()
		elif current_action == 'U':
			player.move_up()

		elif current_action == 'A':
			player.attack_spell("one")
		elif current_action == 'B':
			player.attack_spell("two")
		elif current_action == 'C':
			player.defending = 1
		try:
			self.ser.flushInput()
		except:
			pass

class LoadImagesSheet(object):

	def __init__(self, dirr, images):
		self.dir = dirr
		self.images = images

	def load_images_sheet(self, sprt_len_x, sprt_len_y, crnr_x, crnr_y, length):
		sequence = []
		###########
		sheet = pygame.image.load(self.dirr + self.images)

		for i in range(length):
			sheet.set_clip(pygame.Rect(crnr_x, crnr_y, sprt_len_x, sprt_len_y))
			sequence.append(sheet.subsurface(sheet.get_clip()))
			crnr_x += sprt_len_x  

		###########
		sequence.append(0) #frame tracker
		sequence.append(1) #rate tracker
		return sequence


def in_range_cross(unit, target, range_x, range_y, direction):
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

	for obj in objects:
		if unit != obj:
			if unit.unit_box.collidesWith(obj.unit_box, offsetx, offsety):
				return True
	return False

def straight_line_dist(x1, y1, x2, y2):
	return ((x2-x1)**2 + (y2-y1)**2)**0.5

def is_grid(grid_graph, grid_verts, points):
	for i in points:
		if not grid_graph.is_vertex(grid_verts.get(i)):
			return False
	return True

def spawn_players(player_roster):
	player_reposition = 360
	for player in player_roster:
		player.xpos = 80
		player.ypos = player_reposition
		player_reposition += 64

def spawn_enemy_specified_loc(unit_roster, maps, enemy_type, number, enemy_sprites, xpos, ypos):
		for i in range(number):
			unit_roster.get("Enemies").append(enemy_type(unit_roster, xpos, ypos, "enemy", -2, enemy_sprites, "Bad", maps))

def spawn_enemy_random_loc(unit_roster, maps, enemy_type, number, enemy_sprites, xpos, ypos):
		for i in range(number):
			unit_roster.get("Enemies").append(enemy_type(unit_roster, xpos, ypos, "enemy", -2, enemy_sprites, "Bad", maps))