"""
This is our main driver file, which will be responsible for handling user input and displaying the current GameState object
"""



import pygame as p
import pygame.display

import ChessEngine



WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


"""
Initialize a global dictionary of images. This will be called exactly once in the main.
"""


def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wp', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))



def main():
    p.init()

    screen = p.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess with Heus')
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user
    playerClicks = [] #keep track of player clicks (two tuples)

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #move handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #after the second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #reset user clicks
                    playerClicks = []

            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()   
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)



def drawBoard(screen):
    colors = [p.Color("light gray"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board. The top left square is always light.
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "__":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()