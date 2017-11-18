import sys, pygame, random, time
from pygame.locals import *

# Window setup
FPS = 25
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOX_SIZE = 20
GAME_WIDTH = 10
GAME_HEIGHT = 20

# Margins between the game and window edge
X_MARGIN = int((WINDOW_WIDTH - GAME_WIDTH * BOX_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (GAME_HEIGHT * BOX_SIZE)

# Piece moves one space every 0.15s when the left/right arrow key is held
SIDEWAYS_MOVE_FREQ = 0.15
# Piece moves one space every 0.1s when the down arrow key is held
DOWN_MOVE_FREQ = 0.1

# Color setup (RGB)
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
L_RED = (175, 20, 20)
GREEN = (0, 155, 0)  # should be light green
L_GREEN = (20, 175, 20)
BLUE = (0, 0, 155)
L_BLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
L_YELLOW = (175, 175, 20)
# light blue (cyan)
# orange
# purple

COLORS = (BLUE, GREEN, RED, YELLOW)
L_COLORS = (L_BLUE, L_GREEN, L_RED, L_YELLOW)
assert len(COLORS) == len(L_COLORS)

# Assigning colors to the game
BORDER_COLOR = BLUE
BG_COLOR = BLACK
TEXT_COLOR = WHITE
TEXT_SHADOW_COLOR = GRAY

# Piece setup ("x" is a box and "." is an empty space )
# Each template contains the normal and rotated positions
# These templates are stored into a dictionary
TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5
BLANK = "."

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
    game = getBlankGame()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calcLevel( score )

    curPiece = getPiece()
    nextPiece = getPiece()

    # Game loop
    while True:
        # Checks if there is no falling piece and starts a new piece at the top if there isn't
        if curPiece == None:
            curPiece = nextPiece
            nextPiece = getPiece()
            lastFallTime = time.time()  # Reset last fall time

            # Checks if unable to fit the current piece on the board (game over if unable)
            if not isValidPosition(game, curPiece):
                return

        checkForQuit()

        for event in pygame.event.get():
            if event.type == KEYUP:
                # Pause the game
                if (event.key == K_p):
                    DISPLAY_SURF.fill(BG_COLOR)
                    pygame.mixer.music.stop()
                    showTextScreen("Paused")
                    pygame.mixer.music.play(-1, 0, 0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif event.key == K_LEFT:
                    movingLeft = False
                elif event.key == K_RIGHT:
                    movingRight = False
                elif event.key == K_DOWN:
                    movingDown = False

        # Draws the current game status
        DISPLAY_SURF.fill(BG_COLOR)
        drawGame(game)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if curPiece != None:
            drawPiece(curPiece)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


# Determines the level the player is on and how many seconds should pass until a falling piece
# falls into a space
def calcLevel( score ):
    level = int( score / 10 ) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq


# Returns a random new piece
def getPiece():
    shape = random.choice(list(PIECES.keys()))
    newPiece = {"shape": shape,
                "rotation": random.randint(0, len(PIECES[shape]) - 1),
                "x": int(GAME_WIDTH / 2) - int(TEMPLATE_WIDTH / 2),
                "y": -2,
                "color": random.randint(0, len(COLORS) - 1)}  # need to assign colors somehow
    return newPiece


# Returns true if the piece is within the board and there are no collisions
def isValidPosition(game, piece, adjX=0, adjY=0):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            isAboveBoard = y + piece["y"] + adjY < 0
            if isAboveBoard or PIECES[piece["shape"]][piece["rotation"]][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece["x"] + adjX, y + piece["y"] + adjY):
                return False
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
                     (X_MARGIN - 3, TOP_MARGIN - 7, (GAME_WIDTH * BOX_SIZE) + 8, (GAME_HEIGHT * BOX_SIZE) * 8), 5)

    # Fills the board's background
    pygame.draw.rect(DISPLAY_SURF, BG_COLOR, (X_MARGIN, TOP_MARGIN, BOX_SIZE * GAME_WIDTH, BOX_SIZE * GAME_HEIGHT))

    # Draws the boxes on the board
    for x in range( GAME_WIDTH ):
        for y in range( GAME_HEIGHT ):
            drawBox( x, y, game[x][y] )


# Draws the specified piece
def drawPiece( piece, pixelX=None, pixelY=None ):
    shape = PIECES[piece["shape"]][piece["rotation"]]
    if pixelX == None and pixelY == None:
        pixelX, pixelY = convertToPixel( piece["x"], piece["y"] )
    for x in range( TEMPLATE_WIDTH ):
        for y in range( TEMPLATE_HEIGHT ):
            if shape[y][x] != BLANK:
                drawBox( None, None, piece["color"], pixelX + (x * BOX_SIZE), pixelY + (y * BOX_SIZE) )


# Draws the next piece
def drawNextPiece( piece, pixelX=None, pixelY=None ):
    nextSurf = BASIC_FONT.render('Next:', True, TEXT_COLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOW_WIDTH - 120, 80)
    DISPLAY_SURF.blit(nextSurf, nextRect)
    drawPiece(piece, pixelX=WINDOW_WIDTH - 120, pixelY=100)


# Draws a single box
def drawBox( x, y, color, pixelX=None, pixelY=None ):
    if color == BLANK:
        return
    if pixelX == None and pixelY == None:
        pixelX, pixelY = convertToPixel( x, y )
    pygame.draw.rect( DISPLAY_SURF, COLORS[color], (pixelX + 1, pixelY + 1, BOX_SIZE - 1, BOX_SIZE - 1 ) )
    pygame.draw.rect( DISPLAY_SURF, L_COLORS[color], (pixelX + 1, pixelY + 1, BOX_SIZE - 4, BOX_SIZE - 4 ) )


# Draws the current score and level
def drawStatus( score, level ):
    # Draws score
    scoreSurf = BASIC_FONT.render( "Score: %s" % score, True, TEXT_COLOR )
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOW_WIDTH - 150, 20)
    DISPLAY_SURF.blit( scoreSurf, scoreRect )

    # Draws level
    levelSurf = BASIC_FONT.render('Level: %s' % level, True, TEXT_COLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOW_WIDTH - 150, 50)
    DISPLAY_SURF.blit(levelSurf, levelRect)


# Converts the given xy coordinates of the board to pixel coordinates on the screen
def convertToPixel( x, y ):
    return( X_MARGIN + ( x * BOX_SIZE ) ), ( TOP_MARGIN + ( y * BOX_SIZE ) )


# Displays the text screen (generic text screen function)
def showTextScreen(text):
    # Displays large text (with shadow) until a key is pressed
    titleSurf, titleRect = makeTextObjs(text, BIG_FONT, TEXT_SHADOW_COLOR)
    titleRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    DISPLAY_SURF.blit(titleSurf, titleRect)

    # Draws the text
    titleSurf, titleRect = makeTextObjs(text, BIG_FONT, TEXT_COLOR)
    titleRect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3)
    DISPLAY_SURF.blit(titleSurf, titleRect)

    # Draws the "Press a key to play." text
    pressKeySurf, pressKeyRect = makeTextObjs("Press a key to play.", BASIC_FONT, TEXT_COLOR)
    pressKeyRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100)
    DISPLAY_SURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPS_CLOCK.tick


# Creates text objects
def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


# Checks if a key is pressed
def checkForKeyPress():
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


# Checks if the user wants to quit and terminates the game
def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


# Terminates the game
def terminate():
    pygame.quit()
    sys.exit()


# main method
def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT, BIG_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font("freesansbold.ttf", 18)
    BIG_FONT = pygame.font.Font("freesansbold.ttf", 100)
    pygame.display.set_caption("Tetris!")

    showTextScreen("Tetris!")
    while True:
        # Plays background game music
        pygame.mixer.music.load("tetris.mid")
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen("Game Over")


if __name__ == "__main__":
    main()
