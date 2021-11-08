import pygame, sys
from Config import *
from ButtonClass import *
import os, random, time

class App():
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.icon = pygame.image.load('Data/images/icon.png')
		self.background = pygame.image.load('Data/images/title.jpg')

		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Sudoku')
		pygame.display.set_icon(self.icon)

		self.back = Button("<<",10,10,50,50, BLACK, "californianfb")
		self.notes_mode = False
		self.mode = "menu"
		self.running = True
		self.selected_cell = None
		self.locked_cells = []
		self.notes = [ [[] for _ in range(9)] for _ in range(9)]
		self.difficulty = "easy"
		self.board, self.solution = self.fetch_board()
		self.finished = False
		self.wrongs = [[False for _ in range(9)] for _ in range(9)]
		for xidx,row in enumerate(self.board):
			for yidx,num in enumerate(row):
				if num!=0:
					self.locked_cells.append([xidx, yidx])
		self.selected_number = None
		self.gameButtons = self.loadButtons("start")
		self.menuButtons = self.loadButtons("menu")
		self.settingsButton = self.loadButtons("settings")
		self.difficultyButtons = self.loadButtons("difficulty")

	def run(self):
		while self.running:
			self.main_events()
			self.mousePos = pygame.mouse.get_pos()
			if self.mode == "menu":
				self.menu_draw()
				for button in self.menuButtons:
					button.update(self.mousePos)
			elif self.mode == "start":
				self.game_draw()
				if self.selected_cell:
					self.selected_number = self.board[self.selected_cell[0]][self.selected_cell[1]]
				if self.filled():
					self.finish_draw()
			elif self.mode == "scores":
				self.scores_draw()
			elif self.mode == "settings":
				self.settings_draw()
				for button in self.settingsButton:
					button.update(self.mousePos)
			elif self.mode == "about":
				self.about_draw()
			elif self.mode == "difficulty":
				self.settings_draw()
				for button in self.difficultyButtons:
					button.update(self.mousePos)
		pygame.quit()
		sys.exit()

#############   EVENTS FUNCTIONS #############

	def main_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.mode != "menu" and self.check_collision(self.back):
					self.mode = "menu"

				if self.mode =="menu":
					for button in self.menuButtons:
						if self.check_collision(button):
							self.mode = button.text.lower()

				elif self.mode == "start":
					self.selected_cell = self.get_cell()
					if self.check_collision(self.gameButtons[0]):
						self.notes_mode = not(self.notes_mode)
						if self.notes_mode:
							self.gameButtons[0].button_color = LYELLOW
						else:
							self.gameButtons[0].button_color = YELLOW
				elif self.mode == "settings":
					for button in self.settingsButton:
						if self.check_collision(button):
							self.mode = button.text.lower()
				elif self.mode == "difficulty":
					for button in self.difficultyButtons:
						if self.check_collision(button):
							self.difficulty = button.text.lower()
							self.board, self.solution = self.fetch_board()
							self.mode = "settings"
				
			elif event.type == pygame.KEYDOWN:
				if self.mode == 'start':
					if self.selected_cell != None:
						if event.key == pygame.K_UP:
							self.selected_cell[0] = max(0,self.selected_cell[0]-1)
						elif event.key == pygame.K_LEFT:
							self.selected_cell[1] = max(0,self.selected_cell[1]-1)
						elif event.key == pygame.K_RIGHT:
							self.selected_cell[1] = min(8,self.selected_cell[1]+1)
						elif event.key == pygame.K_DOWN:
							self.selected_cell[0] = min(8, self.selected_cell[0]+1) 
					if self.selected_cell != None and self.selected_cell not in self.locked_cells and event.unicode in list('123456789'):
						if self.notes_mode:
							self.board[self.selected_cell[0]][self.selected_cell[1]] = 0
							if int(event.unicode) in self.notes[self.selected_cell[0]][self.selected_cell[1]]:
								self.notes[self.selected_cell[0]][self.selected_cell[1]].remove(int(event.unicode))
								self.selected_number = None
							else:
								self.notes[self.selected_cell[0]][self.selected_cell[1]].append(int(event.unicode))
								self.selected_number = int(event.unicode)
						else:
							self.notes[self.selected_cell[0]][self.selected_cell[1]] = []
							self.board[self.selected_cell[0]][self.selected_cell[1]] = int(event.unicode)
							self.selected_number = int(event.unicode)
							if int(event.unicode) != self.solution[self.selected_cell[0]][self.selected_cell[1]]:
								self.wrongs[self.selected_cell[0]][self.selected_cell[1]] = True
							else:
								self.wrongs[self.selected_cell[0]][self.selected_cell[1]] = False

					if event.key == pygame.K_BACKSPACE and self.selected_cell and self.selected_cell not in self.locked_cells and not(self.notes_mode):
						self.board[self.selected_cell[0]][self.selected_cell[1]] = 0
						self.selected_number = None

