import pygame
import math

class Maps(object):

	def __init__(self, screen):
		self.screen = screen
		self.bg = pygame.image.load("images/BackgroundCastle1.png")
		self.bg1 = pygame.transform.flip(self.bg,True,False)
		self.sky = pygame.image.load("images/sky2.png")
		self.sky_pos = [0, -1024]
		self.sky_speed = 1
		self.sky_color_default = (100, 100, 200)
		self.sky_color = (100, 100, 200)
		self.is_map_scrolling = 0
		self.current_bg = self.bg

	def update_sky(self):

		#Sky Color Change
		R,G,B = self.sky_color

		# THIS WAS COPIED FROM THE ASSIGNMENT 4
		# This produces a sine wave effect between a and b.
		sin = (math.sin(pygame.time.get_ticks() * 0.00005) + 1) * 0.5
		effect = lambda a, b: a + sin * (b - a)
		R = effect(self.sky_color_default[0]/4, self.sky_color_default[0]+50)
		G = effect(self.sky_color_default[1]/4, self.sky_color_default[1]+50)
		B = effect(self.sky_color_default[2]/4, self.sky_color_default[2]+50)
		self.sky_color = (R,G,B)

		#Cloud Loop
		for i in range(len(self.sky_pos)):
			self.sky_pos[i] += self.sky_speed
			if self.sky_pos[i] > 1024:
				self.sky_pos[i] = -1024

	def sky_draw(self):
		# Fill background
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill(self.sky_color)
		self.screen.blit(background, (0, 0))


		self.update_sky()
		for i in range(len(self.sky_pos)):
			self.screen.blit(self.sky, (self.sky_pos[i], 0))



	def scroll_map_right(self):
		for i in range(64):
			self.sky_draw()
			self.screen.blit(self.bg, (0-i*16, 150))
			self.screen.blit(self.bg1, (1024-i*16, 150))
			pygame.display.update()
		self.is_map_scrolling = 0
		self.current_bg = self.bg1