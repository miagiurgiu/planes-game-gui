# store the human board
# store the computer board
# store plane lists
from domain.board import Board


class BoardRepository():
    def __init__(self):
        self.user_board = Board()
        self.computer_board = Board()
        self.user_planes = []
        self.computer_planes = []
        self.computer_targets = []
        self.user_hits = set()
        self.user_misses = set()
        self.computer_hits = set()
        self.computer_misses = set()

    def add_user_plane(self, plane_cells):
        '''

        :param plane_cells: list of coordinates (tuples) forming a plane represented as (row, col) -> ex: (1,1) for A1
        :return: the updated user_planes list containing the new plane given by the plane_cells list
        '''
        self.user_planes.append(plane_cells)
        for r,c in plane_cells:
            self.user_board.set_plane(r, c)

    def add_computer_plane(self, plane_cells):
        '''

        :param plane_cells: list of coordinates (tuples) forming a plane represented as (row, col) -> ex: (1,1) for A1
        :return: the updated computer_planes list containing the new plane given by the plane_cells list
        '''
        self.computer_planes.append(plane_cells)
        for r,c in plane_cells:
            self.computer_board.set_plane(r, c)

    def record_user_hit(self, cell):
        '''

        :param cell: cell entered by the user hits a computer plane -> ex: (1,3) for A3
        :return: the updated user_hits list containing the new hit cell
                 the computer_board marked with the new hit cell (X)
        '''
        r,c = cell
        self.user_hits.add(cell)
        self.computer_board.set_hit(r,c)

    def record_user_miss(self, cell):
        '''

        :param cell: cell entered by the user misses a computer plane -> ex: (1,3) for A3
        :return: the updated user_misses list containing the new missed cell
                 the computer_board marked with the new missed cell (O)
        '''
        r,c = cell
        self.user_misses.add(cell)
        self.computer_board.set_miss(r,c)

    def record_computer_hit(self, cell):
        '''

        :param cell: cell given by the computer hits a user plane -> ex: (1,3) for A3
        :return: the updated computer_hits list containing the new hit cell
                 the computer_board marked with the new hit cell (X)
        '''
        r,c = cell
        self.computer_hits.add(cell)
        self.user_board.set_hit(r,c)

    def record_computer_miss(self, cell):
        '''

        :param cell: cell given by the computer misses a user plane -> ex: (1,3) for A3
        :return: the updated computer_misses list containing the new missed cell
                 the computer_board marked with the new missed cell (O)
        '''
        r,c = cell
        self.computer_misses.add(cell)
        self.user_board.set_miss(r,c)

    def all_user_heads_destroyed(self):
        '''

        :return: True if all 3 heads from the user planes are destroyed, False otherwise
        '''
        for plane in self.user_planes:
            head = plane[0]
            if head not in self.computer_hits:
                return False
        return True

    def all_computer_heads_destroyed(self):
        '''

        :return: True if all 3 heads from the computer planes are destroyed, False otherwise
        '''
        for plane in self.computer_planes:
            head = plane[0]
            if head not in self.user_hits:
                return False
        return True

    def get_user_board(self):
        return self.user_board

    def computer_plane_overlaps(self, plane_cells):
        '''

        :param plane_cells: the new plane
        :return:
        Checks whether the new plane overlaps with any cell of the planes already placed
            - compresses all the cells occupied by the computer in a set
            - checks if any cell in the new plane (plane_cells) already exists in that set
            - if yes -> overlap -> True
            - if not -> False
        self.computer_planes = [ [(1,1),(2,1),...], [(5,5),(5,6),...],...] = list of planes
        every plane = list of cells (tuples)
        '''
        occupied = set()
        for plane in self.computer_planes:
            for cell in plane:
                occupied.add(cell)
        for cell in plane_cells:
            if cell in occupied:
                return True
        return False

    def user_plane_overlaps(self, plane_cells):
        '''

        :param plane_cells: the new plane
        :return: True if the new plane overlaps with any cell of the planes already placed, False otherwise
        '''
        occupied = set()
        for plane in self.user_planes:
            for cell in plane:
                occupied.add(cell)
        for cell in plane_cells:
            if cell in occupied:
                return True
        return False

    def user_in_bounds(self, row, col):
        return self.user_board.in_bounds(row, col)

    def computer_in_bounds(self, row, col):
        return self.computer_board.in_bounds(row, col)