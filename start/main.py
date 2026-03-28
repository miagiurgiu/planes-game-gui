# import service
from service.board_service import BoardService

# import repo
from repository.board_repo import BoardRepository

# import ui, gui
from ui.ui import ConsoleUI
from ui.gui import ConsoleGUI

# import validator
from validation.validation import Validation

# import errors

def main():
    '''
    Application entry point.
        - initializes repository, service, and validation layers
        - allows the user to choose between console and GUI interfaces
        - starts the selected user interface
    '''

    # instantiate repos
    board_repo = BoardRepository()

    # instantiate validators
    validation = Validation()

    # instantiate services
    service = BoardService(board_repo)

    # choose ui/gui
    while True:
        try:
            mode = input("Choose interface (ui/gui): ").strip().lower()
            if mode == "ui":
                ui = ConsoleUI(service, validation)
                break
            elif mode == "gui":
                ui = ConsoleGUI(service, validation)
                break
            else:
                print("Invalid mode")
        except KeyboardInterrupt:
            print("\nProgram interrupted by the user."),
            return

    # use run() from the ui/gui class to run the program
    ui.run()

if __name__ == "__main__":
    main()

