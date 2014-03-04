# Main File

#!/usr/bin/python

import pygame
from pygame.locals import *

"""
git add --all
git commit -m "S"
git push
"""


def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((1000, 800))
	pygame.display.set_caption('Basic Pygame program')

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((100, 250, 250))

	# Display some text
	font = pygame.font.Font(None, 36)
	text = font.render("Welcome", 1, (10, 10, 10))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		pygame.display.flip()
		update_logic()
		update_draw()


if __name__ == '__main__': main()



def update_draw():
	pygame.draw.rect(None, (0, 25, 25), box, 0)
