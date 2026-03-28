# stores the grid
# getters/setters

class Board:
    # constants:
    EMPTY = 1 # no plane, no hits
    PLANE = 2 # has plane, no hits
    HIT = -2 # has plane, has hits
    MISS = -1 # no plane, but has hits
    def __init__(self):
        '''
        create the 11x11 board with 1 all over the place
        header row: 0 1 2 3 ... 10
        header column: ' ', 'A', 'B', ... 'J'
        '''

        self._board = [[Board.EMPTY for _ in range(11)] for _ in range(11)]
        for col in range(11):
            self._board[0][col] = col

        self._board[0][0] = ' '
        for row in range(1, 11):
            self._board[row][0] = chr(ord('A') + row-1)

    def get(self, row, col):
        return self._board[row][col]

    def set_plane(self, row, col):
        self._board[row][col] = Board.PLANE

    def set_hit(self, row, col):
        self._board[row][col] = Board.HIT

    def set_miss(self, row, col):
        self._board[row][col] = Board.MISS

    def in_bounds(self, row, col):
        '''

        :param row:
        :param col:
        :return: True if plane is in bounds, False otherwise
        '''
        return 1 <= row <= 10 and 1 <= col <= 10

