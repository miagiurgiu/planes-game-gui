# print empty board
# ask for plane 1, plane 2, plane 3
# ask for moves
# print hit/miss messages
# print boards after each move

from domain.board import Board
class ConsoleUI:
    def __init__(self, service, validation):
        self._service = service
        self._validation = validation

    def run(self):
        try:
            self._service.place_computer_planes()
            self._ui_place_user_planes()
            self._game_loop()
        except KeyboardInterrupt:
            print("\nProgram interrupted by the user")
            return

    def _ui_place_user_planes(self):
        print("Place your planes on the board giving HEAD and TAIL coordinates (ex: A3 D3):")
        self._print_board(self._service.get_user_board(), True) # print user board
        for i in range (1,4): #plane1, plane2, plane3
            while True:
                try:
                    coordinates = input(f"Plane {i}:").strip()
                    if not coordinates:
                        raise ValueError("You must enter two coordinates")
                    parts = coordinates.split()
                    if len(parts) != 2:
                        raise ValueError("You must enter two coordinates")
                    head = parts[0]
                    tail = parts[1]
                    if not self._validation.validate_coordinates(head) or not self._validation.validate_coordinates(tail):
                        raise ValueError("Invalid coordinates format (A1-J10)")
                    # UI sends raw strings to service (head=A3, tail = D3)
                    self._service.place_user_planes(head, tail)
                    self._print_board(self._service.get_user_board(), True)
                    break
                except ValueError as e:
                    print("Error: ", e)
                except KeyboardInterrupt:
                    raise

    def _game_loop(self):
        while not self._service.game_over():
            try:
                move = input("Your move:").strip()
                if not self._validation.validate_coordinates(move):
                    raise ValueError("Invalid coordinates")
                print(self._service.user_move(move)) # ce face??
            except ValueError as e:
                print("Error: ", e)
                continue
            self._print_board(self._service.get_target_board(), False)
            if self._service.game_over():
                break
            result = self._service.computer_move()
            print(result)
            self._print_board(self._service.get_user_board(), True)
        print(self._service.get_winner())

    def _print_board(self, board, show_planes):
        for i in range(11):
            for j in range(11):
                cell = board.get(i, j)
                if i==0 or j==0: # header
                    print(cell, end=" ")
                elif cell == board.HIT:
                    print("X", end = " ")
                elif cell == board.MISS:
                    print("O", end = " ")
                elif cell == board.PLANE and show_planes:
                    print("P", end = " ")
                else:
                    print(".", end = " ")
            print()
        print()
