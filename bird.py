import pygame


class Bird:
	def __init__(self, img, vel):
		self.pos = (144, 256)
		self.vel = vel
		self.img = pygame.transform.scale(img, (51, 36))

	def draw(self, screen):
		screen.blit(self.img, (self.pos[0] - 26, self.pos[1] - 18))

	def move(self):
		if 0 < self.pos[1] + self.vel < 960:
			self.pos = (self.pos[0], self.pos[1] + self.vel)