#############   FETCH BOARD FUNCTION #############

	def fetch_board(self):
		board_path = "Data/boards"
		n = random.randint(1,10000)
		filename = os.path.join(board_path,self.difficulty,str(n)+'.csv')
		with open(filename) as file:
			data = file.read()
			board_data = list(data.split()[1].split(',')[0])
			sol_data = data.split()[1].split(',')[1]
		board = [[] for _ in range(9)]
		solution = [[] for _ in range(9)]
		for i in range(len(board_data)):
			board[i//9].append(int(board_data[i]))
			solution[i//9].append(int(sol_data[i]))
		return board, solution

#############   DRAW FUNCTIONS #############

	def menu_draw(self):
		self.screen.blit(self.background, (0,0))
		for button in self.menuButtons:
			button.draw(self.screen)
		pygame.display.update()

	def game_draw(self):
		self.screen.fill(WHITE)
		self.back.draw(self.screen, WHITE)
		numbers = [1,2,3,4,5,6,7,8,9]

		for button in self.gameButtons:
			button.draw(self.screen)

		if self.selected_cell and self.selected_number:
			self.highlight_num()

		if self.selected_cell:
			self.highlight_cell()

		pygame.draw.rect(self.screen, BLACK, (BOARD_POS[0],BOARD_POS[1], BOARD_W, BOARD_H), 3)
		for i in range(9):
			pygame.draw.line(self.screen, BLACK,(BOARD_POS[0]+(i*CELL),BOARD_POS[1]),(BOARD_POS[0]+(i*CELL),BOARD_POS[1]+BOARD_H),3 if i%3==0 else 1)
			pygame.draw.line(self.screen, BLACK,(BOARD_POS[0],BOARD_POS[1]+(i*CELL)),(BOARD_POS[0]+BOARD_W,BOARD_POS[1]+(i*CELL)), 3 if i%3==0 else 1)

		for xidx,row in enumerate(self.board):
			for yidx,num in enumerate(row):
				if num!=0:
					self.text_to_screen(num, xidx, yidx, NUM_FONT)

		notes_font = pygame.font.SysFont("calibri",18,True)
		for xidx, N in enumerate(self.notes):
			for yidx, sub_N in enumerate(N):
				self.notes_draw(sub_N, xidx, yidx, notes_font)
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
		if self.mode == "settings":
			self.screen.fill(SETTINGS)
			self.back.draw(self.screen, SETTINGS)
			font = pygame.font.SysFont("calibri", 50, bold=True)
			settings = font.render("SETTINGS",True,BLACK)
			w = settings.get_width()
			x, y = (WIDTH - w)//2, 30
			font2 = pygame.font.SysFont("inkfree", 20, bold=True)
			level = font2.render("Current difficulty: {}".format(self.difficulty), True, BLACK)
			w2 = level.get_width()
			x2, y2 = (WIDTH - w2)//2, 165
			self.screen.blit(settings,(x,y))
			self.screen.blit(level, (x2,y2))
			for button in self.settingsButton:
				button.draw(self.screen)
		elif self.mode == "difficulty":
			self.screen.fill(SETTINGS)
			font = pygame.font.SysFont("calibri", 50, bold=True)
			settings = font.render("DIFFICULTY",True,BLACK)
			w = settings.get_width()
			x, y = (WIDTH - w)//2, 30
			self.screen.blit(settings,(x,y))
			self.back.draw(self.screen, SETTINGS)
			for button in self.difficultyButtons:
				button.draw(self.screen)
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

	def text_to_screen(self,n,x,y, font_size):
		num_bold = True if n == self.selected_number else False
		if self.wrongs[x][y] == True:
			num_color = RED
		else:
			num_color = BLUE if n==self.selected_number else BLACK
		num_font = pygame.font.SysFont('comicsansms', font_size, num_bold)
		num_text = num_font.render(str(n), True, num_color)
		w = num_text.get_width()
		h = num_text.get_height()
		xi = (CELL - w)//2 + BOARD_POS[0] + y*CELL
		yi = (CELL - h)//2 + BOARD_POS[1] + x*CELL
		self.screen.blit(num_text, (xi,yi))

	def notes_draw(self, numbers, xidx, yidx, font):
		for n in numbers:
			N = font.render(str(n),True,BLACK)
			w = N.get_width()
			h = N.get_height()
			xi = BOARD_POS[0] + yidx*CELL
			yi = BOARD_POS[1] + xidx*CELL
			xi += ((n-1)%3)*(CELL//3)
			yi += ((n-1)//3)*(CELL//3)
			xi += (CELL/3 - w)//2
			yi += (CELL/3 - h)//2
			self.screen.blit(N, (xi,yi))
		pygame.display.update()

	def finish_draw(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						self.__init__()
						self.run()
			w = pygame.Surface((500,200))
			w.set_alpha(10)
			w.fill((128,128,128))
			self.screen.blit(w, (50,250))
			font1 = pygame.font.SysFont('Calibri',40,bold=True)
			font2 = pygame.font.SysFont('inkfree',20)
			t1 = font1.render('Sudoku Finished!', True, BLACK)
			t2 = font2.render('Press Backspace to return',True,BLACK)
			w1 = t1.get_width()
			h1 = t2.get_height()
			x1,y1 = (WIDTH-w1)//2, (HEIGHT-h1)//2
			w2 = t2.get_width()
			h2 = t2.get_height()
			x2,y2 = (WIDTH-w2)//2,(HEIGHT-h2)//2 + h2 + 10
			self.screen.blit(t1, (x1,y1))
			self.screen.blit(t2, (x2,y2))
			pygame.display.update()

#############   HELPER FUNCTIONS #############

	def check_collision(self, button):
		lower1 = self.mousePos[0] >= button.pos[0]
		lower2 = self.mousePos[1] >= button.pos[1]
		upper1 = self.mousePos[0] <= button.pos[0] + button.size[0]
		upper2 = self.mousePos[1] <= button.pos[1] + button.size[1]
		return (lower1 and lower2 and upper1 and upper2)

	def highlight_cell(self):
		cell_w = CELL
		cell_h = CELL

		pygame.draw.rect(self.screen, LLTEAL,
			(BOARD_POS[0]+CELL*3*(self.selected_cell[1]//3),
				BOARD_POS[1]+3*CELL*(self.selected_cell[0]//3),
				CELL*3,
				CELL*3))

		pygame.draw.rect(self.screen, LTEAL,
			(BOARD_POS[0], BOARD_POS[1]+(CELL*self.selected_cell[0]),
				CELL*9,
				CELL))

		pygame.draw.rect(self.screen, LTEAL,
			(BOARD_POS[0]+(CELL*self.selected_cell[1]),
				BOARD_POS[1],
				CELL,
				CELL*9))

		pygame.draw.rect(self.screen,TEAL, (BOARD_POS[0]+self.selected_cell[1]*CELL, BOARD_POS[1]+self.selected_cell[0]*CELL,cell_w, cell_h))

	def highlight_num(self):
		cell_w = CELL
		cell_h = CELL
		same_num_cells = []

		for xidx, row in enumerate(self.board):
			for yidx, num in enumerate(row):
				if num==self.selected_number and num!=0:
					same_num_cells.append((xidx,yidx))

		for x,y in same_num_cells:
			pygame.draw.rect(self.screen, LTEAL, (BOARD_POS[0]+(y*CELL), BOARD_POS[1]+(x*CELL), cell_w, cell_h))


	def get_cell(self):
		if self.mousePos[0] < BOARD_POS[0] or self.mousePos[1] < BOARD_POS[1]:
			return False
		if self.mousePos[0] > BOARD_POS[0]+BOARD_W or self.mousePos[1] > BOARD_POS[1] + BOARD_H:
			return False

		return [(self.mousePos[1]-BOARD_POS[1])//CELL, (self.mousePos[0]-BOARD_POS[0])//CELL]

	def loadButtons(self, key):
		buttons = []
		if key == "menu":
			for i in range(len(BUTTONS["menu"])):
				button = Button(BUTTONS["menu"][i],M_TOP_LEFT[0],M_TOP_LEFT[1]+(M_SPACE+M_BH)*(i+1), M_BW, M_BH, button_color=M_COLOR, font="inkfree", bold=True)
				buttons.append(button)
		elif key == "start":
			for i in range(len(BUTTONS["start"])):
				button = Button(BUTTONS["start"][i],S_X,S_Y,S_BW,S_BH, YELLOW, "inkfree", True)
				buttons.append(button)
		elif key == "settings":
			for i in range(len(BUTTONS["settings"])):
				button = Button(BUTTONS["settings"][i], SE_TOP_LEFT[0], SE_TOP_LEFT[1], SE_BW, SE_BH, SE_COLOR, "inkfree", True)
				buttons.append(button)
		elif key == "difficulty":
			for i in range(len(BUTTONS["difficulty"])):
				button = Button(BUTTONS["difficulty"][i], SE_TOP_LEFT[0], SE_TOP_LEFT[1]+(SE_SPACE+SE_BH)*(i+1), SE_BW, SE_BH, SE_COLOR, "inkfree", True)
				buttons.append(button)
		return buttons

	def filled(self):
		filled = True
		correct = True
		for B in self.board:
			for b in B:
				if b==0:
					filled = False
		
		for i in range(9):
			for j in range(9):
				if self.wrongs[i][j] == True:
					correct = False
		return (filled and correct)