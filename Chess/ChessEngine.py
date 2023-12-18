"""
This class is responsible for storing all the information about the current state of a chess game.
It will also be responsible for the current state. It will also keep a move log.
"""


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R' : self.getRookMoves, 'N': self.getKnightMoves, 'B' : self.getBishopMoves, 
                              'Q' : self.getQueenMoves, 'K' : self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "__"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCapture
            self.whiteToMove = not self.whiteToMove #switch turn back
    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in given rows
                turn = self.board[r][c][0]
                
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1];
                    self.moveFunctions[piece](r, c, moves) #call the approriate  based on piece types
        return moves
    

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # pawn to move
            if self.board[r - 1][c] == "__":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "__":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0: #captures to the left
                if self.board[r - 1][c - 1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7: #captures to the right
                if self.board[r - 1][c + 1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))  
        elif not self.whiteToMove:
            if self.board[r + 1][c] == "__": 
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "__":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:
            for i in range(r - 1,  -1, -1): #Rook moves upward
                if self.board[i][c] == "__":
                    moves.append(Move((r, c), (i, c), self.board))
                elif self.board[i][c][0] == 'b':  
                    moves.append(Move((r, c), (i, c), self.board))
                    break
                else:
                    continue
            for i in range(r + 1, 8, +1): #Rook moves downward
                if self.board[i][c] == "__":
                    moves.append(Move((r, c), (i, c), self.board))
                elif self.board[i][c][0] == 'b':  
                    moves.append(Move((r, c), (i, c), self.board))
                    break
                else:
                    continue
            for i in range(c - 1, -1, -1): #Rook moves to the left
                if self.board[r][i] == "__":
                    moves.append(Move((r, c), (r, i), self.board))
                elif self.board[r][i][0] == 'b':  
                    moves.append(Move((r, c), (r, i), self.board))
                    break
                else:
                    continue
            for i in range(c + 1, 8, + 1): #Rook moves to the right
                if self.board[r][i] == "__":
                    moves.append(Move((r, c), (r, i), self.board))
                elif self.board[r][i][0] == 'b':  
                    moves.append(Move((r, c), (r, i), self.board))
                    break
                else:
                    continue
        elif not self.whiteToMove:
            for i in range(r + 1,  8): #Rook moves upward
                if self.board[i][c] == "__":
                    moves.append(Move((r, c), (i, c), self.board))
                elif self.board[i][c][0] == 'w':  
                    moves.append(Move((r, c), (i, c), self.board))
                    break
                else:
                    continue
            for i in range(r - 1, -1, -1): #Rook moves downward
                if self.board[i][c] == "__":
                    moves.append(Move((r, c), (i, c), self.board))
                elif self.board[i][c][0] == 'w':  
                    moves.append(Move((r, c), (i, c), self.board))
                    break
                else:
                    continue
            for i in range(c + 1, 8, + 1): #Rook moves to the left
                if self.board[r][i] == "__":
                    moves.append(Move((r, c), (r, i), self.board))
                elif self.board[r][i][0] == 'b':  
                    moves.append(Move((r, c), (r, i), self.board))
                    break
                else:
                    continue
            for i in range(c - 1, -1, -1): #Rook moves to the right
                if self.board[r][i] == "__":
                    moves.append(Move((r, c), (r, i), self.board))
                elif self.board[r][i][0] == 'b':  
                    moves.append(Move((r, c), (r, i), self.board))
                    break
                else:
                    continue

    def getKnightMoves(self, r, c, moves):
        directions = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
    
            if 0 <= new_r < 8 and 0 <= new_c < 8:
                if self.whiteToMove and self.board[new_r][new_c][0] != self.board[r][c][0]:
                    moves.append(Move((r, c), (new_r, new_c), self.board))
    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
            # Bishop moves upward and to the left
            for i, j in zip(range(r - 1, -1, -1), range(c - 1, -1, -1)):
                if self.board[i][j] == "__":
                    moves.append(Move((r, c), (i, j), self.board))
                elif self.board[i][j][0] == 'b':
                    moves.append(Move((r, c), (i, j), self.board))
                    break
                else: 
                    continue

            # Bishop moves downward and to the right
            for i, j in zip(range(r + 1, 8), range(c + 1, 8)):
                if self.board[i][j] == "__":
                    moves.append(Move((r, c), (i, j), self.board))
                elif self.board[i][j][0] == 'b':
                    moves.append(Move((r, c), (i, j), self.board))
                    break
                else:
                    continue

            # Bishop moves upward and to the right
            for i, j in zip(range(r - 1, -1, -1), range(c + 1, 8)):
                if self.board[i][j] == "__":
                    moves.append(Move((r, c), (i, j), self.board))
                elif self.board[i][j][0] == 'b':
                    moves.append(Move((r, c), (i, j), self.board))
                    break
                else:
                    continue

            # Bishop moves downward and to the left
            for i, j in zip(range(r + 1, 8), range(c - 1, -1, -1)):
                if self.board[i][j] == "__":
                    moves.append(Move((r, c), (i, j), self.board))
                elif self.board[i][j][0] == 'b':
                    moves.append(Move((r, c), (i, j), self.board))
                    break
                else:
                    continue
        elif not self.whiteToMove:
            # Bishop moves downward and to the left
            for i, j in zip(range(r - 1, -1, -1), range(c - 1, -1, -1)):
                if self.board[i][j] == "__":
                    moves.append(Move((r, c), (i, j), self.board))
                elif self.board[i][j][0] == 'b':
                    moves.append(Move((r, c), (i, j), self.board))
                    break
                else:
                    break

            # Bishop moves upward and to the right
            for i, j in zip(range(r + 1, 8), range(c + 1, 8)):
                if self.board[i][j] == "__":
                    moves.append(Move((r, c), (i, j), self.board))
                elif self.board[i][j][0] == 'b':
                    moves.append(Move((r, c), (i, j), self.board))
                    break
                else:
                    break

            # Bishop moves downward and to the right
            for i, j in zip(range(r - 1, -1, -1), range(c + 1, 8)):
                if self.board[i][j] == "__":
                    moves.append(Move((r, c), (i, j), self.board))
                elif self.board[i][j][0] == 'b':
                    moves.append(Move((r, c), (i, j), self.board))
                    break
                else:
                    break

            # Bishop moves upward and to the left
            for i, j in zip(range(r + 1, 8), range(c - 1, -1, -1)):
                if self.board[i][j] == "__":
                    moves.append(Move((r, c), (i, j), self.board))
                elif self.board[i][j][0] == 'b':
                    moves.append(Move((r, c), (i, j), self.board))
                    break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    def getKingMoves(self, r, c, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
    
            if 0 <= new_r < 8 and 0 <= new_c < 8:
                if self.whiteToMove and self.board[new_r][new_c][0] != self.board[r][c][0]:
                    moves.append(Move((r, c), (new_r, new_c), self.board))
class Move():

    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4,
                   "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3,
                   "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapture = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol*100 + self.endRow*10 + self.endCol
        print(self.moveID)


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]




