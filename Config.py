#window measurements
# HEIGHT = 700
WIDTH, HEIGHT = 600, 700

#BOARD
BOARD_POS = (50,150)
CELL = 55
BOARD_W, BOARD_H = 9*CELL,9*CELL
NUM_FONT = 34


#COLORS
RED = (160,0,0)
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
DIFF = (49, 84, 113)
ABOUT = (70,70,70)

#BUTTONS
BUTTONS = {"menu":["Start","Scores","Difficulty","About"], "start": ["Notes"],  "difficulty":["Breezy","Easy","Medium","Hard","Evil"]}

#Menu Button dimensions and locations
M_BW = 250
M_BH = 60
M_TOP_LEFT = ((WIDTH - M_BW)//2,180)
M_SPACE = 30
M_COLOR = (120,10,50)

#Settings button dimensions and locations
SE_BW = 250
SE_BH = 60
SE_TOP_LEFT = ((WIDTH - SE_BW)//2,100)
SE_SPACE = 30
SE_COLOR = (204,157,0)

#Start button dimensions and locations
S_BW = 120
S_BH = 50
S_X, S_Y = 460, 15

#Score calculations
PAR_TIME = {"breezy":300,"easy":600, "medium":900,"hard":1200, "evil":1500}
PEN = {"breezy":25,"easy":50, "medium":75,"hard":100, "evil":125}
BASE = {"breezy":100,"easy":200, "medium":300,"hard":400, "evil":500}


#SCORES in scores.txt are stored as Average, num_games and best score