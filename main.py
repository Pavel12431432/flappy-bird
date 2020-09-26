import pygame
from bird import Bird
from pipe import Pipe
import random

pygame.init()
screen = pygame.display.set_mode((288, 512), 0, 32)
pygame.display.set_caption('Flappy bird')
font = pygame.font.SysFont('consolas', 15)
clock = pygame.time.Clock()

backgroundImg = pygame.image.load('sprites/background-day.png')
birdImg = pygame.image.load('sprites/yellowbird-midflap.png')
floorImg = pygame.image.load('sprites/base.png')

maxVel = 6
bird = Bird(birdImg, maxVel)
floorX = 0


# pipe = Pipe((WIDTH, 300), 2)

def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			if chr(event.key) == ' ':
				bird.vel = -5


def draw():
	global floorX
	screen.fill((0, 0, 0))
	screen.blit(backgroundImg, (0, 0))
	bird.move()
	bird.draw(screen)
	if bird.vel < maxVel:
		bird.vel += 0.1
	'''if not pipe.move():
		pipe.pos = random.randint(WIDTH, WIDTH * 2), random.randint(100, int(HEIGHT / 1.5))
	pipe.draw(screen)'''
	floorX -= 1
	if floorX <= -288:
		floorX = 0
	screen.blit(floorImg, (floorX, 450))
	screen.blit(floorImg, (floorX + 288, 450))

	screen.blit(font.render(str(int(clock.get_fps())), True, (255, 0, 0)), (10, 10))
	pygame.display.update()

while True:
	inp()
	draw()
	clock.tick(144)