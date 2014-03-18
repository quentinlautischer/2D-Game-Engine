#2D Grid generator
import pygame
from pygame.locals import *

def main():
	# Initialise screen
	#RESOLUTION_X = int(input("input x size"))
	RESOLUTION_X = 1024
	#RESOLUTION_Y = int(input("input y size"))
	RESOLUTION_Y = 600
	#grid_delta = int(input("input grid box size"))
	grid_delta = 8
	grid_bg = pygame.image.load("images/dark_forest_by_vityar83-d4yjpvb.jpg")
	

	pygame.init()
	screen = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y))
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	screen.blit(background, (0, 0))
	screen.blit(grid_bg, (0, 0))

	for i in range(RESOLUTION_X//grid_delta):
		for j in range(RESOLUTION_Y//grid_delta):
			rect = (i*grid_delta, j*grid_delta, grid_delta, grid_delta)
			pygame.draw.rect(screen, (0, 255, 0), rect)
			rect = (i*grid_delta, j*grid_delta, grid_delta-1, grid_delta-1)
			pygame.draw.rect(screen, (0, 0, 0), rect)

	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
		pygame.display.update()

if __name__ == '__main__': main()
