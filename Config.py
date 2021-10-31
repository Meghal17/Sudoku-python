#window measurements
WIDTH, HEIGHT = 600, 700

#BOARD
BOARD_POS = (50,150)
CELL = 55
BOARD_W, BOARD_H = 9*CELL,9*CELL
NUM_FONT = 34


#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (10,10,10)
LGRAY = (180,180,180)
BLUE = (44,97,202)
TEAL = (128, 203, 164)
YELLOW = (231,177,0)
LYELLOW = tuple(min(T+40,255) for T in YELLOW)
LTEAL = tuple(min(T+40,255) for T in TEAL)
LLTEAL = tuple(min(T+70,255) for T in TEAL)
SCORES = (119, 91, 88)
SETTINGS = (49, 84, 113)
ABOUT = (70,70,70)

#BUTTONS
BUTTONS = {"menu":["Start","Scores","Settings","About"], "start": ["Notes"]}

#Menu Button dimensions
M_NUM = 4
M_BW = 250
M_BH = 60
M_TOP_LEFT = ((WIDTH - M_BW)//2,180)
M_SPACE = 30
M_COLOR = (120,10,50)

#Start button dimensions
S_BW = 120
S_BH = 50
S_X, S_Y = 460,15