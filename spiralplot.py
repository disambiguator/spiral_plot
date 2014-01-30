#!/usr/bin/python
import sys
import pygame
import math
import time
import random
import itertools

class spiralPlot:

	def drawLine(self, (x1, y1), (x2, y2)):
		l = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		x2 = x1 + (l+self.delta)*(x2-x1)/l

		y2 = y1 + (l+self.delta)*(y2-y1)/l
	#	pygame.draw.aalines(self.screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), False, [(x1, y1), (x2, y2)], 1)
		pygame.draw.aalines(self.screen, self.c_iter.next(), False, [(x1, y1), (x2, y2)], 1)	
		return (x2, y2)

	def run(self):
		self.delta = 5
		l = 15
		
		pygame.init()
		screen_width = pygame.display.Info().current_w
		screen_height = pygame.display.Info().current_h
		self.screen=pygame.display.set_mode((screen_width, screen_height))
		
		#colors
		red = (255,0,0)
		green = (0,255,0)
		blue = (0,0,255)
		darkBlue = (0,0,128)
		white = (255,255,255)
		black = (0,0,0)
		pink = (255,200,200)
		colors = [red, green, blue] #darkBlue], white, black, pink]
		self.c_iter=itertools.cycle(colors)
		coords = []
		angle = math.radians(90)
		x1 = pygame.display.Info().current_w/2
		y1 = pygame.display.Info().current_h/2
		coords.append((x1,y1))	
		coords.append((x1+l, y1))
		x3 = x1+l-l*math.cos(angle)
		y3 = y1-l*math.sin(angle)
		#coords.append((x3, y3))
		coords.append((x1+l, y1+l))
		coords.append((x1, y1+l))
		#x4 = 
		
		pygame.draw.aalines(self.screen, white, False, coords, 1)

		n = len(coords) - 1
		for _ in range(10000):
			coords[0] = self.drawLine(coords[n], coords[0])
			for i in range(n):	
				coords[i+1] = self.drawLine(coords[i], coords[i+1])
		#	time.sleep(0.05)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return

			pygame.display.update()

		raw_input("Press enter to exit")
		pygame.quit()
		sys.exit()

spiralPlot().run()
