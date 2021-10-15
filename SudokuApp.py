import pygame, sys
from Config import *
from ButtonClass import *

class App():
	def __init__(self):
		pygame.init()
		self.icon = pygame.image.load('Data/images/icon.png')
		self.background = pygame.image.load('Data/images/title.jpg')
		self.back = Button("<<",10,10,50,50, BLACK, "californianfb")
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Sudoku')
		pygame.display.set_icon(self.icon)
		self.mode = "main"
		self.running = True
		self.selected_cell = None
		self.buttons = []
		self.state = "playing"
		self.playingButtons = []
		self.menuButtons = []
		self.loadMenuButtons()

	def run(self):
		while self.running:
			self.main_events()
			self.main_update()
			if self.mode == "main":
				self.main_draw()
			elif self.mode == "start":
				self.game_draw()
			elif self.mode == "scores":
				self.scores_draw()
			elif self.mode == "settings":
				self.settings_draw()
			elif self.mode == "about":
				self.about_draw()

		pygame.quit()
		sys.exit()

#############   EVENTS FUNCTIONS #############

	def main_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.mode != 'main' and self.check_collision(self.back):
					self.mode = 'main'

				if self.mode=='main':
					for button in self.menuButtons:
						if (self.mousePos[0]>=button.pos[0] and self.mousePos[0]<=button.pos[0]+button.size[0]) and (self.mousePos[1]>=button.pos[1] and self.mousePos[1]<=button.pos[1]+button.size[1]):
							self.mode = button.text.lower()
				elif self.mode == 'start':
					self.selected_cell = self.get_cell()

#############   DRAW FUNCTIONS #############

	def main_draw(self):
		self.screen.blit(self.background, (0,0)) 
		for button in self.menuButtons:
			button.draw(self.screen)
		pygame.display.update()

	def game_draw(self):
		self.screen.fill(WHITE)
		self.back.draw(self.screen, WHITE)
		for button in self.playingButtons:
			button.draw(self.screen)

		if self.selected_cell:
			self.highlight_cell()
			
		pygame.draw.rect(self.screen, BLACK, (BOARD_POS[0],BOARD_POS[1], BOARD_W, BOARD_H), 3)
		for i in range(9):
			if i%3==0:
				line_thickness = 3
			else:
				line_thickness = 1
			pygame.draw.line(self.screen, BLACK,(BOARD_POS[0]+(i*CELL),BOARD_POS[1]),(BOARD_POS[0]+(i*CELL),BOARD_POS[1]+BOARD_H),line_thickness)
			pygame.draw.line(self.screen, BLACK,(BOARD_POS[0],BOARD_POS[1]+(i*CELL)),(BOARD_POS[0]+BOARD_W,BOARD_POS[1]+(i*CELL)), line_thickness)

		pygame.display.update()

	def scores_draw(self):
		self.screen.fill(SCORES)
		self.back.draw(self.screen, SCORES)
		font = pygame.font.SysFont("calibri",50, bold=True)
		scores = font.render("SCORES HERE!", True, BLACK)
		w = scores.get_width()
		x,y = (WIDTH - w)//2, 30
		self.screen.blit(scores, (x,y))
		pygame.display.update()

	def settings_draw(self):
		self.screen.fill(SETTINGS)
		self.back.draw(self.screen, SETTINGS)
		font = pygame.font.SysFont("calibri", 50, bold=True)
		settings = font.render("SETTINGS",True,BLACK)
		w = settings.get_width()
		x, y = (WIDTH - w)//2, 30 
		self.screen.blit(settings,(x,y))
		pygame.display.update()

	def about_draw(self):
		self.screen.blit(self.background,(0,0))
		self.back.draw(self.screen, ABOUT)
		font = pygame.font.SysFont("calibri", 30, bold=True)
		about = font.render("Developed by: Meghal Darji", True, BLACK)
		w = about.get_width()
		h = about.get_height()
		x,y = (WIDTH - w)//2, (HEIGHT - h)//2
		self.screen.blit(about,(x,y))
		pygame.display.update()

#############   HELPER FUNCTIONS #############

	def check_collision(self, button):
		lower1 = self.mousePos[0] >= button.pos[0]
		lower2 = self.mousePos[1] >= button.pos[1]
		upper1 = self.mousePos[0] <= button.pos[0] + button.size[0]
		upper2 = self.mousePos[1] <= button.pos[1] + button.size[1]
		return (lower1 and lower2 and upper1 and upper2)

	def main_update(self):
		self.mousePos = pygame.mouse.get_pos()
		for button in self.menuButtons:
			button.update(self.mousePos)

	def highlight_cell(self):
		cell_w = CELL
		cell_h = CELL

		pygame.draw.rect(self.screen, LLTEAL, 
			(BOARD_POS[0]+CELL*3*(self.selected_cell[0]//3),
				BOARD_POS[1]+3*CELL*(self.selected_cell[1]//3),
				CELL*3, 
				CELL*3))

		pygame.draw.rect(self.screen, LTEAL, 
			(BOARD_POS[0], BOARD_POS[1]+(CELL*self.selected_cell[1]),
				CELL*9,
				CELL))
		
		pygame.draw.rect(self.screen, LTEAL, 
			(BOARD_POS[0]+(CELL*self.selected_cell[0]),
				BOARD_POS[1],
				CELL,
				CELL*9))

		if self.selected_cell[0]==8:
			cell_w -= 2
		if self.selected_cell[1]==8:
			cell_h -=2

		pygame.draw.rect(self.screen,TEAL, (BOARD_POS[0]+self.selected_cell[0]*CELL, BOARD_POS[1]+self.selected_cell[1]*CELL,cell_w, cell_h))
		

	def get_cell(self):
		# print(((self.mousePos[0]-BOARD_POS[0])//CELL, (self.mousePos[1]-BOARD_POS[1])//CELL))
		if self.mousePos[0] < BOARD_POS[0] or self.mousePos[1] < BOARD_POS[1]:
			return False
		if self.mousePos[0] > BOARD_POS[0]+BOARD_W or self.mousePos[1] > BOARD_POS[1] + BOARD_H:
			return False
		
		return ((self.mousePos[0]-BOARD_POS[0])//CELL, (self.mousePos[1]-BOARD_POS[1])//CELL)

	def loadMenuButtons(self):
		for i in range(M_NUM):
			button = Button(BUTTONS[i],M_TOP_LEFT[0],M_TOP_LEFT[1]+(M_SPACE+M_BL)*(i+1), M_BW, M_BL, button_color=M_COLOR, font="inkfree", bold=True)
			self.menuButtons.append(button)
