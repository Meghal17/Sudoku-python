import pygame, sys
from Config import *
from ButtonClass import *
import os, random, time

class App():
	def __init__(self):
		pygame.init()
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
		self.start_time = None
		self.best_score_flag = False
		self.locked_cells = []
		self.game_elapsed_time = 0
		self.mistakes = 0
		self.game_score = 0
		self.notes = [ [[] for _ in range(9)] for _ in range(9)]
		with open('Data/difficulty.txt','r') as file:
			self.difficulty = file.read()
			if self.difficulty == '':
				self.difficulty = "breezy"
		self.board, self.solution = self.fetch_board()
		self.finished = False
		self.wrongs = [[False for _ in range(9)] for _ in range(9)]
		self.selected_number = None
		self.gameButtons = self.loadButtons("start")
		self.menuButtons = self.loadButtons("menu")
		self.difficultyButtons = self.loadButtons("difficulty")
		self.scoreButtons = self.loadButtons("scores")
		self.gameRunning = False

	def run(self):
		while self.running:
			self.main_events()
			self.mousePos = pygame.mouse.get_pos()
			if self.mode != "start" and self.gameRunning:
				self.gameRunning = False
				self.game_elapsed_time += time.time() - self.start_time
			if self.mode == "menu":
				self.menu_draw()
				for button in self.menuButtons:
					button.update(self.mousePos)
			elif self.mode == "start":
				if not self.gameRunning:
					self.gameRunning = True
					self.start_time = time.time()
				self.game_draw()
				if self.selected_cell:
					self.selected_number = self.board[self.selected_cell[0]][self.selected_cell[1]]
				if self.notes_mode:
					self.gameButtons[0].button_color = LYELLOW
				else:
					self.gameButtons[0].button_color = YELLOW
				if self.filled():
					self.game_elapsed_time += time.time() - self.start_time
					self.get_score()
					self.update_scores()
					self.mistakes = 0
					self.finish_draw()
			elif self.mode == "scores" or self.mode == "scoring":
				self.scores_draw()
				for button in self.scoreButtons:
					button.update(self.mousePos)
			elif self.mode == "difficulty":
				self.difficulty_draw()
				for button in self.difficultyButtons:
					button.update(self.mousePos)
			elif self.mode == "help":
				self.help_draw()
		pygame.quit()
		sys.exit()

#############   EVENTS FUNCTIONS #############

	def main_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				with open('Data/difficulty.txt','w') as file:
					file.truncate(0)
					file.write(self.difficulty)
				self.running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.mode == "scoring" and self.check_collision(self.back):
					self.mode = "scores"
				elif self.mode != "menu" and self.check_collision(self.back):
					self.mode = "menu"

				if self.mode =="menu":
					for button in self.menuButtons:
						if self.check_collision(button):
							self.mode = button.text.lower()
				elif self.mode == "scores":
					for button in self.scoreButtons:
						if self.check_collision(button):
							self.mode = button.text.lower()

				elif self.mode == "start":
					self.selected_cell = self.get_cell()
					if self.check_collision(self.gameButtons[0]):
						self.notes_mode = not(self.notes_mode)
				elif self.mode == "difficulty":
					for button in self.difficultyButtons:
						if self.check_collision(button):
							self.difficulty = button.text.lower()
							self.board, self.solution = self.fetch_board()
							self.notes = [ [[] for _ in range(9)] for _ in range(9)]
							self.mode = "menu"

			elif event.type == pygame.KEYDOWN:
				if self.mode == 'start':
					if event.key == pygame.K_n and self.selected_cell:
						self.notes_mode = not(self.notes_mode)
					if self.selected_cell != None:
						if event.key == pygame.K_UP:
							self.selected_cell[0] = max(0,self.selected_cell[0]-1)
						elif event.key == pygame.K_LEFT:
							self.selected_cell[1] = max(0,self.selected_cell[1]-1)
						elif event.key == pygame.K_RIGHT:
							self.selected_cell[1] = min(8,self.selected_cell[1]+1)
						elif event.key == pygame.K_DOWN:
							self.selected_cell[0] = min(8, self.selected_cell[0]+1)

					if self.selected_cell != None and (self.selected_cell not in self.locked_cells) and (event.unicode in list('123456789')):

						if self.notes_mode:
							self.board[self.selected_cell[0]][self.selected_cell[1]] = 0
							if int(event.unicode) in self.notes[self.selected_cell[0]][self.selected_cell[1]]:
								self.notes[self.selected_cell[0]][self.selected_cell[1]].remove(int(event.unicode))
								self.selected_number = None
							else:
								if not self.check_num_rcg(int(event.unicode), self.selected_cell):
									self.notes[self.selected_cell[0]][self.selected_cell[1]].append(int(event.unicode))
									self.selected_number = int(event.unicode)
						else:
							if not self.check_num_rcg(int(event.unicode), self.selected_cell):
								self.board[self.selected_cell[0]][self.selected_cell[1]] = int(event.unicode)
								self.selected_number = int(event.unicode)
								self.notes[self.selected_cell[0]][self.selected_cell[1]] = []

								if int(event.unicode) != self.solution[self.selected_cell[0]][self.selected_cell[1]]:
									self.wrongs[self.selected_cell[0]][self.selected_cell[1]] = True
									self.mistakes += 1
								else:									
									self.locked_cells.append([self.selected_cell[0],self.selected_cell[1]])
									self.wrongs[self.selected_cell[0]][self.selected_cell[1]] = False

					if event.key == pygame.K_BACKSPACE and self.selected_cell and self.selected_cell not in self.locked_cells and not(self.notes_mode):
						self.board[self.selected_cell[0]][self.selected_cell[1]] = 0
						self.selected_number = None

