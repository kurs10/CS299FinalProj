import sys, pygame, random, time,HS
from pygame.locals import *

# Window setup
FPS = 25
WINDOW_WIDTH = 640  # Window 640 pixels wide
WINDOW_HEIGHT = 480  # Winow 480 pixels high
BOX_SIZE = 20  # 20x20 pixels
GAME_WIDTH = 10  # Game board is 10 boxes wide
GAME_HEIGHT = 20  # Game board is 20 boxes tall

# Margins between the game and window edge
# Margin from window leftright = (Total Window width - Game Width)/2
X_MARGIN = int((WINDOW_WIDTH - GAME_WIDTH * BOX_SIZE) / 2)
# Margin from top = (Total window height - Game Height) - 10
# 10 is the distance from board to bottom
TOP_MARGIN = WINDOW_HEIGHT - (GAME_HEIGHT * BOX_SIZE) - 10

# Piece moves one space to the left or right every 0.15s when the left/right arrow key is held
SIDEWAYS_MOVE_FREQ = 0.15
# Piece moves one space down every 0.1s when the down arrow key is held
DOWN_MOVE_FREQ = 0.1

# Color setup (RGB) for tetris block and its shadow
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (216, 0, 0)
L_RED = (240, 0, 0)
GREEN = (0, 216, 0)
L_GREEN = (0, 240, 0)
BLUE = (0, 0, 216)
L_BLUE = (0, 0, 240)
YELLOW = (216, 216, 0)
L_YELLOW = (240, 240, 0)
CYAN = (0, 216, 216)
L_CYAN = (0, 240, 240)
ORANGE = (216, 144, 0)
L_ORANGE = (240, 160, 51)
PURPLE = (144, 0, 216)
L_PURPLE = (160, 0, 240)

# Assigns piece colors to an index
PIECE_COLOR = {"S": 0, "Z": 1, "J": 2, "L": 3, "I": 4, "O": 5, "T": 6}
# Block Colors
COLORS = (GREEN, RED, BLUE, ORANGE, CYAN, YELLOW, PURPLE)
# Block Colors HighLight
L_COLORS = (L_GREEN, L_RED, L_BLUE, L_ORANGE, L_CYAN, L_YELLOW, L_PURPLE)

# If false, raise an assertionError Exception
# Make sure each color has an equal ligher color
assert len(COLORS) == len(L_COLORS), "Not all colors have a lighter equal"

# Assigning colors to the game
BORDER_COLOR = BLUE
BG_COLOR = BLACK
TEXT_COLOR = WHITE
TEXT_SHADOW_COLOR = GRAY

# Piece setup ("x" is a box and "." is an empty space )
# Each template contains the normal and all rotated positions
# These templates are stored into a dictionary
BLANK = "."
TEMPLATE_WIDTH = 5  # Templates will be 5x5 the area of shape rotation
TEMPLATE_HEIGHT = 5

S_PIECE = [[".....",
            ".....",
            "..xx.",
            ".xx..",
            "....."],
           [".....",
            "..x..",
            "..xx.",
            "...x.",
            "....."]]

Z_PIECE = [[".....",
            ".....",
            ".xx..",
            "..xx.",
            "....."],
           [".....",
            "..x..",
            ".xx..",
            ".x...",
            "....."]]

I_PIECE = [["..x..",
            "..x..",
            "..x..",
            "..x..",
            "....."],
           [".....",
            ".....",
            "xxxx.",
            ".....",
            "....."]]

O_PIECE = [[".....",
            ".....",
            ".xx..",
            ".xx..",
            "....."]]

J_PIECE = [[".....",
            ".x...",
            ".xxx.",
            ".....",
            "....."],
           [".....",
            "..xx.",
            "..x..",
            "..x..",
            "....."],
           [".....",
            ".....",
            ".xxx.",
            "...x.",
            "....."],
           [".....",
            "..x..",
            "..x..",
            ".xx..",
            "....."]]

L_PIECE = [[".....",
            "...x.",
            ".xxx.",
            ".....",
            "....."],
           [".....",
            "..x..",
            "..x..",
            "..xx.",
            "....."],
           [".....",
            ".....",
            ".xxx.",
            ".x...",
            "....."],
           [".....",
            ".xx..",
            "..x..",
            "..x..",
            "....."]]

T_PIECE = [[".....",
            "..x..",
            ".xxx.",
            ".....",
            "....."],
           [".....",
            "..x..",
            "..xx.",
            "..x..",
            "....."],
           [".....",
            ".....",
            ".xxx.",
            "..x..",
            "....."],
           [".....",
            "..x..",
            ".xx..",
            "..x..",
            "....."]]

