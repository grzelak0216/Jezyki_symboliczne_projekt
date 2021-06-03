import pygame
from sys import exit
from MazeGenerator import *
import time


SIZE = 20
QUANTITY_IN_WIDTH = 31  #nieparzysta liczba!
QUANTITY_IN_HEIGHT = 31 #nieparzysta liczba!
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 100
SCREEN_WIDTH = QUANTITY_IN_WIDTH * SIZE
SCREEN_HEIGHT = QUANTITY_IN_HEIGHT * SIZE + BUTTON_HEIGHT

class Button():
	def __init__(self, screen, type, x, y):
		self.screen = screen
		self.width = BUTTON_WIDTH
		self.height = BUTTON_HEIGHT
		self.button_color = (200, 200, 200)
		self.text_color = [(64, 64, 64), (248, 0, 0)]
		self.font = pygame.font.SysFont(None, BUTTON_HEIGHT*2//3)
		
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.topleft = (x, y)
		self.type = type
		self.init_msg()
		
	def init_msg(self):
		self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[0], self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
		
	def draw(self):
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
	
	def click(self, game):
		game.maze_type = self.type
		self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[1], self.button_color)
	
	def unclick(self):
		self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[0], self.button_color)

class Game():
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
		self.clock = pygame.time.Clock()
		self.map = Map(QUANTITY_IN_WIDTH, QUANTITY_IN_HEIGHT)
		self.mode = 0
		self.maze_type = MAZE_GENERATOR_TYPE.RECURSIVE_BACKTRACKER
		self.buttons = []
		self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.RECURSIVE_BACKTRACKER, 0, 0))
		self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.UNION_FIND_SET, (BUTTON_WIDTH + 10) * 1, 0))
		self.buttons[0].click(self)

	def play(self):
		self.clock.tick(30)
		
		pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, SCREEN_WIDTH, BUTTON_HEIGHT))
		for button in self.buttons:
			button.draw()

		for y in range(self.map.height):
			for x in range(self.map.width):
				type = self.map.getType(x, y)
				if type == MAP_ENTRY_TYPE.MAP_EMPTY:
					color = (255, 190, 128)
				elif type == MAP_ENTRY_TYPE.MAP_BLOCK:
					color = (150, 75, 0)
				elif type == MAP_ENTRY_TYPE.MAP_TARGET:
					color = (255, 255, 0)
				elif type == MAP_ENTRY_TYPE.MAP_BEGIN:
					color = (0, 0, 0)
				elif type == MAP_ENTRY_TYPE.MAP_PLAYER:
					color = (128, 128, 128)
				else:
					color = (0, 255, 0)
				pygame.draw.rect(self.screen, color, pygame.Rect(SIZE * x, SIZE * y + BUTTON_HEIGHT, SIZE, SIZE))

	def generateMaze(self):
		if self.mode >= 3:
			self.mode = 0

		if self.mode == 0:
			generateMap(self.map, self.maze_type)

		elif self.mode == 1:
			self.source = self.map.generatePos((1, self.map.width-2), (1, self.map.height-2))
			self.player = list(self.source)
			self.dest = self.map.generatePos((1, self.map.width-2), (1, self.map.height-2))
			self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
			self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
			self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)

		else:
			self.map.resetMap(MAP_ENTRY_TYPE.MAP_EMPTY)
		self.mode += 1


	def move_playe(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			if self.map.getType(self.player[0], self.player[1]-1) != MAP_ENTRY_TYPE.MAP_BLOCK:
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_EMPTY)
				self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
				self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
				self.player[1] -= 1
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
				time.sleep(0.4)

		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			if self.map.getType(self.player[0], self.player[1]+1) != MAP_ENTRY_TYPE.MAP_BLOCK:
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_EMPTY)
				self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
				self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
				self.player[1] += 1
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
				time.sleep(0.4)

		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			if self.map.getType(self.player[0]+1, self.player[1]) != MAP_ENTRY_TYPE.MAP_BLOCK:
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_EMPTY)
				self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
				self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
				self.player[0] += 1
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
				time.sleep(0.4)

		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			if self.map.getType(self.player[0]-1, self.player[1]) != MAP_ENTRY_TYPE.MAP_BLOCK:
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_EMPTY)
				self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
				self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
				self.player[0] -= 1
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
				time.sleep(0.4)

def check_buttons(game, mouse_x, mouse_y):
	for button in game.buttons:
		if button.rect.collidepoint(mouse_x, mouse_y):
			button.click(game)
			for tmp in game.buttons:
				if tmp != button:
					tmp.unclick()
			break


pygame.init()
game = Game()
button_i = 0
while True:

	game.play()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
			game.generateMaze()
			break
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_buttons(game, mouse_x, mouse_y)
			print(mouse_x, mouse_y)
	game.move_playe()
	pygame.display.update()

