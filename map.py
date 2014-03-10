import pygame
import math

class Map(object):

	def __init__(self, screen):
		self.screen = screen
		self.bg = pygame.image.load("images/BackgroundCastle1.png")
		self.sky = pygame.image.load("images/sky2.png")
		self.sky_pos = [0, -1024]
		self.sky_speed = 1
		self.sky_color_default = (100, 100, 200)
		self.sky_color = (100, 100, 200)

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