PIECES = {"S": S_PIECE, "Z": Z_PIECE, "J": J_PIECE, "L": L_PIECE,
          "I": I_PIECE, "O": O_PIECE, "T": T_PIECE}


# Sets up the game, runs it, and checks for quit
def runGame():
    # Create new game
    game = getBlankGame()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    # Calcuates the level and fall frequency based on score
    # Level increase and Fall Frequency increase the higher the score
    level, FALL_FREQ = calcLevel(score)

    curPiece = getPiece()
    nextPiece = getPiece()

    # Game loop
    while True:
        # Checks if there is no current piece and starts a new piece at the top if there isn't
        if curPiece == None:
            curPiece = nextPiece
            nextPiece = getPiece()
            lastFallTime = time.time()  # Reset last fall time

            # Checks if unable to fit the current piece on the board (game over if unable)
            if not isValidPosition(game, curPiece):
                return

        checkForQuit()
        # Event handling (Pause Game,Rotate Piece, Move Piece Down)
        for event in pygame.event.get():
            # If key is released
            if event.type == KEYUP:
                # If p key released
                if (event.key == K_p):
                    # Pause the game
                    # Display board with black screen
                    DISPLAY_SURF.fill(BG_COLOR)
                    pygame.mixer.music.stop()
                    # Will show "Paused" until a key is pressed
                    showTextScreen("Paused")
                    # Once a key is pressed , restart music
                    pygame.mixer.music.play(-1, 0.0)
                    # Resest times to current time
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                # If left arrow key released
                elif event.key == K_LEFT:
                    movingLeft = False  # No longer rotating
                # If left arrow key released
                elif event.key == K_RIGHT:
                    movingRight = False  # No longer rotating
                # If down arrow key released
                elif event.key == K_DOWN:
                    movingDown = False  # No longer moving doww

            # =====Code dealing with moving piecies=====START
            # Else if a key is pressed
            elif event.type == KEYDOWN:
                # MOVE LEFT
                # If left arrow key or a is pressed and new positin is a valid position
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(game, curPiece, adjX=-1):
                    # Update x position by 1 to the left
                    curPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                # MOVE RIGHT
                # If right arrow key or d is pressed and new positin is a valid position
                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(game, curPiece, adjX=1):
                    # Update x position by 1 to the right
                    curPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # TO MOVE DOWN
                # If down arrow key or s is pressed 
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    # If new position is a valid position
                    if isValidPosition(game, curPiece, adjY=1):
                        # Update y position by 1 down
                        curPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # TO MOVE DOWN ALL THE WAY
                # If space bar is pressed         
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    # For each row in board starting at 1 row from the top
                    for i in range(1, GAME_HEIGHT):
                        # If new row is not a valid position then stop at i
                        if not isValidPosition(game, curPiece, adjY=i):
                            break
                    # Set lowest valid row possibile as 1 row above row i
                    curPiece['y'] += i - 1

                # ROTATE CLOCKWISE
                # If up arrow key or w is pressed 
                elif (event.key == K_UP or event.key == K_w):
                    # Update rotation key value by +1
                    curPiece['rotation'] = (curPiece['rotation'] + 1) % len(PIECES[curPiece['shape']])
                    # If rotation value is larger than num of rotations, roll over and set rotation value to 0
                    if not isValidPosition(game, curPiece):
                        # Revert rotation to previous
                        curPiece['rotation'] = (curPiece['rotation'] - 1) % len(PIECES[curPiece['shape']])

                # ROTATE COUNTERCLOCKWISE
                # If q key is pressed
                elif (event.key == K_q):
                    # Update rotation key value by -1    
                    curPiece['rotation'] = (curPiece['rotation'] - 1) % len(PIECES[curPiece['shape']])
                    # If new rotation of piece is not a valid position
                    if not isValidPosition(game, curPiece):
                        # Revert rotation to previous
                        curPiece['rotation'] = (curPiece['rotation'] + 1) % len(PIECES[curPiece['shape']])

        # HOLDING DOWN RIGHT OR LEFT ARROW KEY                
        # If moving left or right true
        # AND time elapsed since piece last moved sideways is greater than the sideways move frequecy
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > SIDEWAYS_MOVE_FREQ:
            # If moving left and new postition(1 space to the right) is a valid position
            if movingLeft and isValidPosition(game, curPiece, adjX=-1):
                # Update x position by -1
                curPiece['x'] -= 1
            # If moving right and new postition(1 space to the right) is a valid position
            elif movingRight and isValidPosition(game, curPiece, adjX=1):
                # Update x position by -1
                curPiece['x'] += 1
            # Update last move sidways time to current time
            lastMoveSidewaysTime = time.time()

        # If piece is moving down
        if movingDown:
            # If time elapsed since peice last moved down is greater than the down move frequency
            if time.time() - lastMoveDownTime > DOWN_MOVE_FREQ:
                # If 1 row down is a valid position
                if isValidPosition(game, curPiece, adjY=1):
                    # Move piece down by 1
                    curPiece['y'] += 1
                    # Update last move down time
                    lastMoveDownTime = time.time()

        # If time elapsed since peice last fell is greater than its fall frequency
        if time.time() - lastFallTime > FALL_FREQ:
            # If piece is already in place (aka 1 row down is not valid position)
            if not isValidPosition(game, curPiece, adjY=1):
                # Add piece to gameboard
                addToBoard(game, curPiece)
                # Check if there are any full rows and delete them and update score
                score += deleteFullRows(game)
                # Update level and fall frequency based on score
                level, FALL_FREQ = calcLevel(score)
                # No more current piece
                curPiece = None
            # Else if piece is still falling
            else:
                # Move piece one row down
                curPiece['y'] += 1
                # Update last fall time
                lastFallTime = time.time()

        # =====Code dealing with moving piecies=====END

        # Draws the current game status
        DISPLAY_SURF.fill(BG_COLOR)
        drawGame(game)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if curPiece != None:
            drawPiece(curPiece)
        # Updates entire screen
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


