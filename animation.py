import pygame

class Animation(object):
	"""
	!! If I had more time id rework this to be a more general object/function.

	Object Class in charge of managing individual Animation sequences.
	Fed a list of sprites, a rate at which to move through the list.
	Will draw the image on player position and ajust according to offset.
	"""

	def __init__(self, screen, player, offsetx, offsety, sequence, rate):
		self.sequence = sequence
		self.rate = rate
		self.player = player
		self.screen = screen
		self.offsetx = offsetx
		self.offsety = offsety

	def animate(self):
		"""
		~! Should be reworked so that rate is counted by time not logic loops

		With each logic loop we increment the count on rate, once this "rate" has done a full 
		loop we adcance the frame. This allows for control of speed of animations.
		"""

		#Image Centering (Centeres with current player box width/height)
		x_delta = (self.sequence[self.sequence[-2]].get_rect().size[0]-self.player.width) / 2
		y_delta = (self.sequence[self.sequence[-2]].get_rect().size[1]-self.player.height) / 2

		#Image Orientation (left or right facing image, uses player direction)
		if self.player.direction == 'left':
			self.screen.blit(self.sequence[self.sequence[-2]], (self.player.xpos-x_delta-self.offsetx, self.player.ypos-self.player.height-y_delta-self.offsety))
		else:
			flip_img = pygame.transform.flip(self.sequence[self.sequence[-2]],True,False)
			self.screen.blit(flip_img, (self.player.xpos-x_delta+self.offsetx, self.player.ypos-self.player.height-y_delta-self.offsety))
		
		#Controls the framerate

		#Advance to next frame if rate has done a full loop
		if self.sequence[-1] == 0:
			self.sequence[-2] = (self.sequence[-2] + 1) % (len(self.sequence) - 2)
			self.sequence[-1] = 1

		#Frame is not advance, rate is just incremented.
		elif self.sequence[-1]:
			self.sequence[-1] += 1
			if self.sequence[-1] >= self.rate:
				self.sequence[-1] = 0

	def animate_spell(self):
		"""
		Same as animate()
		"""
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
	"""
	Loads a set of image files into a sequence with pre-defined rate and frame tracker.
	This is to be used for any sequence of images that you would like to be formed into a 
	animation.

	Optional angle rotaion on the images.
	"""

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
