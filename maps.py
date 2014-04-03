import pygame
import math
from graph_module import Graph
from animation import *
import scripting

class Maps(object):


	def load_map_grid(self, filename):
	    """
	    Read in the Edmonton Road Map Data from the
	    given filename and create our Graph, a dictionary
	    for looking up the latitude and longitude information
	    for vertices and a dictionary for mapping streetnames
	    to their associated edges.
	    """
	    graph = Graph()
	    location = {}
	    get_vert = {}
	    streetnames = {}

	    with open(filename, 'r') as f:
	        for line in f:
	            elements = line.split(",")
	            if(elements[0] == "V"):
	                graph.add_vertex(int(elements[1]))
	                location[int(elements[1])] = (int(elements[2]),
	                                              int(elements[3]))
	                get_vert[(int(elements[2]), int(elements[3]))] = int(elements[1])
	            elif (elements[0] == "E"):
	                graph.add_edge((int(elements[1]), int(elements[2])))
	                streetnames[(int(elements[1]), int(elements[2]))] = elements[3]

	    return (graph, location, get_vert)	

	def __init__(self, screen):
		self.screen = screen
		self.grid_size = 8
		l = pygame.image.load


		self.backgrounds = {"map1": [l("images/Demo_1.png"), l("images/Demo_2.png"), l("images/Demo_3.png"),l("images/Demo_4.png"),l("images/Demo_5.png"),l("images/Demo_6.png")]}
		self.foregrounds = {"map1": [l("images/transparent.png"), l("images/transparent.png"), l("images/Demo_3.5.png"), l("images/transparent.png"), l("images/Demo_5.5.png"), l("images/transparent.png")]}


		self.sky = pygame.image.load("images/sky2.png")
		self.sky_pos = [0, -1024]
		self.sky_speed = 1
		self.sky_color_default = (100, 100, 200)
		self.sky_color = (100, 100, 200)
		self.is_map_scrolling = 0
		self.current_bg_index = 0
		self.current_bg = self.backgrounds.get("map1")[self.current_bg_index]
		self.current_fg = self.foregrounds.get("map1")[self.current_bg_index]
		self.map_list = ["map1","map2"]
		self.current_map = 0

		self.current_grid = 0
		self.map_grids = {"map1": [self.load_map_grid("Grid_Demo_1.txt"), self.load_map_grid("Grid_Demo_2.txt"), self.load_map_grid("Grid_Demo_1.txt"),
							self.load_map_grid("Grid_Demo_1.txt"),self.load_map_grid("Grid_Demo_1.txt"),self.load_map_grid("Grid_Demo_1.txt")],
						"map2": []}
		
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

		

	def draw_grid(self):

		for i in self.map_grids.get(self.map_list[self.current_map])[self.current_grid][0].edges():
					id1, id2 = i
					pygame.draw.line(self.screen, (255, 0, 0), self.map_grids.get(self.map_list[self.current_map])[self.current_grid][1][id1], self.map_grids.get(self.map_list[self.current_map])[self.current_grid][1][id2], 1)

	def scroll_map_right(self):
		for i in range(64):
			self.sky_draw()
			self.screen.blit(self.backgrounds.get(self.map_list[self.current_map])[self.current_grid], (0-i*16, 0))
			self.screen.blit(self.backgrounds.get(self.map_list[self.current_map])[self.current_grid+1], (1024-i*16, 0))
			pygame.display.update()
		self.is_map_scrolling = 0
		self.current_bg_index += 1
		self.current_bg_index %= len(self.backgrounds.get("map1"))
		self.current_bg = self.backgrounds.get("map1")[self.current_bg_index]

		self.current_grid += 1
		self.current_grid %= len(self.map_grids.get("map1"))

		if self.current_grid == 4:
			self.sky_speed = 0
			self.sky = pygame.image.load("images/Forest_Back.png")
			self.sky_pos = [0, -1024]

