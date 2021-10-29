#window measurements
WIDTH, HEIGHT = 600,700

#BOARD
BOARD_POS = (50,150)
CELL = 55
BOARD_W, BOARD_H = 9*CELL,9*CELL

TESTBOARD = [[0,6,0,2,0,0,8,3,1],
             [0,0,0,0,8,4,0,0,0],
             [0,0,7,6,0,3,0,4,9],
             [0,4,6,8,0,2,1,0,0],
             [0,0,3,0,9,6,0,0,0],
             [1,2,0,7,0,5,0,0,6],
             [7,3,0,0,0,1,0,2,0],
             [8,1,5,0,2,9,7,0,0],
             [0,0,0,0,7,0,0,1,5]]

#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (10,10,10)
BLUE = (44,97,202)
TEAL = (128, 203, 164)
LTEAL = tuple(min(T+40,255) for T in TEAL)
LLTEAL = tuple(min(T+70,255) for T in TEAL)
SCORES = (119, 91, 88)
SETTINGS = (49, 84, 113)
ABOUT = (70,70,70)

#MENU BUTTONS
BUTTONS = ["Start","Scores","Settings","About"]
M_NUM = 4
M_BW = 250
M_BL = 60
M_TOP_LEFT = ((WIDTH - M_BW)//2,180)
M_SPACE = 30
M_COLOR = (120,10,50)