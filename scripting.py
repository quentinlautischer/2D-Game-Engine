import pygame, math, engine
from graph_module import Graph
from animation import *
#Import Enemies that need to be spawned by the script
from unit.teddyghost_unit import TeddyGhostUnit
from unit.werewolf_unit import WerewolfUnit
from unit.goblin_unit import GoblinUnit

class Script(object):
	"""
	This Object deals with the maintenace or script
	and game progression.

	current_grid_quests is a data struction that works as a event queue
	Key is the current map grid. While on a grid the script_update will
	execute through the current grids quest list until it is empty. Once 
	empty it will allow the players to advance to the next map grid.

	The quest come in tuples of at least 2 elements. The second element is
	a label that indicates how the current quest should be handled.

	Labels:

	"quest text": Tuple of 2 elements the first element is used as quest text
	this text will be printed to the screen for a predetermined amount of time.
	This quest  will be remove from the quest queue as soon as it is executed.

	"release wave": Tuple of 5 elements. This will be removed from the quest queue
	upon execution. 1 element is the method call release_wave(), 3 element is the 
	number of enemies released in this wave. 4 element is the type of enemy, 5 is 
	the enemies image file.

	"defeat wave": Tuple of 2. 1st element is Null. When this quest is executed it is not
	cleared from the quest queue until all enemies in the enemy roster are removed. (Killed)
	This will restrict any other quests from being executed until the monsters have been cleared

	"duel": Enables friendly fire. Used at end of game so that if both players are still alive
	they can battle to the death.

	"""

	def __init__(self, unit_roster, maps, screen):
		self.unit_roster = unit_roster
		self.screen = screen
		self.maps = maps
		self.scroll_available = 0
		self.text_print = 1
		self.quest_text = ""
		self.duel_mode = 0
		self.text_display_time = 4000
	
		self.current_grid_quests = {
			0: [("Welcome to the game", "quest text")], #(self.release_wave,"release wave", 1, TeddyGhostUnit, "images/teddyghost/"),(None, "defeat wave")],
			1: [("Defeat the Monsters!", "quest text"),(self.release_wave,"release wave", 4, GoblinUnit, "images/enemy/"), (None, "defeat wave")],
			2: [("Keep Going", "quest text")],
			3: [("Defeat the Monsters!", "quest text"),(self.release_wave,"release wave", 4, GoblinUnit, "images/enemy/"), (None, "defeat wave")],
			4: [("A stronger enemy approaches...", "quest text"), (self.release_wave1, "release wave", 1, WerewolfUnit, "images/werewolf/"), (None, "defeat wave")],
			5: [("Death Teddy Asks that you leave...!", "quest text"),(self.release_wave,"release wave", 1, TeddyGhostUnit, "images/teddyghost/"), (None, "defeat wave"),("Only One Can Be Champion...", "quest text"),("duel", "duel"),("End Quest", "End Quest")]
		}

		self.quest = self.current_grid_quests.get(self.maps.current_grid)

	def update_script(self):
		"""
		Runs through current grids quests executing and removing them
		once conditions are satisfied. 

		If all quests have been completed for a grid. Player advancement
		to the next grid is enabled.
		"""
		if self.quest:
			self.scroll_available = 0
			if self.quest[0][1] == "release wave":
				a,b,c,d,e = self.quest.pop(0)
				a(d, e, c)
			elif self.quest[0][1] == "defeat wave":
				if self.unit_roster.get("Enemies"):
					pass
				else:
					self.quest.pop(0)
			elif self.quest[0][1] == "quest text":
				self.quest_text, b = self.quest.pop(0)
				self.text_timer = pygame.time.get_ticks()
				self.text_print = 1
			elif self.quest[0][1] == "duel":
				self.duel_mode = 1
		else:
			self.scroll_available = 1

		if pygame.time.get_ticks() > self.text_timer + self.text_display_time:
			self.text_print = 0
			self.quest_text = "" 

	def release_wave(self, enemy_type, enemy_img, num):
		#Only allows 4 mobs at a time.
		for i in range(num%5):
			engine.spawn_enemy_specified_loc(self.unit_roster, self.maps, enemy_type, 1, enemy_img, 800, 400+(i*64))
	
	def release_wave1(self, enemy_type, enemy_img, num):
		#Only allows 4 mobs at a time.
		for i in range(num%5):
			engine.spawn_enemy_specified_loc(self.unit_roster, self.maps, enemy_type, 1, enemy_img, 800, 320+(i*256))
	
	def update_quest(self):
		self.quest = self.current_grid_quests.get(self.maps.current_grid)

	def update_quest_text(self):
		font = pygame.font.SysFont("monospace", 50)
		label = font.render(self.quest_text, 1, (255, 255, 255))
		self.screen.blit(label, (100, 125))		
