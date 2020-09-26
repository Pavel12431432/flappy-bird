import pygame

class Pipe:
	def __init__(self, pos, vel):
		self.pos = pos
		self.vel = vel
	def move(self):
		if self.pos[0] - self.vel > 0:
			self.pos = self.pos[0] - self.vel, self.pos[1]
			return 1
		else:
			return 0
	def draw(self, screen):
		pygame.draw.line(screen, (0, 200, 0), self.pos, (self.pos[0], 0), 50)