# Determines the level the player is on and how many seconds should pass until current piece
# falls into a space
def calcLevel(score):
    # Level increases every 10 points/lines cleared, starts at level 1
    level = int(score / 10) + 1
    # Blocks fall faster by 0.02 secs as level increases (but max speed reached at level 13)
    if (level > 13):
        FALL_FREQ = 0.27 - (13 * 0.02)
    else:
        FALL_FREQ = 0.27 - (level * 0.02)
    return level, FALL_FREQ


# Returns a random new piece
def getPiece():
    shape = random.choice(list(PIECES.keys()))
    newPiece = {"shape": shape,
                "rotation": random.randint(0, len(PIECES[shape]) - 1),
                "x": int(GAME_WIDTH / 2) - int(TEMPLATE_WIDTH / 2),
                "y": -2,
                "color": PIECE_COLOR[shape]}
    return newPiece


# Returns true if the piece is within the board and there are no collisions
# adjX, adjY used to adjust piece coordiates to actual board coordinates
def isValidPosition(game, piece, adjX=0, adjY=0):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            isAboveBoard = y + piece["y"] + adjY < 0
            # If the piece is above the board or is a blacnk space
            if isAboveBoard or PIECES[piece["shape"]][piece["rotation"]][y][x] == BLANK:
                continue
            # If a part of the piece is not located on board
            if not isOnBoard(x + piece["x"] + adjX, y + piece["y"] + adjY):
                return False
            # If a part of the pice is located on coordinate of board that is not blank (aka already occupied)
            if game[x + piece["x"] + adjX][y + piece["y"] + adjY] != BLANK:
                return False
    return True


# Checks if the given coordinate is on the game board
def isOnBoard(x, y):
    return x >= 0 and x < GAME_WIDTH and y < GAME_HEIGHT


# Creates and returns a new blank game
def getBlankGame():
    game = []
    for i in range(GAME_WIDTH):
        game.append([BLANK] * GAME_HEIGHT)
    return game


# Draws the current state of the game board
def drawGame(game):
    # Draws the board's border
    pygame.draw.rect(DISPLAY_SURF, BORDER_COLOR,
                     (X_MARGIN - 3, TOP_MARGIN - 7, (GAME_WIDTH * BOX_SIZE) + 8, (GAME_HEIGHT * BOX_SIZE) + 8), 5)

    # Fills the board's background
    pygame.draw.rect(DISPLAY_SURF, BG_COLOR, (X_MARGIN, TOP_MARGIN, BOX_SIZE * GAME_WIDTH, BOX_SIZE * GAME_HEIGHT))

    # Draws the boxes on the board
    for x in range(GAME_WIDTH):
        for y in range(GAME_HEIGHT):
            drawBox(x, y, game[x][y])


