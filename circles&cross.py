from tkinter import *
#TODO change import method, to from tkinter import module

# Constants
CANVAS_SIZE = 600
FIGURE_SIZE = 200
RATIO = CANVAS_SIZE // FIGURE_SIZE
BG_COLOR = 'white'
EMPTY = None

# Players setup
X = 'player 1'
O = 'player 2'
FIRST_PLAYER = X

# Classes
class Board(Tk):
    def __init__(self, startPlayer):
        super().__init__()
        self.canvas = Canvas(height=CANVAS_SIZE, width=CANVAS_SIZE, bg=BG_COLOR)
        self.canvas.pack()
        self.figureSize = FIGURE_SIZE
        self.currentPlayer = startPlayer
        self.canvas.bind('<Button-1>', self.clickEvent)
        self.gameStatus = True
        
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
            ]
    
    def buildGrid(self,gridColor):
        x = FIGURE_SIZE
        y1 = 0
        y2 = CANVAS_SIZE
        for _ in range(2):
            self.canvas.create_line(x, y1, x, y2, fill=gridColor)
            self.canvas.create_line(y1, x, y2, x, fill=gridColor)
            x+=FIGURE_SIZE
    
    def renderCross(self,posX,posY):
        fSize = self.figureSize - 5
        posX2 = posX + fSize
        posY2 = posY + fSize
        self.canvas.create_line(posX+5, posY+5, posX2, posY2, fill='red', width=5)
        self.canvas.create_line(posX2, posY+5, posX+5, posY2, fill='red',width=5)
    
    def renderCircle(self,posX,posY):
        fSize = self.figureSize - 5
        self.canvas.create_oval(posX+5, posY+5, posX+fSize, posY+fSize, outline='blue', width=5)
        
    def renderLine(self, posX, posY, posX2, posY2):
        self.canvas.create_line(posX+5, posY+5, posX2, posY2, fill='black', width=7.5)    
    
    def clickEvent(self,e):
        coordX = e.x //FIGURE_SIZE
        coordY = e.y //FIGURE_SIZE
        if e.x >= CANVAS_SIZE:
            coordX = 2
        if e.y >= CANVAS_SIZE:
            coordY = 2    
        self.makeMove(coordX, coordY)
        
        if self.gameStatus:
            self.aiBestMove()
        print(coordX,coordY)
        
    def makeMove(self,x,y):
        pos = {0:0,1:200,2:400}
        currentPlayer = self.currentPlayer

        if self.board[x][y] == EMPTY:
            self.changePlayer()
            
            if currentPlayer == X:
                self.renderCross(pos[x], pos[y])
            elif currentPlayer == O:
                self.renderCircle(pos[x], pos[y])
            
            self.updateBoard(x,y)
            
    def updateBoard(self,x,y):
        cp = self.currentPlayer
        self.board[x][y] = cp
        if self.checkWin(self.board,cp):
            self.winner(cp)
        elif self.checkDraw(self.board):
            self.winner()
    
    def checkWin(self, b, p):
        for y in range(RATIO):
            if b[y] == [p]*RATIO:
                return True
        for x in range(RATIO):
            if b[0][x] == b[1][x] == b[2][x] == p:
                return True
        
        if b[0][0] == b[1][1] == b[2][2] == p:
            return True
        
        if b[0][2] == b[1][1] == b[2][0] == p:
            return True
        
        return False
    
    def checkDraw(self, b):
        for row in b:
            if EMPTY in row:
                return False
        return True
    
    def changePlayer(self):
        if self.currentPlayer == X:
            self.currentPlayer = O
        else:
            self.currentPlayer = X  
            
    def crossLine(self, p):
        coords = []
        for m in range(len(self.board)):
            for i in range(len(self.board[m])):
                if self.board[m][i] == p:
                    coords.append([m,i])
        print(coords)
        self.getCoords(coords)   
        
    def getCoords(self, c):
        half = FIGURE_SIZE//2
        posX = (c[0][1] + 1) * FIGURE_SIZE - half
        posY = (c[0][0] + 1) * FIGURE_SIZE - half
        posX2 = (c[-1][1] + 1) * FIGURE_SIZE - half
        posY2 = (c[-1][0] + 1) * FIGURE_SIZE - half
        self.renderLine(posY-5, posX-5, posY2, posX2)          
        
    def winner(self, player=None):
        center = CANVAS_SIZE // 2
        if player:
            text = f'Winner is {player}!!!'
            self.crossLine(player)
        else:
            text = 'Draw!'
        self.canvas.create_text(center, center, text=text, fill='black', font='Arial 50')
        self.canvas.unbind('<Button-1>')
        
    def minimax(self, board, isMax):
        boardLen = range(len(self.board))
        
        if self.checkWin(board, O):
            return 1
        elif self. checkWin(board, X):
            return -1
        elif self.checkDraw(board):
            return 0
        
        if isMax:
            bestScore = float('-inf')
            for i in boardLen:
                for j in boardLen:
                    if board[i][j] == EMPTY:
                        board[i][j] = O
                        score = self.minimax(board, False)
                        board[i][j] = EMPTY
                        bestScore = max(score, bestScore)
        else:
            bestScore = float('inf')
            for i in boardLen:
                for j in boardLen:
                    if board[i][j] == EMPTY:
                        board[i][j] = X
                        score = self.minimax(board, True)
                        board[i][j] = EMPTY
                        bestScore = min(score, bestScore)
        return bestScore
    
    def aiBestMove(self):
        bestScore = float('-inf')
        boardLen = range(len(self.board))
        board = self.board[:]
        for i in boardLen:
            for j in boardLen:
                if board[i][j] == EMPTY:
                    board[i][j] = O
                    score = self.minimax(board, False)
                    board[i][j] = EMPTY
                    if score > bestScore:
                        bestScore = score
                        move = j, i
        print(move)
        self.makeMove(move[0],move[1])
        

    
# Initialize game object and execute requre methods
gameV1 = Board(startPlayer=FIRST_PLAYER)
gameV1.buildGrid('black')
# gameV1.renderCross(0,0)
# gameV1.renderCircle(200,200)


# Run the game
gameV1.mainloop()