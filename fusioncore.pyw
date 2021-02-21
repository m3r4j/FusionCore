import pygame
import os
import sys
import random

pygame.init()
pygame.font.init()

font = pygame.font.SysFont(None, 40)

black = (0, 0, 0)
blue = (0, 0, 255)

width, height = 400, 500

window = pygame.display.set_mode((width, height))

pygame.display.set_caption('Fusion Core')

game_icon = pygame.image.load('icon.png')
pygame.display.set_icon(game_icon)

fps = 60

clock = pygame.time.Clock()

background = pygame.image.load(os.path.join('sprites', 'background.png'))
background = pygame.transform.scale(background, (width, height))

background_speed = 5

player_car_width = 100
player_car_height = 150

player_car = pygame.image.load(os.path.join('sprites', 'player_car.png'))
player_car = pygame.transform.rotate(player_car, 90)
player_car = pygame.transform.scale(player_car, (player_car_width, player_car_height))

swap_lane = 125

player_car_y = height - player_car_height - 10

max_cars = 2

score_per_round = 5

car_speed_add = 1

enemy_car = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(os.path.join('sprites', 'enemy_car.png')), 180), (player_car_width, player_car_height))

def generate_cars(amount):
	global cars

	x_coords = [25, 150, 275]

	for i in cars:
		if i.x in x_coords:
			x_coords.remove(i.x)

	if random.random() < 0.01:
		if len(cars) != max_cars:
			for i in range(amount):
				x = random.choice(x_coords)
				y = -100
				car_rect = pygame.Rect(x, y, player_car_width, player_car_height)
				cars.append(car_rect)


def draw_intro():
	text = font.render('Press SPACE to begin', True, blue)
	window.blit(text, (width - (width - 60), height // 2))



def draw_cars(cars):
	global score

	index = 0
	for i in cars:
		window.blit(enemy_car, (i))
		if i.y > height:
			del cars[index]
			score += 1
		i.y += car_speed
		index += 1


def draw_road():
	global background_y

	if background_y >= height:
		background_y = 0

	window.blit(background, (0, background_y))
	window.blit(background, (0, background_y - height))
	background_y += background_speed



def main():
	global cars, background_y, score, car_speed

	cars = []

	car_speed = 3

	score = 0
	scores = []

	started = False

	player_car_x = 150

	background_y = 0

	while True:
		clock.tick(fps)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					started = True

				if started:
					if event.key == pygame.K_a and not player_car_x - swap_lane < 0:
						player_car_x -= swap_lane

					if event.key == pygame.K_d and not player_car_x + swap_lane >= width:
						player_car_x += swap_lane

		window.fill(black)
		draw_road()
		window.blit(player_car, (player_car_x, player_car_y))
		player_rect = pygame.Rect(player_car_x, player_car_y, player_car_width, player_car_height)

		if not started:
			draw_intro()

		if started:
			generate_cars(1)
			draw_cars(cars)


		for i in cars:
			if player_car_x == i.x and player_rect.colliderect(i):
				main()

		if score % score_per_round == 0 and score != 0 and score not in scores:
			scores.append(score)
			car_speed += car_speed_add

		pygame.display.update()

main()