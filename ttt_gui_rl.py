# Import libraries
import pygame as pg,sys
from pygame.locals import *
import time
from ttt_rl import *

# Initialize global variables
XO = 'x'
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (2,2,2)

# Initialize RL Variables

# Uncomment to train the model and store in pickle file.
#p1 = Player("p1")
#p2 = Player("p2")
#
#state = State(p1, p2)
#print("TRAINING...")
#state.play(50000)
#p1.savePolicy()
#p2.savePolicy()

# Loading in the computer.
p1 = Player("computer", exp_rate=0)
p1.loadPolicy("policy_p1")

p2 = HumanPlayer("human")

state = State(p1, p2)


# TicTacToe 3x3 board
TTT = [[None]*3,[None]*3,[None]*3]

# Initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100),0,32)
pg.display.set_caption("Tic Tac Toe")

# Loading the images
opening = pg.image.load('images/ttt_blank.jpg')
x_img = pg.image.load('images/xxx.jpg')
o_img = pg.image.load('images/oo.jpg')

# Resizing images
x_img = pg.transform.scale(x_img, (80,80))
o_img = pg.transform.scale(o_img, (80,80))
opening = pg.transform.scale(opening, (width, height+100))

# no change in this function.
def game_opening():
    screen.blit(opening,(0,0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    
    # Drawing vertical lines
    pg.draw.line(screen,line_color,(width/3,0),(width/3, height),7)
    pg.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height),7)
    # Drawing horizontal lines
    pg.draw.line(screen,line_color,(0,height/3),(width, height/3),7)
    pg.draw.line(screen,line_color,(0,height/3*2),(width, height/3*2),7)
    draw_status()
    
# no change here also.
def draw_status():
    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game Draw!'

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # Copy the rendered message onto the board
    screen.fill ((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()

#no changes here
def check_win():
    global TTT, winner, draw

    # Check for winning rows
    for row in range (0,3):
        if ((TTT [row][0] == TTT[row][1] == TTT[row][2]) and(TTT [row][0] is not None)):
            winner = TTT[row][0]
            pg.draw.line(screen, (250,0,0), (0, (row + 1)*height/3 -height/6),\
                              (width, (row + 1)*height/3 - height/6 ), 4)
            break

    # Check for winning columns
    for col in range (0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # This column won
            winner = TTT[0][col]
            # Draw winning line
            pg.draw.line (screen, (250,0,0),((col + 1)* width/3 - width/6, 0),\
                          ((col + 1)* width/3 - width/6, height), 4)
            break

    # Check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # Game won diagonally left to right
        winner = TTT[0][0]
        pg.draw.line (screen, (250,70,70), (50, 50), (350, 350), 4)
       

    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # Game won diagonally right to left
        winner = TTT[0][2]
        pg.draw.line (screen, (250,70,70), (350, 50), (50, 350), 4)
    
    if(all([all(row) for row in TTT]) and winner is None ):
        draw = True
    draw_status()


def drawXO(row,col):
    global TTT, XO
    if row==1:
        posx = 30
    if row==2:
        posx = width/3 + 30
    if row==3:
        posx = width/3*2 + 30

    if col==1:
        posy = 30
    if col==2:
        posy = height/3 + 30
    if col==3:
        posy = height/3*2 + 30

    #################################
    TTT[row-1][col-1] = XO

    if(XO == 'x'):
        screen.blit(x_img,(posy,posx))
        XO= 'o'
    else:
        screen.blit(o_img,(posy,posx))
        XO= 'x'
    pg.display.update()
   
    

def userClick():
    '''
    global x0, if x then get row, col from computer, else get from user.
    '''
    global XO, state

    if XO == 'x':
        positions = state.availablePositions()
        p1_action = state.p1.chooseAction(positions, state.board, state.playerSymbol)

        state.updateState(p1_action)

        drawXO(p1_action[0] + 1, p1_action[1] + 1)
        check_win()

    else:
        # Get coordinates of mouse click
        x,y = pg.mouse.get_pos()

        # Get column of mouse click (1-3)
        if(x<width/3):
            col = 1
        elif (x<width/3*2):
            col = 2
        elif(x<width):
            col = 3
        else:
            col = None
            
        # Get row of mouse click (1-3)
        if(y<height/3):
            row = 1
        elif (y<height/3*2):
            row = 2
        elif(y<height):
            row = 3
        else:
            row = None
        

        if(row and col and TTT[row-1][col-1] is None):
            
            # Draw the x or o on screen
            ############################################################### only if x0 is o, else no user input.
            p2_action = (row-1, col-1)

            state.updateState(p2_action)

            drawXO(row,col)
            check_win()
            
        

def reset_game():
    global TTT, winner, XO, draw, state
    time.sleep(3)
    XO = 'x'
    draw = False
    winner=None
    game_opening()
    TTT = [[None]*3,[None]*3,[None]*3]
    state.reset()

game_opening()

# Run the game loop forever
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if XO == 'x':
            userClick()
            if (winner or draw):
                reset_game()
        if XO == 'o':
            if event.type == MOUSEBUTTONDOWN:
                userClick()
                if(winner or draw):
                    reset_game()
            
    pg.display.update()
    CLOCK.tick(fps)
