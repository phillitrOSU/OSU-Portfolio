import itertools

class Tictactoe():
    """A class for representing a game of tic-tac-toe"""

    board = []
    columns = ["1","2","3","4","5","6","7","8","9"]
    rows = ["A","B","C","D","E","F","G","H","I"]
    spots = []
    win_length = 0
    size = 0
    marker = None
    opponentMarker = None
    player = None

    def __init__(self, marker, size, win_length):

        self.board = [["-" for x in range(size)] for x in range(size)]
        self.columns = self.columns[:size]
        self.rows = self.rows[:size]
        self.marker = marker

        if self.marker == "o":
            self.opponentMarker = "x"
        else:
            self.opponentMarker = "o"

        self.size = size
        self.spots = ["".join(item) for item in list(itertools.product(self.rows, self.columns))]
        self.win_length = win_length


    def to_string(self):
        print("   ",end="")
        print("  ".join(self.columns))
        for i in range(len(self.board)):
            print(f"{self.rows[i]}",end="  ")
            for j in range(len(self.board[0])):
                spot = self.board[i][j]
                print(f"{spot}", end="  ")
            print()
        print()

    def printBoard(self):
        self.to_string()

    def placeMarker(self, coordinates):
        if coordinates in self.spots:
            row, column = self.rows.index(coordinates[0]), self.columns.index(coordinates[1])

            if self.board[row][column] == "-":
                self.board[row][column] = self.marker
                return True

        return False

    def placeOpponent(self, coordinates):
        if coordinates in self.spots:
            row, column = self.rows.index(coordinates[0]), self.columns.index(coordinates[1])

            if self.board[row][column] == "-":
                self.board[row][column] = self.opponentMarker
                return True

        return False

    # Check for winning win_lengths.
    def checkWin(self):
        win = False

        if self.checkRow() or self.checkColumn():
            win = True

        if self.checkDiagonalRight() or self.checkDiagonalLeft():
            win = True

        return win

    # Check column win_lengths.
    def checkColumn(self):
        win = True

        for row in range(self.size):
            for column in range(self.size):

                # If marker found, check for column win.
                if self.board[row][column] == self.marker:

                    for y in range(self.win_length):

                        try:
                            if self.board[row + y][column] != self.marker:
                                win = False

                        except: # out of range
                            win = False

                    if win == True:
                        return win

        return win

    # Check row win_lengths
    def checkRow(self):
        win = True

        for row in range(self.size):
            for column in range(self.size):

                # If marker found, check for row win.
                if self.board[row][column] == self.marker:

                    for y in range(self.win_length):

                        try:
                            if self.board[row][column + y] != self.marker:
                                win = False

                        except: # out of range
                            win = False

                    if win == True:
                        return win

        return win

    # Check Diagonal win_lengths
    def checkDiagonalRight(self):
        win = True

        for row in range(self.size):
            for column in range(self.size):

                # If marker found, check for diagonal right win.
                if self.board[row][column] == self.marker:

                    for y in range(self.win_length):

                        try:
                            if self.board[row + y][column + y] != self.marker:
                                win = False

                        except: # out of range
                            win = False

                    if win == True:
                        return win

        return win

    # Check diagonal win_lengths
    def checkDiagonalLeft(self):
        win = True

        for row in range(self.size):
            for column in range(self.size):

                # If marker found, check for diagonal left win.
                if self.board[row][column] == self.marker:

                    for y in range(self.win_length):

                        try:
                            if self.board[row + y][column - y] != self.marker:
                                win = False

                        except: # out of range
                            win = False

                    if win == True:
                        return win

        return win