#############   FETCH BOARD FUNCTION #############

	def fetch_board(self):
		board_path = "Data/boards"
		n = random.randint(1,10000)
		filename = os.path.join(board_path,self.difficulty+'.csv')
		with open(filename) as file:
			for i in range(n+1):
				data = file.readline()[:-1]
			board_data, sol_data = data.split(',')
		board = [[] for _ in range(9)]
		solution = [[] for _ in range(9)]
		for i in range(len(board_data)):
			board[i//9].append(int(board_data[i]))
			solution[i//9].append(int(sol_data[i]))
		self.locked_cells = []
		for xidx,row in enumerate(board):
			for yidx,num in enumerate(row):
				if num!=0:
					self.locked_cells.append([xidx, yidx])
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
		font = pygame.font.SysFont("calibri",42, bold=True)
		if self.mode == "scores":
			for button in self.scoreButtons:
				button.draw(self.screen)
			text = font.render("SCORES", True, BLACK)
			w = text.get_width()
			x,y = (WIDTH - w)//2, 30
			self.screen.blit(text, (x,y))

			font1 = pygame.font.SysFont("calibri", 38, bold=True)
			text1 = font1.render("Difficulty", True, BLACK)
			text2 = font1.render("Average", True, BLACK)
			text3 = font1.render("Best",True, BLACK)
			self.screen.blit(text1, (50,120))
			self.screen.blit(text2, (250,120))
			self.screen.blit(text3, (450,120))
			with open('Data/scores.txt') as file:
				scores = file.read().splitlines()
			font2 = pygame.font.SysFont("calibri", 34, False)
			difficulty = ["Breezy","Easy","Medium","Hard","Evil"]
			for i in range(5):
				level = font2.render(difficulty[i],True,BLACK)
				average = font2.render(scores[i].split(' ')[0],True,BLACK)
				best = font2.render(scores[i].split(' ')[2], True,BLACK)
				self.screen.blit(level, (50,120 + ((i+1)*80)))
				self.screen.blit(average, (250, 120 + ((i+1)*80)))
				self.screen.blit(best	, (450, 120 + ((i+1)*80)))

		elif self.mode == "scoring":
			text = font.render("SCORING RULES", True, BLACK)
			w,h = text.get_width(), text.get_height()
			x,y = (WIDTH-w)//2, 50
			self.screen.blit(text, (x,y))
			font1 = pygame.font.SysFont('Calibri',22, bold=True)
			text1 = ["Each difficulty level has an associated par time. Completing","a puzzle under par time rewards you with 1 bonus point for","each second.","","Additionally there's a base score for each difficulty level.","However, penalty points will be deducted for each mistake.","","Mistake: Entering an incorrect number in a cell."]
			for i in range(len(text1)):
				t = font1.render(text1[i],True, BLACK)
				self.screen.blit(t, (25,100+(i*25)))
			font2 = pygame.font.SysFont('Calibri',24,bold = True)
			header = ["Difficulty","Par Time","Base Score","Penalty"]
			for i in range(len(header)):
				text =  font2.render(header[i],True,BLACK)
				self.screen.blit(text,(50+(i*150),350))
			difficulty = ["Breezy","Easy","Medium","Hard","Evil"]
			par_times = ["300","600","900","1200","1500"]
			base_scores = ["100","200","300","400","500"]
			penalties = ["25","50","75","100","125"]
			for i in range(5):
				level = font1.render(difficulty[i], True, BLACK)
				par = font1.render(par_times[i], True, BLACK)
				base = font1.render(base_scores[i], True, BLACK)
				pen = font1.render(penalties[i], True, BLACK)
				self.screen.blit(level,(50,400+(i*35)))
				self.screen.blit(par, (200,400+(i*35)))
				self.screen.blit(base, (350,400+(i*35)))
				self.screen.blit(pen, (500,400+(i*35)))
		pygame.display.update()

	def difficulty_draw(self):
		self.screen.fill(DIFF)
		font2 = pygame.font.SysFont("calibri", 28, bold=True)
		level = font2.render("Current: {}".format(self.difficulty), True, BLACK)
		w2 = level.get_width()
		x2, y2 = (WIDTH - w2)//2, 150
		self.screen.blit(level, (x2,y2))
		font = pygame.font.SysFont("calibri", 50, bold=True)
		difficulty = font.render("DIFFICULTY",True,BLACK)
		w = difficulty.get_width()
		x, y = (WIDTH - w)//2, 30
		self.screen.blit(difficulty,(x,y))
		self.back.draw(self.screen, DIFF)
		for button in self.difficultyButtons:
			button.draw(self.screen, selected=button.text.lower()==self.difficulty)
		pygame.display.update()

	def help_draw(self):
		self.screen.fill(HELP)
		self.back.draw(self.screen, HELP)
		font = pygame.font.SysFont("calibri", 50, bold=True)
		font1 = pygame.font.SysFont("calibri", 34, bold=True)
		text1 = font.render("How to Play?", True, BLACK)
		self.screen.blit(text1, ((WIDTH - text1.get_width())//2,30))
		font2 = pygame.font.SysFont("Calibri",24,bold=True)
		ins = ["The objective of Sudoku game is to fill each empty cell","of a 9x9 grid with a number such that each row, each","column and each 3x3 block contains all digits from", "1 to 9 only once.","","The numbers already present on the board cannot be", "changed. There is only one correct solution to each", "Sudoku puzzle","","For scoring rules refer to \"Scoring\" section in Scores.","","Use mouse or arrow-keys to change cells."]
		for i in range(len(ins)):
				text =  font2.render(ins[i],True,BLACK)
				self.screen.blit(text,(30,170+(i*25)))

		dev = font1.render('Developed by: Meghal Darji', True, BLACK)
		self.screen.blit(dev,((WIDTH - dev.get_width())//2,550))
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

	def finish_draw(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						difficulty = self.difficulty
						self.__init__()
						self.difficulty = difficulty
						self.run()
			w = pygame.Surface((500,200))
			w.set_alpha(10)
			w.fill((128,128,128))
			self.screen.blit(w, (50,250))
			if self.best_score_flag:
				font = pygame.font.SysFont('Calibri',36, bold=True)
				text = font.render('New Best Score!',True, BLACK)
				w,h = text.get_width(), text.get_height()
				x,y = (WIDTH - w)//2, (HEIGHT - h)//2 - 40
				self.screen.blit(text, (x,y))
			font1 = pygame.font.SysFont('Calibri',34,bold=True)
			font2 = pygame.font.SysFont('inkfree',20)
			t1 = font1.render('Sudoku Finished! Score:{}'.format(self.game_score), True, BLACK)
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
		# print([(self.mousePos[1]-BOARD_POS[1])//CELL, (self.mousePos[0]-BOARD_POS[0])//CELL])
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
				button = Button(BUTTONS["start"][i],S_X,S_Y,S_BW,S_BH, YELLOW, "mvboli", True)
				buttons.append(button)
		elif key == "difficulty":
			for i in range(len(BUTTONS["difficulty"])):
				button = Button(BUTTONS["difficulty"][i], SE_TOP_LEFT[0], SE_TOP_LEFT[1]+(SE_SPACE+SE_BH)*(i+1), SE_BW, SE_BH, SE_COLOR, "inkfree", True)
				buttons.append(button)
		elif key == "scores":
			for i in range(len(BUTTONS["scores"])):
				button = Button(BUTTONS['scores'][i], (WIDTH - 200)//2,600, 200, 50, YELLOW, "inkfree", True)
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

	def check_num_rcg(self, n, cell):
		xidx, yidx = cell
		for i in range(9):
			if self.board[xidx][i] == n:
				return True
			if self.board[i][yidx] == n:
				return True

		for i in range((xidx//3)*3, (xidx//3+1)*3):
			for j in range((yidx//3)*3, (yidx//3+1)*3):
				if self.board[i][j] == n:
					return True
		return False

	def get_score(self):
		self.game_score = round((BASE[self.difficulty] - self.mistakes * PEN[self.difficulty] + max(0, (PAR_TIME[self.difficulty] - self.game_elapsed_time))),2)

	def update_scores(self):
		diff_map = {"breezy":0,"easy":1,"medium":2,"hard":3,"evil":4}
		with open('Data/scores.txt',"r+") as file:
			scores = file.read().split('\n')
			idx = diff_map[self.difficulty]
			avg_score, num_games, best_score = map(float, scores[idx].split(' '))
			if self.game_score > best_score:
				best_score = self.game_score
				self.best_score_flag = True
			num_games += 1
			new_avg_score = round(((avg_score*(num_games-1) + self.game_score)/num_games), 2)
			scores[idx] = str(new_avg_score) +' '+str(num_games) +' ' + str(best_score)
			file.seek(0)
			file.truncate(0)
			scores = '\n'.join(scores)
			file.write(scores)