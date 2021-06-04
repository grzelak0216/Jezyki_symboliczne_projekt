import pygame
from sys import exit
from MazeGenerator import *
import time


SIZE = 15
QUANTITY_IN_WIDTH = 31  #nieparzysta liczba!
QUANTITY_IN_HEIGHT = 31 #nieparzysta liczba!
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 67
SCREEN_WIDTH = QUANTITY_IN_WIDTH * SIZE
SCREEN_HEIGHT = (QUANTITY_IN_HEIGHT * SIZE) + (2 * BUTTON_HEIGHT)


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


class Path_Btn:
	def __init__(self, screen):
		self.color = (0, 255, 0)
		self.f_color = (0, 0, 0)
		self.font = pygame.font.SysFont(None, BUTTON_HEIGHT * 2 // 3)
		self.text = self.font.render('PATH', True, self.f_color)
		self.screen = screen
		self.draw()

	def draw(self):
		pygame.draw.rect(self.screen, self.color, pygame.Rect(SCREEN_WIDTH-BUTTON_WIDTH, SCREEN_HEIGHT - BUTTON_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT))
		self.screen.blit(self.text, (SCREEN_WIDTH - BUTTON_WIDTH + 12, SCREEN_HEIGHT - BUTTON_HEIGHT//4 - 18))


class Start_Restart_Btn:
	def __init__(self, screen):
		self.color = (255, 255, 0)
		self.f_color = (0, 0, 0)
		self.font = pygame.font.SysFont(None, BUTTON_HEIGHT * 2 // 3)
		self.text = self.font.render('START', True, self.f_color)
		self.screen = screen
		self.draw()

	def draw(self):
		pygame.draw.rect(self.screen, self.color, pygame.Rect(0, SCREEN_HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, SCREEN_HEIGHT))
		self.screen.blit(self.text, (BUTTON_WIDTH//4 - 10, SCREEN_HEIGHT - BUTTON_HEIGHT//4 - 18))


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
		self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.UNION_FIND_SET, BUTTON_WIDTH, 0))
		self.buttonSTART = Start_Restart_Btn(self.screen)
		self.buttonPATH = Path_Btn(self.screen)
		self.buttons[0].click(self)

	def play(self):
		self.clock.tick(30)
		self.font = pygame.font.SysFont(None, BUTTON_HEIGHT // 2 * 3)
		self.text = self.font.render('!END!', True, (0, 0, 0))

		pygame.draw.rect(self.screen, (255, 190, 128), pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
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

		self.buttonSTART.draw()
		self.buttonPATH.draw()

	def generateMaze(self):
		if self.mode > 2:
			self.mode = 0

		if self.mode == 0:
			generateMap(self.map, self.maze_type)

		elif self.mode == 1:
			self.source = self.map.generatePos((1, self.map.width-2), (1, self.map.height-2))
			self.player = list(self.source)
			self.dest = self.map.generatePos((1, self.map.width-2), (1, self.map.height-2))
			if self.source[0] == self.dest[0] or self.source[1] == self.dest[1]:
				self.generateMaze()
			self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
			self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
			self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)

		else:
			self.map.resetMap(MAP_ENTRY_TYPE.MAP_EMPTY)
		self.mode += 1


	def move_playe(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			if (self.dest[0] == self.player[0] and self.player[1] == self.dest[1]):
				self.screen.blit(self.text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
			elif self.map.getType(self.player[0], self.player[1]-1) != MAP_ENTRY_TYPE.MAP_BLOCK:
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_EMPTY)
				self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
				self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
				self.player[1] -= 1
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
				time.sleep(0.4)

		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			if (self.dest[0] == self.player[0] and self.player[1] == self.dest[1]):
				self.screen.blit(self.text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
			elif self.map.getType(self.player[0], self.player[1]+1) != MAP_ENTRY_TYPE.MAP_BLOCK:
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_EMPTY)
				self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
				self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
				self.player[1] += 1
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
				time.sleep(0.4)

		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			if (self.dest[0] == self.player[0] and self.player[1] == self.dest[1]):
				self.screen.blit(self.text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
			elif self.map.getType(self.player[0]+1, self.player[1]) != MAP_ENTRY_TYPE.MAP_BLOCK:
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_EMPTY)
				self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
				self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
				self.player[0] += 1
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
				time.sleep(0.4)

		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			if (self.dest[0] == self.player[0] and self.player[1] == self.dest[1]):
				self.screen.blit(self.text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
			elif self.map.getType(self.player[0]-1, self.player[1]) != MAP_ENTRY_TYPE.MAP_BLOCK:
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_EMPTY)
				self.map.setMap(self.source[0], self.source[1], MAP_ENTRY_TYPE.MAP_BEGIN)
				self.map.setMap(self.dest[0], self.dest[1], MAP_ENTRY_TYPE.MAP_TARGET)
				self.player[0] -= 1
				self.map.setMap(self.player[0], self.player[1], MAP_ENTRY_TYPE.MAP_PLAYER)
				time.sleep(0.4)


def check_buttons(game, mouse_x, mouse_y):
	tempMode = game.mode
	if mouse_y > SCREEN_HEIGHT/2:
		print(game.mode)
		if ((SCREEN_HEIGHT - BUTTON_HEIGHT) < mouse_y < SCREEN_HEIGHT) and tempMode == 1:
			if 0 < mouse_x < BUTTON_WIDTH:
				game.generateMaze()
			elif ((SCREEN_WIDTH - BUTTON_WIDTH) < mouse_x < SCREEN_WIDTH):
				print('sciezka')
	else:
		for button in game.buttons:
			if button.rect.collidepoint(mouse_x, mouse_y):
				button.click(game)
				for tmp in game.buttons:
					if tmp != button:
						tmp.unclick()
						game.mode = 0
						game.generateMaze()
				break



def LETS_PLAY_A_GAME(WIDTH, HEIGHT):
	print('test1')
	global QUANTITY_IN_WIDTH
	QUANTITY_IN_WIDTH = (WIDTH // 2) * 2 + 1

	global QUANTITY_IN_HEIGHT
	QUANTITY_IN_HEIGHT = (HEIGHT // 2) * 2 + 1

	global SCREEN_WIDTH
	SCREEN_WIDTH = QUANTITY_IN_WIDTH * SIZE

	global SCREEN_HEIGHT
	SCREEN_HEIGHT = QUANTITY_IN_HEIGHT * SIZE + 2 * BUTTON_HEIGHT

	time.sleep(0.6)
	pygame.init()
	game = Game()

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

