#2D Grid generator
import pygame
from pygame.locals import *

"""
	Creates a visual grid that you can color in. Colored squares will upon saving
	be generated into graph data that can be loaded using Load_Graph_Data.

	This isnt really part of the project just  a tool I develloped on the side
	to assit with generating grids in our game.
"""

def generate_data(filename, array, RESOLUTION_X, RESOLUTION_Y, grid_delta):
	"""
	for each colored box write the Vertices and Edge data into a file.
	"""

	vertices = {}
	vert_id_to_coord = {}
	edges = {}

	vert_id = 0
	for x in range(RESOLUTION_X//grid_delta):
		for y in range(RESOLUTION_Y//grid_delta):
			if array[y][x] == 1:

				TL = (x*grid_delta, y*grid_delta)
				TR = (x*grid_delta+grid_delta, y*grid_delta)
				BL = (x*grid_delta, y*grid_delta+grid_delta)
				BR = (x*grid_delta+grid_delta, y*grid_delta+grid_delta)

				if TL not in vertices:
					vertices[TL] = vert_id #LT
					vert_id += 1
				if TR not in vertices:
					vertices[TR] = vert_id
					vert_id += 1
				if BR not in vertices:
					vertices[BR] = vert_id
					vert_id += 1
				if BL not in vertices:
					vertices[BL] = vert_id
					vert_id += 1

				edges[(vertices[TL], vertices[TR])] = None
				edges[(vertices[TR], vertices[BR])] = None	
				edges[(vertices[BR], vertices[BL])] = None
				edges[(vertices[BL], vertices[TL])] = None

	for key, value in vertices.items():
		vert_id_to_coord[value] = key

	f = open(filename, 'w+')

	for key, value in vertices.items():
		f.write("V, " + str(value) + ", " + str(key[0]) + ", " + str(key[1]) + "\n")

	for key in edges:
		f.write("E, " + str(key[0]) + ", " + str(key[1]) + ", None" + "\n")		
	
	return vertices, vert_id_to_coord, edges

def select_square(screen, surface, array, grid_delta, grid_bg, brush_size):
	"""
	Color the grid square and indicated on the array that the square is filled.
	"""
	x, y = pygame.mouse.get_pos()
	x //= grid_delta
	y //= grid_delta

	for i in range(brush_size):
		rect = ((x+i)*grid_delta, (y+i)*grid_delta, grid_delta, grid_delta)
		pygame.draw.rect(surface, (0, 255, 0), rect)
		rect = ((x+i)*grid_delta, (y+i)*grid_delta, grid_delta-1, grid_delta-1)
		pygame.draw.rect(surface, (0, 255, 0), rect)
		try:
			array[y+i][x+i] = 1
		except:
			pass

		rect = ((x+i+1)*grid_delta, (y+i)*grid_delta, grid_delta, grid_delta)
		pygame.draw.rect(surface, (0, 255, 0), rect)
		rect = ((x+i+1)*grid_delta, (y+i)*grid_delta, grid_delta-1, grid_delta-1)
		pygame.draw.rect(surface, (0, 255, 0), rect)
		try:
			array[y+i][x+i+1] = 1
		except:
			pass

		rect = ((x+i)*grid_delta, (y+i+1)*grid_delta, grid_delta, grid_delta)
		pygame.draw.rect(surface, (0, 255, 0), rect)
		rect = ((x+i)*grid_delta, (y+i+1)*grid_delta, grid_delta-1, grid_delta-1)
		pygame.draw.rect(surface, (0, 255, 0), rect)
		try:
			array[y+i+1][x+i] = 1
		except:
			pass


	screen.blit(grid_bg, (0, 0))
	screen.blit(surface, (0, 0))

def desel_square(screen, surface, array, grid_delta, grid_bg, brush_size):
	"""
	Remove Color the grid square and indicated on the array that the square is empty.
	"""
	x, y = pygame.mouse.get_pos()
	x //= grid_delta
	y //= grid_delta

	rect = (x*grid_delta, y*grid_delta, grid_delta, grid_delta)
	pygame.draw.rect(surface, (0, 255, 0), rect)
	rect = (x*grid_delta, y*grid_delta, grid_delta-1, grid_delta-1)
	pygame.draw.rect(surface, (0, 0, 0), rect)

	array[y][x] = 0

	screen.blit(grid_bg, (0, 0))
	screen.blit(surface, (0, 0))

def main():
	# Initialise screen
	#RESOLUTION_X = int(input("input x size"))
	RESOLUTION_X = 1024
	#RESOLUTION_Y = int(input("input y size"))
	RESOLUTION_Y = 600
	grid_delta = int(input("input grid box size"))
	img_file = input("input image filename")
	grid_bg = pygame.image.load(img_file)
	grid_name = input("Please provide output filename: Ex: outputfile.txt")

	pygame.init()
	screen = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y))
	
	brush_size = 1
	screen.blit(grid_bg, (0, 0))

	background = pygame.Surface(screen.get_size())
	background.set_alpha(75)
	
	array = [[0 for x in range(RESOLUTION_X//grid_delta)] for y in range(RESOLUTION_Y//grid_delta)]

	for i in range(RESOLUTION_X//grid_delta):
		for j in range(RESOLUTION_Y//grid_delta):
			rect = (i*grid_delta, j*grid_delta, grid_delta, grid_delta)
			pygame.draw.rect(background, (0, 255, 0), rect)
			rect = (i*grid_delta, j*grid_delta, grid_delta-1, grid_delta-1)
			pygame.draw.rect(background, (0, 0, 0), rect)

	screen.blit(background, (0, 0))

	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			#Color Square. Mark as 4 verts with edges between
			if pygame.mouse.get_pressed() == (1, 0, 0):
				select_square(screen, background, array, grid_delta, grid_bg, brush_size)
			#Remove Square. 
			if pygame.mouse.get_pressed() == (0, 0, 1):
				desel_square(screen, background, array, grid_delta, grid_bg, brush_size) 
			keys = pygame.key.get_pressed()
			if  keys[pygame.K_LEFT]:
				vert, vertId_cord, edges = generate_data(grid_name, array, RESOLUTION_X, RESOLUTION_Y, grid_delta)
				for i in edges:
					id1, id2 = i
					pygame.draw.line(background, (255, 0, 0), vertId_cord[id1], vertId_cord[id2], 5)
				screen.blit(background, (0, 0))
				return
			#Increase Brush Size
			if  keys[pygame.K_UP]:
				if brush_size < 1000:
					brush_size += 1
					print(brush_size)
			if  keys[pygame.K_DOWN]:
				if brush_size > 1:
					brush_size -= 1
					print(brush_size)
		pygame.display.update()

if __name__ == '__main__': main()
