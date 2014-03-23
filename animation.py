import pygame

class Animation(object):

	def __init__(self, screen, player, offset, sequence, rate):
		self.sequence = sequence
		self.rate = rate
		self.player = player
		self.screen = screen
		self.offset = offset

	def animate(self):

		#Image Centering
		x_delta = (self.sequence[self.sequence[-2]].get_rect().size[0]-self.player.width) / 2
		y_delta = (self.sequence[self.sequence[-2]].get_rect().size[1]-self.player.height) / 2

		#Image Orientation
		if self.player.direction == 'left':
			self.screen.blit(self.sequence[self.sequence[-2]], (self.player.xpos-x_delta-self.offset, self.player.ypos-self.player.height-y_delta))
		else:
			flip_img = pygame.transform.flip(self.sequence[self.sequence[-2]],True,False)
			self.screen.blit(flip_img, (self.player.xpos-x_delta+self.offset, self.player.ypos-self.player.height-y_delta))
		
		#Controls the framerate
		if self.sequence[-1] == 0:

			# Advance to next frame
			self.sequence[-2] = (self.sequence[-2] + 1) % (len(self.sequence) - 2)
			self.sequence[-1] = 1
		elif self.sequence[-1]:
			self.sequence[-1] += 1
			if self.sequence[-1] >= self.rate:
				self.sequence[-1] = 0

	def animate_spell(self):
		#Image Centering
		x_delta = (self.sequence[self.sequence[-2]].get_rect().size[0]-self.player.width) / 2
		y_delta = (self.sequence[self.sequence[-2]].get_rect().size[1]-self.player.height) / 2

		#Image Orientation
		if self.player.direction == 'left':
			self.screen.blit(self.sequence[self.sequence[-2]], (self.player.xpos-x_delta-self.player.width, self.player.ypos-self.player.height-y_delta))
		else:
			flip_img = pygame.transform.flip(self.sequence[self.sequence[-2]],True,False)
			self.screen.blit(flip_img, (self.player.xpos-x_delta+self.player.width, self.player.ypos-self.player.height-y_delta))
		
		#Controls the framerate
		if self.sequence[-1] == 0:

			# Advance to next frame
			self.sequence[-2] = (self.sequence[-2] + 1) % (len(self.sequence) - 2)
			self.sequence[-1] = 1
		elif self.sequence[-1]:
			self.sequence[-1] += 1
			if self.sequence[-1] >= self.rate:
				self.sequence[-1] = 0 

class LoadImages(object):

	def __init__(self, dirr, images, angle = 0):
		self.dirr = dirr
		self.angle = angle
		self.images = images
		self.sequence = self.load_images()
	
	def load_images(self):
		sequence = []

		for i in self.images:
			sequence.append(pygame.transform.rotate(pygame.image.load(self.dirr + i), self.angle))
		sequence.append(0) #frame tracker
		sequence.append(1) #rate tracker
		return sequence
