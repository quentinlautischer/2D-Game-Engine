import sys, pygame
import random

class GUI(object):
	"""
	An object that deals with the game interface. Basically just a fancy bar that holds the health bar.
	This really doesnt do much more than draw deal with that. Oh and it deals with gameover... because why not?
	"""

	def __init__(self, screen, unit_roster):
		self.screen = screen
		self.unit_roster = unit_roster
		self.health_bar_len = 200
		self.panel = pygame.image.load("images/panel1.png")
		self.gameover_img = pygame.image.load("images/Game_over.png")

	def draw(self, unit_roster):
		"""
		Draws inteface based on player information.
		"""
		#Draw Interface Panel
		self.screen.blit(self.panel, (0, -40)) #-40 cause the image wasnt cut proper.
		
		# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
		myfont = pygame.font.SysFont("Times New Roman", 25)

		# Draw moving part (Health bars)
		self.draw_update(unit_roster)

		#Print Player names
		for member in unit_roster.get("Players"):
			label = myfont.render(member.name, 1, (100,100,100))
			self.screen.blit(label, (200+(225*(member.number-1)), 20))

	def draw_update(self, unit_roster):
		#The health bars and energy bars update
		for member in unit_roster.get("Players"):
			pygame.draw.rect(self.screen, (200, 50, 50), (200+(225*(member.number-1)), 20, self.health_bar_len, 30), 0)
			pygame.draw.rect(self.screen, (0, 200, 50), (200+(225*(member.number-1)), 20, (member.health / member.health_max)*self.health_bar_len, 30), 0)

			pygame.draw.rect(self.screen, (0, 0, 0), (200+(225*(member.number-1)), 52, self.health_bar_len, 10), 0)
			pygame.draw.rect(self.screen, (250, 250, 0), (200+(225*(member.number-1)), 52, (member.energy / member.energy_max)*self.health_bar_len, 10), 0)

	def gameover_draw(self):
		# Draw an opaque gameover screen
		self.screen.blit(self.gameover_img, (0,0))