# Draws the specified piece
def drawPiece( piece, pixelX=None, pixelY=None ):
    # Set shapes with piece's shape and rotation
    shape = PIECES[piece["shape"]][piece["rotation"]]
    # If no pixel coordinates given
    if pixelX == None and pixelY == None:
        # Convert board coordiates to pixel coordinates
        pixelX, pixelY = convertToPixel(piece["x"], piece["y"])
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if shape[y][x] != BLANK:
                drawBox(None, None, piece["color"], pixelX + (x * BOX_SIZE), pixelY + (y * BOX_SIZE))


# Draws the next piece
def drawNextPiece(piece, pixelX=None, pixelY=None):
    # Displays "Next:" on screen
    nextSurf = BASIC_FONT.render('Next:', True, TEXT_COLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOW_WIDTH - 120, 80)
    DISPLAY_SURF.blit(nextSurf, nextRect)
    # Draws the next piece on side of board
    drawPiece(piece, pixelX=WINDOW_WIDTH - 120, pixelY=100)


# Draws a single box given x,y board coordinated or x,y pixel coordinates
def drawBox(x, y, color, pixelX=None, pixelY=None):
    # If no color given, exit function
    if color == BLANK:
        return
    # If no pixel coordinates given
    if pixelX == None and pixelY == None:
        # Convert booard coordinates to pixel coordinates
        pixelX, pixelY = convertToPixel(x, y)
    # Draw box with darker color first 
    pygame.draw.rect(DISPLAY_SURF, COLORS[color], (pixelX + 1, pixelY + 1, BOX_SIZE - 1, BOX_SIZE - 1))
    # Draw box with lighter color (for shading)
    pygame.draw.rect(DISPLAY_SURF, L_COLORS[color], (pixelX + 1, pixelY + 1, BOX_SIZE - 4, BOX_SIZE - 4))


# Draws the current score and level
def drawStatus(score, level):
    # Draws score
    scoreSurf = BASIC_FONT.render("Score: %s" % score, True, TEXT_COLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_WIDTH - 150, 20)
    DISPLAY_SURF.blit(scoreSurf, scoreRect)  # Draws scoreSurf at given rectangle on display

    # Draws level
    levelSurf = BASIC_FONT.render('Level: %s' % level, True, TEXT_COLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOW_WIDTH - 150, 50)
    DISPLAY_SURF.blit(levelSurf, levelRect)  # Draws levelSurf at given rectangle on display


# Adds piece permanelty to board once piece has landed
def addToBoard(game, piece):
    # For evrey box in 5x5 template
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            # If box is not blank/ is part of piece
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                # Color in box located in board with pieces location
                game[x + piece['x']][y + piece['y']] = piece['color']


# Checks is a row is fully filled, return True is whole row is filled
def isRowFull(game, y):
    # For each box in row y
    for x in range(GAME_WIDTH):
        # If box is empty
        if game[x][y] == BLANK:
            # Row not full
            return False
    return True


# Deletes all full rows on board and shifts rows down 
def deleteFullRows(game):
    rowsDel = 0
    # Start at bottom row
    y = GAME_HEIGHT - 1
    while y >= 0:
        # If row y is full
        if isRowFull(game, y):
            # Delete row y and shift all rows above it down 
            # For all rows above row y
            for pullDownY in range(y, 0, -1):
                for x in range(GAME_WIDTH):
                    # Set row as row above it
                    game[x][pullDownY] = game[x][pullDownY - 1]
            # Set very top row as blank.
            for x in range(GAME_WIDTH):
                game[x][0] = BLANK
            rowsDel += 1
        # Else if row y is not full
        else:
            # Check next row up
            y -= 1
    # Return rows deleted to update score
    return rowsDel


# Converts the given xy coordinates of the board to pixel coordinates on the screen
def convertToPixel(x, y):
    return (X_MARGIN + (x * BOX_SIZE)), (TOP_MARGIN + (y * BOX_SIZE))

