import random
import pygame

# initialize pygame audio mixer
pygame.mixer.pre_init(frequency=44100, size=16, channels=1)
# initialize pygame
pygame.init()
screen = pygame.display.set_mode((288, 512), 0, 32)
pygame.display.set_caption('Flappy bird')
# import custom font
font = pygame.font.Font('font.ttf', 40)
clock = pygame.time.Clock()

# import sprites
day_img = pygame.image.load('sprites/background-day.png').convert()
night_img = pygame.image.load('sprites/background-night.png').convert()
floor_img = pygame.image.load('sprites/base.png').convert()
pipe_img = pygame.image.load('sprites/pipe-green.png').convert()
gameover_img = pygame.image.load('sprites/message.png').convert_alpha()

# import different frames from the bird flapping its wings
bird_frames = [
	pygame.image.load('sprites/yellowbird-downflap.png').convert(),
	pygame.image.load('sprites/yellowbird-midflap.png').convert(),
	pygame.image.load('sprites/yellowbird-upflap.png').convert()
]

# import sound effects
flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')

# start position for drawing the floor
floor_x = 0
# how fast the bird falls
fall_speed = 0.25
# birds velocity
# positive velocity means bird is falling
bird_velocity = 0
# game score
score = 0
high_score = 0
# index to decide which frame to draw from bird animation
bird_index = 0
# gap between pipes
pipe_gap = 150
# speed at which bird is moving
speed = 1200
running = True

# list of all pipes in the world
pipe_list = []

# variable to contain image of the background(day or night)
background_img = day_img

# define pygame rects for the bird and the gameover image
bird_rect = bird_frames[bird_index].get_rect(center=(50, 256))
gameover_rect = gameover_img.get_rect(center=(144, 256))

# create a timer to update bird animation frame every 150 ms
BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 150)

# create a timer to spawn a pipe every 1200 ms
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)


# function to handle input()
def inp():
	global bird_velocity, running, pipe_list, bird_index, bird_rect, score, speed
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			# check if space is pressed and the game is running
			if event.key == pygame.K_SPACE and running:
				# make bird jump
				bird_velocity = -6
				# flay flap sound
				flap_sound.play()
			# check if space is pressed and the game is not running
			elif event.key == pygame.K_SPACE and not running:
				# reset game
				running = True
				pipe_list.clear()
				bird_rect.center = (50, 256)
				bird_velocity = -6
				score = 0
				speed = 1200
				pygame.time.set_timer(SPAWN_PIPE, 1200)
		# every 1200 ms a pipe is spawned
		elif event.type == SPAWN_PIPE:
			pipe_list.extend(create_pipe())
		# every 150 ms bird frame index is updated
		elif event.type == BIRD_FLAP:
			bird_index = (bird_index + 1) % 3
			bird_rect = bird_frames[bird_index].get_rect(center=(50, bird_rect.centery))


# function to show score
def display_score():
	# show score
	surf = font.render(str(int(score)), True, (255, 255, 255))
	screen.blit(surf, surf.get_rect(center=(144, 50)))
	# if game has ended display the high score as well
	if not running:
		surf = font.render(str(int(high_score)), True, (255, 255, 255))
		screen.blit(surf, surf.get_rect(center=(144, 425)))


# function to create a pipe
def create_pipe():
	# pick height for pipe
	pos = random.randint(200, 400)
	# create top and bottom pipes
	bottom = pipe_img.get_rect(midtop=(350, pos))
	top = pipe_img.get_rect(midbottom=(350, pos - pipe_gap))
	# return the 2 pipes
	# second value indicates if the pipe x > 50 (if bird has not passed it yet)
	return (bottom, True), (top, True)


def move_pipes():
	global pipe_list, score, speed, background_img
	# move every pipe left
	for pipe, _ in pipe_list:
		pipe.centerx -= speed // 600
	# check if the first pipe has been passed
	if pipe_list:
		if pipe_list[0][0].centerx < 50 and pipe_list[0][1]:
			# if it has then play sound
			score_sound.play()
			# mark first 2 (top and bottom) pipes as passed
			pipe_list[0] = (pipe_list[0][0], False)
			pipe_list[1] = (pipe_list[1][0], False)
			# increase score
			score += 1
			# every 20 points change the background(day and night)
			# and update the speed at which pipes spawn
			if not score % 20:
				if background_img == day_img:
					background_img = night_img
				else:
					background_img = day_img
				pygame.time.set_timer(SPAWN_PIPE, 1200 - 10 * score)
		# if the pipe is off the screen then remove the pipe and its top/bottom pipe
		if pipe_list[0][0].centerx < -26:
			pipe_list = pipe_list[2:]


# check if player has hit a pipe or has gone off screen
def check_collision():
	for pipe, _ in pipe_list:
		if bird_rect.colliderect(pipe):
			return False
	return not (bird_rect.top <= -50 or bird_rect.bottom >= 450)


# draw every pipe
def draw_pipes():
	global pipe_list
	for pipe, _ in pipe_list:
		screen.blit(pygame.transform.flip(pipe_img, 0, 1) if pipe.bottom < 256 else pipe_img, pipe)


# draw and update floor
# have 2 floors moving simultaneously and when left on goes off the screen if goes on the right
# basically a digital treadmill
def draw_floor():
	global floor_x
	# check if floor image has gone off screen
	# else subtract speed // 600 from floor_x (moves floor left)
	floor_x = 0 if floor_x <= -288 else floor_x - speed // 600
	# draw floor
	screen.blit(floor_img, (floor_x, 450))
	screen.blit(floor_img, (floor_x + 288, 450))


# main draw function
def draw():
	global bird_velocity, running, score, high_score
	# show background
	screen.blit(background_img, (0, 0))
	# draw and update floor
	draw_floor()
	if running:
		# show rotated bird depending on if the bird's velocity is positive or negative
		screen.blit(pygame.transform.rotate(bird_frames[bird_index], - bird_velocity * 5), bird_rect)
		# increase bird velocity
		bird_velocity += fall_speed
		bird_rect.centery += round(bird_velocity)
		# check for collisions
		if not (running := check_collision()):
			death_sound.play()

		move_pipes()
		draw_pipes()
	else:
		# if game is not running show game over screen
		screen.blit(gameover_img, gameover_rect)
		# update high score
		high_score = max(score, high_score)

	display_score()
	pygame.display.update()


while True:
	inp()
	draw()
	clock.tick(120)
