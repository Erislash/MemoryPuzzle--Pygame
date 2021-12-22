# Memory Puzzle
# By Erislash
# Released under a "Simplified BSD" license

import random, sys, collections, pygame
from pygame.locals import *                     # Pygame constants
from utils.colors import *



# ==================== Utils ====================

Size: tuple = collections.namedtuple('Size', 'width height')
Position: tuple = collections.namedtuple('Position', 'x y')
Icon: tuple = collections.namedtuple('Icon', 'shape color')

shapes: dict = {
    'DONUT' : 'donut',
    'SQUARE' : 'square',
    'DIAMOND' : 'diamond',
    'LINES' : 'lines',
    'OVAL' : 'oval'
}

COLORS: tuple = (RED, GREEN, BLUE, YELLOW, LIME, PURPLE, TEAL)

SHAPES: tuple = (shapes['DONUT'], shapes['SQUARE'], shapes['DIAMOND'], shapes['LINES'], shapes['OVAL'])

# ==================== Game's constants Setup ====================

FPS: int = 30
WINDOW_SIZE: Size = Size(640, 480)
REVEAL_SPEED: int = 8
BOX_SIZE: int = 40
GAP_SIZE: int = 10
COLUMNS: int = 10
ROWS: int = 7
X_MARGIN: int = int((WINDOW_SIZE.width - (COLUMNS * ( BOX_SIZE + GAP_SIZE ))) / 2)
Y_MARGIN: int = int((WINDOW_SIZE.height - (ROWS * ( BOX_SIZE + GAP_SIZE ))) / 2)


assert ((COLUMNS * ROWS) % 2 == 0), f'The board MUST have a pair number of boxes for pair matches.\n{COLUMNS} cols x {ROWS} rows = {COLUMNS * ROWS} boxes'

assert len(COLORS) * len(SHAPES) * 2 >= COLUMNS * ROWS, "Board is too big for the number of shapes/colors defined."


BG_COLOR: tuple = NAVYBLUE
LIGHT_BG_COLOR: tuple = GRAY
BOX_COLOR: tuple = WHITE
HIGHLIGHT_COLOR: tuple = BLUE

FPSCLOCK = pygame.time.Clock()
DISPLAYSURFACE = pygame.display.set_mode(WINDOW_SIZE)

# ==================== Main game function ====================

def main() -> None:
    # ==================== Game Setup ====================

    pygame.init()
    pygame.display.set_caption('Memory Game')

    
    mousePosition = Position(0, 0)

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection: tuple = None

    DISPLAYSURFACE.fill(BG_COLOR)
    # startGameAnimation(mainBoard)



    # ==================== Main Game Loop ====================
    while True:
        DISPLAYSURFACE.fill(BG_COLOR)
        drawBoard(mainBoard, revealedBoxes)

        events = pygame.event.get()
        for event in events: # event handling loop

            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                
                pygame.quit()
                sys.exit()


        pygame.display.update()
        FPSCLOCK.tick(30)



def getIconsList () -> list[Icon]:

    # Get all shape/color combinations
    icons: list[Icon] = [Icon(shape, color) for shape in SHAPES for color in COLORS]

    # We need n DIFFERENT icons, where n is the half of the number of boxes (columns * rows)
    iconsNeeded: int = int(COLUMNS * ROWS / 2)
    
    random.shuffle(icons)                           # Shuffle all the icons in the list
    icons = icons[: iconsNeeded] * 2                # Take all the icons needed and then duplicate them
    
    random.shuffle(icons)                           # Shuffle the result

    return icons



def getRandomizedBoard () -> list[list]:

    icons = getIconsList()

    board: list[list] = []

    for x in range(COLUMNS):
        column: list = []
        for y in range(ROWS):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    
    return board



def generateRevealedBoxesData ( val ) -> list[list]:
    
    revealedBoxes: list = []

    for i in range(COLUMNS):
        revealedBoxes.append([val] * ROWS)
    
    return revealedBoxes



def splitIntoGroupsOf(groupSize, list):
    
    output = []
    listLength = len(list)

    for i in range(0, listLength, groupSize):
        output.append(list[i : i + groupSize])

    return output



def leftTopCoordsOfBox ( placeX: int, placeY: int ) -> Position:
    
    xPos = X_MARGIN + (placeX * (BOX_SIZE + GAP_SIZE))
    yPos = Y_MARGIN + (placeY * (BOX_SIZE + GAP_SIZE))

    return Position(xPos, yPos)



def geticon (board, placeX, placeY) -> Icon:
    
    return Icon(board[placeX][placeY].shape, board[placeX][placeY].color)



def drawIcon (icon: Icon, coords: Position):
    QUARTER = int( BOX_SIZE * ( 1/4 ) )
    HALF = int( BOX_SIZE * ( 1/2 ) )

    shape, color = Icon
    xPos, yPos = coords

    if shape == shapes[ 'DONUT' ]:
        pygame.draw.circle( DISPLAYSURFACE, color, ( xPos + HALF, yPos + HALF ), HALF - 5 )
        pygame.draw.circle( DISPLAYSURFACE, BG_COLOR, ( xPos + HALF, yPos + HALF ), QUARTER - 5 )
    
    elif shape == shapes[ 'SQUARE' ]:
        pygame.draw.rect( DISPLAYSURFACE, color, 
        ( xPos + QUARTER, yPos + QUARTER, BOX_SIZE - HALF, BOX_SIZE - HALF ) )

    elif shape == shapes[ 'DIAMOND' ]:
        pygame.draw.polygon( DISPLAYSURFACE, color, ( 
        Position(xPos + HALF, yPos),
        Position(xPos + BOX_SIZE, yPos + HALF),
        Position(xPos + HALF, yPos + BOX_SIZE),
        Position(xPos, yPos + HALF)
        ))
    
    elif shape == shapes[ 'LINES' ]:
        for i in range( 0, BOX_SIZE, 5 ):
            pygame.draw.line( DISPLAYSURFACE, color, ( xPos, yPos + i ), ( xPos + i, yPos ) )

    elif shape == shapes[ 'OVAL' ]:
        pygame.draw.ellipse( DISPLAYSURFACE, color, ( xPos, yPos + QUARTER, BOX_SIZE, HALF ) )



def drawBoard (board, revealedBoard):

    for boardX in range( COLUMNS ):
        
        for boardY in range( ROWS ):
            
            boxPixelPosition: Position = leftTopCoordsOfBox(boardX, boardY)

            if not revealedBoard[ boardX ][ boardY ]:
                
                pygame.draw.rect(DISPLAYSURFACE, BOX_COLOR, (boxPixelPosition.x, boxPixelPosition.y, BOX_SIZE, BOX_SIZE))
            
            else:

                icon: Icon = geticon( board, boardX, boardY )

                drawIcon(Icon, boxPixelPosition)



def startGameAnimation ( board ):
    
    coveredBoxes = generateRevealedBoxesData( False )
    boxes = []

    for x in range( COLUMNS ):
        for y in range( ROWS ):
            boxes.append( (x, y) )

    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    


if __name__ == '__main__':
    main()