# Generic Button Create Function
def button (text,x,y,w,h,color,hColor,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(DISPLAY_SURF, hColor,(x,y,w,h))
        
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(DISPLAY_SURF,color,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",14)
    #textSurf = smallText.render(text, True, BLACK)
    textSurf,textRect = makeTextObjs(text,smallText,BLACK)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    DISPLAY_SURF.blit(textSurf, textRect)

# Displays the text screen (generic text screen function)
def showTextScreen(text):
    # Draws the shadow for the text (For looks purposes)
    titleSurf, titleRect = makeTextObjs(text, BIG_FONT, TEXT_SHADOW_COLOR)
    titleRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    DISPLAY_SURF.blit(titleSurf, titleRect)

    # Draws the text
    titleSurf, titleRect = makeTextObjs(text, BIG_FONT, TEXT_COLOR)
    titleRect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3)
    DISPLAY_SURF.blit(titleSurf, titleRect)    

    if text == "Paused":
        # Draws the "Press a key to play." text
        pressKeySurf, pressKeyRect = makeTextObjs("Press a key to play.", BASIC_FONT, TEXT_COLOR)
        pressKeyRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100)
        DISPLAY_SURF.blit(pressKeySurf, pressKeyRect)

        # Once a key is pressed, stop displaying text
        while checkForKeyPress() == None:
            pygame.display.update()
            FPS_CLOCK.tick



def showInstructions():
    DISPLAY_SURF.fill(BG_COLOR)
    textSurf, textRect = makeTextObjs("Instrutions", BIG_FONT, TEXT_SHADOW_COLOR)
    textRect.center = ((100+(100/2)), (100+(100/2)))
    DISPLAY_SURF.blit(textSurf, textRect)
    
    
# Creates text objects
def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

# Checks if a key is pressed
def checkForKeyPress():
    checkForQuit()
    # Get all KEYDOWNs and KEYUPs events
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        # Ignore KEYDOWN
        if event.type == KEYDOWN:
            continue
        # Return KEYUP event
        return event.key
    return None


# Checks if the user wants to quit and terminates the game
def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        # If ESC key was pressed
        if event.key == K_ESCAPE:
            terminate()
        # Else if KEYUP was not for ESC key, put back in event queue
        pygame.event.post(event)


# Terminates the game
def terminate():
    pygame.quit()
    sys.exit()

def start():
     while True:
        pygame.mixer.music.load("tetris.mid")
        # Loop music indefinitely (-1)
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen("Game Over!")
         
def instructions():
        cont = True
        DISPLAY_SURF.fill(BG_COLOR)
        textSurf, textRect = makeTextObjs("Instrutions", BIG_FONT, TEXT_SHADOW_COLOR)
        textRect.center = ((300), (100+(100/2)))
        DISPLAY_SURF.blit(textSurf, textRect)
        pygame.display.update()

        while cont:
            for event in pygame.event.get():
                button("back",275,425,100,30,BLUE,L_BLUE,back)
                pygame.display.update()

def back():
    mainMenu()

def highScore():
    cont = True
    DISPLAY_SURF.fill(BG_COLOR)
    textSurf, textRect = makeTextObjs("HighScores", BIG_FONT, TEXT_SHADOW_COLOR)
    textRect.center = ((300), (50+(100/2)))
    DISPLAY_SURF.blit(textSurf, textRect)
    
    #Get HighScores()
    hScores = HS.readFromCSV();
    h = 200
    for x in range(len(hScores)):
        text = hScores[x][0] + "  ....  " + str(hScores[x][1])
        textSurf, textRect = makeTextObjs(text, BASIC_FONT, TEXT_SHADOW_COLOR)
        textRect.center = ((300), (h))
        h += 25
        DISPLAY_SURF.blit(textSurf, textRect)
    
    pygame.display.update()
    while cont:
        for event in pygame.event.get():
            button("back",275,425,100,30,BLUE,L_BLUE,back)
            pygame.display.update()
            
def mainMenu():
    # Displays title
    DISPLAY_SURF.fill(BG_COLOR)
    showTextScreen("Tetris")
    clock = pygame.time.Clock()
    loop = True

    while loop:
        for event in pygame.event.get():
            button("Start",100,375,100,30,GREEN,L_GREEN,start)
            button("Instructions",275,375,100,30,BLUE,L_BLUE,instructions)
            button("High Score",450,375,100,30,RED, L_RED,highScore)
            pygame.display.update()
            clock.tick(15)
            
# main method
def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT, BIG_FONT
    pygame.init()
    # Create a clock object to track time
    FPS_CLOCK = pygame.time.Clock()
    # Initializes a window with given size 
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Creates a new Font Object from a file
    BASIC_FONT = pygame.font.Font("freesansbold.ttf", 18)
    BIG_FONT = pygame.font.Font("freesansbold.ttf", 100)
    # Sets the window title/name as "Tetris!"
    pygame.display.set_caption("Tetris!")

    mainMenu()


if __name__ == "__main__":
    main()
