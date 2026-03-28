# create computer board
# randomly place 3 computer planes (no overlap, in bounds)
# place human plane
# converts head + tail -> full plane list
# checks overlap
# checks bounds
# human move
# computer move
# check game over
import random
from domain.board import Board

class BoardService:
    def __init__(self, board_repo):
        self.board_repo = board_repo
        self.user_finished = False
        self._just_destroyed_head = False

    def _parse_coord(self, coord):
        '''

        :param coord: the coordinate received of the form A3
        :return: the row and the column corresponding to the coordinate
        Converts A3 -> (row = 1, col = 3)
        '''

        row = coord[0] # str
        col = int(coord[1:]) # int
        row = ord(row) - ord('A') + 1 # int
        return row, col

    def place_user_planes(self, head, tail):
        '''

        :param head: the head of the plane entered by the user A3
        :param tail: the tail of the plane entered by the user D3
        :return:
        Determines all the cells of the plane based on the head and the tail coordinates
        Adds those cells to the user board
        '''
        head_row, head_col = self._parse_coord(head) # head = (head_row, head_col)
        tail_row, tail_col = self._parse_coord(tail) # tail = (tail_row, tail_col)
        dr = abs(head_row - tail_row)
        dc = abs(head_col - tail_col)
        if not ((dr==3 and dc == 0 ) or (dr ==0 and dc == 3)):
            raise ValueError("Invalid plane position")
        # orientation
        if head_row < tail_row:
                orientation = "N"
        elif head_row > tail_row:
                orientation = "S"
        elif head_col > tail_col:
                orientation = "E"
        else:
                orientation = "W"
        # create cell list
        plane_cells = []
        plane_cells.append((head_row, head_col))

        if orientation == "N":
            plane_cells.append((head_row+1, head_col))
            plane_cells.append((head_row+1, head_col-1))
            plane_cells.append((head_row+1, head_col+1))

            plane_cells.append((head_row+2, head_col))

            plane_cells.append((head_row+3, head_col))
            plane_cells.append((head_row+3, head_col-1))
            plane_cells.append((head_row+3, head_col+1))

        elif orientation == "S":
            plane_cells.append((head_row-1, head_col))
            plane_cells.append((head_row-1, head_col-1))
            plane_cells.append((head_row-1, head_col+1))

            plane_cells.append((head_row-2, head_col))

            plane_cells.append((head_row-3, head_col))
            plane_cells.append((head_row-3, head_col-1))
            plane_cells.append((head_row-3, head_col+1))

        elif orientation == "W":
            plane_cells.append((head_row, head_col-1))
            plane_cells.append((head_row-1, head_col-1))
            plane_cells.append((head_row+1, head_col-1))

            plane_cells.append((head_row, head_col-2))

            plane_cells.append((head_row, head_col-3))
            plane_cells.append((head_row-1, head_col-3))
            plane_cells.append((head_row+1, head_col-3))

        elif orientation == "E":
            plane_cells.append((head_row, head_col+1))
            plane_cells.append((head_row-1, head_col+1))
            plane_cells.append((head_row+1, head_col+1))

            plane_cells.append((head_row, head_col+2))

            plane_cells.append((head_row, head_col+3))
            plane_cells.append((head_row+1, head_col+3))
            plane_cells.append((head_row-1, head_col+3))

        for r,c in plane_cells:
            if not self.board_repo.user_board.in_bounds(r, c):
                raise ValueError("Plane out of bounds")
        if self.board_repo.user_plane_overlaps(plane_cells):
            raise ValueError("Plane overlaps another plane")
        self.board_repo.add_user_plane(plane_cells)

    def place_computer_planes(self):
        '''

        :return:
        Chooses a random head coordinate and a random orientation and creates the corresponding plane
        '''
        orientations = ["N", "S", "E", "W"]
        while len(self.board_repo.computer_planes) < 3:
            head_row = random.randint(1, 10)
            head_col = random.randint(1, 10)
            orientation = random.choice(orientations)
            head = (head_row, head_col)
            body = []
            plane_cells = [] # (head + body)

            if orientation == "N":
                body.append((head_row + 1, head_col))
                body.append((head_row + 1, head_col - 1))
                body.append((head_row + 1, head_col + 1))

                body.append((head_row + 2, head_col))

                body.append((head_row + 3, head_col))
                body.append((head_row + 3, head_col - 1))
                body.append((head_row + 3, head_col + 1))

            elif orientation == "S":
                body.append((head_row - 1, head_col))
                body.append((head_row - 1, head_col - 1))
                body.append((head_row - 1, head_col + 1))

                body.append((head_row - 2, head_col))

                body.append((head_row - 3, head_col))
                body.append((head_row - 3, head_col - 1))
                body.append((head_row - 3, head_col + 1))

            elif orientation == "W":
                body.append((head_row, head_col - 1))
                body.append((head_row - 1, head_col - 1))
                body.append((head_row + 1, head_col - 1))

                body.append((head_row, head_col - 2))

                body.append((head_row, head_col - 3))
                body.append((head_row - 1, head_col - 3))
                body.append((head_row + 1, head_col - 3))

            elif orientation == "E":
                body.append((head_row, head_col + 1))
                body.append((head_row - 1, head_col + 1))
                body.append((head_row + 1, head_col + 1))

                body.append((head_row, head_col + 2))

                body.append((head_row, head_col + 3))
                body.append((head_row + 1, head_col + 3))
                body.append((head_row - 1, head_col + 3))

            plane_cells = [head] + body

            #
            ok = True # suppose we have placed the planes accordingly
            for r,c in plane_cells:
                if not self.board_repo.computer_board.in_bounds(r, c):
                    ok = False
                    break
            if not ok:
                continue # keep regenerating
            if self.board_repo.computer_plane_overlaps(plane_cells):
                continue # keep regenerating
            self.board_repo.add_computer_plane(plane_cells)

    def user_move(self, coord):
        '''

        :param coord: coordinate entered by the user
        :return: the state corresponding to the given coordinate: hit, miss or head destroyed
        '''
        r, c = self._parse_coord(coord)
        cell = (r, c)
        if cell in self.board_repo.user_hits or cell in self.board_repo.user_misses:
            raise ValueError("Already attacked")

        for plane in self.board_repo.computer_planes:
            if cell == plane[0]:
                self.board_repo.record_user_hit(cell)
                return "Head destroyed by you!"
            if cell in plane:
                self.board_repo.record_user_hit(cell)
                return "You hit!"
        self.board_repo.record_user_miss(cell)
        return "You miss!"

    def computer_move(self):
        '''
        AI explanation:
            - the program does not use a minimax algorithm
            - the game is a hidden-information game (Battleship-like)
            - decisions are based only on previous hits, misses, and neighbours

        Decision order:
            - if there are neighbouring target cells (computer_targets), one of them is attacked first
            - otherwise, if a plane head was NOT destroyed in the previous move, a head is guessed using _guess_head_from_hits()
            - otherwise, a random untried cell is selected

        Special rule:
            - after destroying a plane head:
                - the entire plane is marked as destroyed
                - neighbour targets are cleared
                - head guessing is disabled for exactly ONE move

        Move result:
            - head hit:
                - mark entire plane as hit
                - clear targets
                - set _just_destroyed_head = True
            - body hit:
                - mark hit
                - add orthogonal neighbours to computer_targets
            - miss:
                - mark miss
        '''

        cell = None
        # try neighbours from previous hits
        if self.board_repo.computer_targets:
            cell = self.board_repo.computer_targets.pop()

        # try to guess a head ONLY if we didn't just destroy one
        elif not self._just_destroyed_head:
            cell = self._guess_head_from_hits()

        if self._just_destroyed_head:
            self._just_destroyed_head = False

        if cell is None:
            # fallback random
            while True:
                r = random.randint(1, 10)
                c = random.randint(1, 10)
                cell = (r, c)
                if cell not in self.board_repo.computer_hits and cell not in self.board_repo.computer_misses:
                     break

        for plane in self.board_repo.user_planes:
            if cell == plane[0]:
                self.board_repo.record_computer_hit(cell)
                for pr,pc in plane:
                    if (pr,pc) not in self.board_repo.computer_hits:
                        self.board_repo.computer_hits.add((pr,pc))
                        self.board_repo.user_board.set_hit(pr,pc)

                self.board_repo.computer_targets.clear()
                self._just_destroyed_head = True
                return "Head destroyed by computer!"
            if cell in plane:
                self.board_repo.record_computer_hit(cell)
                self._add_neighbours(cell)
                return "Computer hits!"
        self.board_repo.record_computer_miss(cell)
        # print(self.board_repo.computer_targets)
        return "Computer misses!"

    def _guess_head_from_hits(self):
        '''
        Attempts to guess a plane head using previous computer hits.

        Pattern detection:
            - horizontal pattern: left and right neighbours are both hits (XXX)
            - vertical pattern: up and down neighbours are both hits (XXX)

        Candidate generation:
            - extend the hit line forward and backward (+/-2, +/-3 cells)
            - check perpendicular positions around the middle hit

        Validation:
            - cell must be in bounds
            - cell must not have been previously attacked

        Returns:
            - a valid candidate cell
            - None if no valid guess exists
        '''

        hits = list(self.board_repo.computer_hits)
        for (r,c) in hits:
            left = (r, c-1)
            right = (r, c+1)
            if left in hits and right in hits: # we have XXX horizontally
                candidates = [
                    (r, c-2),
                    (r, c+2),
                    (r-1,c),
                    (r+1,c),
                    (r-3,c),
                    (r+3,c)
                ]
                # cell = (r,c); kinda cell[0] = r, cell[1] = c
                for cell in candidates:
                    if self.board_repo.user_board.in_bounds(*cell) and cell not in self.board_repo.computer_hits and cell not in self.board_repo.computer_misses:
                        return cell
        for (r,c) in hits:
            up = (r-1, c)
            down = (r+1, c)
            if up in hits and down in hits:
                candidates = [
                    (r-2, c),
                    (r+2, c),
                    (r, c-1),
                    (r, c+1),
                    (r, c+3),
                    (r, c-3)
                ]
                for cell in candidates:
                    if self.board_repo.user_board.in_bounds(*cell) and cell not in self.board_repo.computer_hits and cell not in self.board_repo.computer_misses:
                        return cell
        return None

    def _add_neighbours(self, cell):
        '''
        Adds neighbouring cells of a successful hit to the computer's target list.

        Behaviour:
        - considers the four orthogonal neighbours (left, right, up, down)
        - ignores diagonal cells
        - adds only cells that are inside the board boundaries
        - skips cells that were already attacked or already stored as targets

        Purpose:
        - supports targeted search after a hit
        - increases the probability of consecutive hits by focusing on nearby cells
        :param cell:
        :return:
        '''

        r,c=cell

        candidates = [
            (r,c-1),
            (r,c+1),
            (r-1,c),
            (r+1,c)
        ]

        for nr,nc in candidates:
            if 1<=nr<=10 and 1<=nc<=10:
                neighbour = (nr, nc)
                if neighbour not in self.board_repo.computer_hits and neighbour not in self.board_repo.computer_misses and neighbour not in self.board_repo.computer_targets:
                    self.board_repo.computer_targets.append(neighbour)

    def game_over(self):
        '''

        Checks if the game has ended.
        - ends immediately if all user plane heads are destroyed
        - allows one final computer move after all computer plane heads are destroyed
        - ends the game on the next check
        :return:
        '''
        if self.board_repo.all_user_heads_destroyed():
            return True
        if self.board_repo.all_computer_heads_destroyed():
            if not self.user_finished:
                self.user_finished = True
                return False # last chance for computer
            return True # stop after that move
        return False


    def get_winner(self):
        '''

        :return:
        Determines the game outcome.
        - returns "Draw!" if both players destroyed all plane heads
        - returns "You won!" if only the computer planes are destroyed
        - returns "You lost!" otherwise
        '''
        user_won = self.board_repo.all_computer_heads_destroyed()
        computer_won = self.board_repo.all_user_heads_destroyed()
        if user_won and computer_won:
            return "Draw!"
        if user_won:
            return "You won!"
        return "You lost!"

    def get_user_board(self):
        '''

        :return: the current user board with planes, hits, and misses.
        '''
        return self.board_repo.get_user_board()

    def get_target_board(self):
        '''

        :return: the board representing the user's view of the computer board, containing only hit and miss information.
        '''
        board = Board()
        for r, c in self.board_repo.user_hits:
            board.set_hit(r, c)
        for r, c in self.board_repo.user_misses:
            board.set_miss(r, c)
        return board

'''

   ?

   ?
 ?xxx?
   ?

   ?

'''