import sys, pygame
import random

class GUI(object):

	def __init__(self, screen, unit_roster):
		self.screen = screen
		self.unit_roster = unit_roster
		self.health_bar_len = 200
		self.panel = pygame.image.load("images/panel1.png")
		self.gameover_img = pygame.image.load("images/Game_over.png")

	def draw(self, unit_roster):
		#pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, self.screen.get_size()[0] , 150), 0)
		self.screen.blit(self.panel, (0, -40))
		# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
		myfont = pygame.font.SysFont("Times New Roman", 25)

		self.draw_update(unit_roster)

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
		self.screen.blit(self.gameover_img, (0,0))