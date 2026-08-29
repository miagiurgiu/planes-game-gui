from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class ConsoleGUI:
    # Color palette constants derived from the pixel-art plane image
    BG_DARK = "#0B0B0B"  # Pitch-black background
    BG_FRAME = "#1C0A18"  # Dark plum container frame
    CELL_EVEN = "#2E1128"  # Checkerboard dark purple cell
    CELL_ODD = "#45193C"  # Checkerboard lighter purple cell
    HEADER_BG = "#6E2457"  # Magenta header background
    GRID_BORDER = "#8A3370"  # Cell outline

    TEXT_PINK = "#FF99C8"  # Soft pink for text
    TEXT_WHITE = "#FFFFFF"  # Crisp white highlight
    TEXT_DARK = "#1C0A18"  # Dark text for bright buttons

    COLOR_PLANE = "#F27DB7"  # Bubblegum pink plane fill
    COLOR_HIT_HEAD = "#FF2E63"  # Bright red-pink head hit
    COLOR_HIT_BODY = "#FFB3D9"  # Pastel hit text
    COLOR_MISS = "#00E5FF"  # Bright cyan miss marker

    def __init__(self, service, validation):
        self._service = service
        self._validation = validation
        self._plane_index = 1


    def run(self):
        self._service.place_computer_planes()
        self._create_window()
        #self._gui_place_user_planes()
        self._root.mainloop()

    def _create_window(self):
        self._root = Tk()  # create the window
        self._root.title("Planes Game")  # title of the window
        self._root.geometry("800x600")  # size of the window
        self._root.configure(bg=self.BG_DARK)


        img = Image.open("/Users/Maria/Downloads/image.png")
        img = img.resize((800, 600), Image.LANCZOS)
        self._background = ImageTk.PhotoImage(img)

        '''
        self._background = PhotoImage(file="/Users/Maria/Downloads/image.png")
        '''

        self._bg_label = Label(self._root, image=self._background)
        self._bg_label.pack()

        self._start_button = Button(
            self._root,
            text="START",
            font=("Arial", 22, "bold"),
            width=10,
            height=1,
            bg=self.COLOR_PLANE,
            fg=self.TEXT_DARK,
            activebackground=self.TEXT_PINK,
            activeforeground=self.TEXT_DARK,
            bd=0,
            cursor="hand2",
            command=self._start_game
        )

        self._start_button.place(relx=0.5, rely=0.8, anchor="center")

        self._boards = Frame(self._root, bg=self.BG_DARK)  # prep the two boards

        # left (user) board
        self._left = Frame(self._boards, bg=self.BG_DARK)
        Label(
            self._left,
            text="Your Board",
            font=("Consolas", 15, "bold"),
            bg=self.BG_DARK,
            fg=self.TEXT_PINK
        ).pack(pady=2)
        # self._user_board_frame = Frame(self._left)
        self._user_board_frame = Frame(self._left, bg=self.BG_FRAME, bd=2, relief="solid")

        # right (target) board
        self._right = Frame(self._boards, bg=self.BG_DARK)
        Label(
            self._right,
            text="Target Board",
            font=("Consolas", 15, "bold"),
            bg=self.BG_DARK,
            fg=self.TEXT_PINK
        ).pack(pady=2)
        # self._target_board_frame = Frame(self._right)
        self._target_board_frame = Frame(self._right, bg=self.BG_FRAME, bd=2, relief="solid")

    def _start_game(self):
        #self._info.config(text="") # remove the text from the _info label
        self._bg_label.destroy()
        self._start_button.destroy() # remove start button

        self._boards.pack(pady=10)
        self._left.grid(row=0, column=0, padx=20)
        self._right.grid(row=0, column=1, padx=20)

        self._user_board_frame.pack(pady=10) # show user board
        self._target_board_frame.pack(pady=10) # show target board
        self._draw_board(self._service.get_user_board(), True, self._user_board_frame)
        self._draw_board(self._service.get_target_board(), False, self._target_board_frame)

        self._input_frame = Frame(self._root, bg=self.BG_DARK)
        self._input_frame.pack(pady=10)
        #self._input_frame.lift()

        self._plane_label = Label(self._input_frame, text=f"Plane 1 coordinates:", font = ("Consolas", 15), bg=self.BG_DARK, fg=self.TEXT_PINK)
        self._plane_label.pack(side=LEFT, padx=5)
        self._plane_entry = Entry(
            self._input_frame,
            width=10,
            font=("Consolas", 14),
            bg=self.BG_FRAME,
            fg=self.TEXT_WHITE,
            insertbackground=self.TEXT_PINK,
            bd=1,
            relief="solid"
        )
        self._plane_entry.pack(side=LEFT, padx=5)
        self._plane_button = Button(
            self._input_frame,
            text="Place",
            command=self._place_plane,
            font=("Consolas", 12, "bold"),
            bg=self.COLOR_PLANE,
            fg=self.TEXT_DARK,
            activebackground=self.TEXT_PINK,
            activeforeground=self.TEXT_DARK,
            bd=0,
            padx=10
        )
        self._plane_button.pack(side=LEFT, padx=5)

        self._user_status = Label(self._right, text="", font=("Consolas", 11), bg=self.BG_DARK, fg=self.TEXT_WHITE)
        self._user_status.pack(padx=5)

        self._computer_status = Label(self._left, text="", font=("Consolas", 11), bg=self.BG_DARK, fg=self.TEXT_WHITE)
        self._computer_status.pack(padx=5)

        self._format_label = Label(
            self._input_frame,
            text="(Coordinates example: A3 B3)",
            font=("Consolas", 11, "italic"),
            bg=self.BG_DARK,
            fg=self.TEXT_PINK
        )
        self._format_label.pack(side=LEFT, padx=5)

    def _draw_board(self, board, show_planes, frame):
        # default_bg = frame.cget("bg")

        computer_heads = set()
        computer_plane_cells = set()
        user_heads = set()
        user_plane_cells = set()

        if show_planes:
            for plane in self._service.board_repo.user_planes:
                user_heads.add(plane[0])
                for cell in plane: # no problem that we add again the head because it's a set and no duplicates are stored
                    user_plane_cells.add(cell)
        else:
            for plane in self._service.board_repo.computer_planes:
                computer_heads.add(plane[0])
                for cell in plane:
                    computer_plane_cells.add(cell)

        for i in range(11):
            for j in range(11):
                cell = board.get(i, j)
                fg = self.TEXT_PINK
                bg = self.CELL_EVEN if (i + j) % 2 == 0 else self.CELL_ODD
                text = "."

                if i == 0 or j == 0:
                    text = str(cell)
                    bg = self.HEADER_BG
                    fg = self.TEXT_WHITE
                elif (i, j) in user_plane_cells and show_planes:
                    bg = self.COLOR_PLANE
                    fg = self.TEXT_DARK
                    if cell == board.HIT:
                        text = "X"
                        fg = self.COLOR_HIT_HEAD if (i, j) in user_heads else self.COLOR_HIT_BODY
                    else:
                        text = "■"
                elif cell == board.HIT:
                    text = "X"
                    fg = self.COLOR_HIT_HEAD if (i, j) in computer_heads else self.COLOR_HIT_BODY
                elif cell == board.MISS:
                    text = "O"
                    fg = self.COLOR_MISS

                Label(
                    frame,
                    text=text,
                    fg=fg,
                    bg=bg,
                    width=3,
                    height=2,
                    borderwidth=0,
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground=self.GRID_BORDER,
                    font=("Consolas", 11, "bold"),
                ).grid(row=i, column=j)

    def _place_plane(self):
        text = self._plane_entry.get().strip()
        if not text:
            messagebox.showerror("Error", "You must enter two coordinates")
            return
        parts = text.split()
        if len(parts) != 2:
            messagebox.showerror("Error", "You must enter two coordinates")
            return
        head, tail = parts
        if not self._validation.validate_coordinates(head) or not self._validation.validate_coordinates(tail):
            messagebox.showerror("Error", "Invalid coordinates format (A1-J10")
            return
        try: # what errors could i encounter here?
            self._service.place_user_planes(head, tail)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self._update_user_board()
        self._plane_entry.delete(0, END)
        self._plane_index+=1
        if self._plane_index <=3:
            self._plane_label.config(text=f"Plane {self._plane_index} coordinates:")
        else:
            self._game_loop()

    def _game_loop(self):
        self._plane_label.config(text="Your move:")
        self._plane_entry.delete(0, END)
        self._plane_button.config(text="Fire", command = self._user_move)

    def _user_move(self):
        move = self._plane_entry.get().strip()
        if not self._validation.validate_coordinates(move):
            messagebox.showerror("Error", "Invalid coordinates format (A1-J10")
            return
        try:
            usr_result = self._service.user_move(move)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self._user_status.config(text=usr_result)
        self._plane_entry.delete(0, END)
        self._update_target_board()

        if self._service.game_over():
            messagebox.showerror("Game Over", self._service.get_winner())
            self._plane_button.config(state=DISABLED)
            return

        comp_result = self._service.computer_move()
        self._computer_status.config(text=comp_result)
        self._update_user_board()

        if self._service.game_over():
            messagebox.showerror("Game Over", self._service.get_winner())
            self._plane_button.config(state=DISABLED)
            return

    def _update_user_board(self):
        for widget in self._user_board_frame.winfo_children():
            widget.destroy()
        self._draw_board(self._service.get_user_board(), True, self._user_board_frame)

    def _update_target_board(self):
        for widget in self._target_board_frame.winfo_children():
            widget.destroy()
        self._draw_board(self._service.get_target_board(), False, self._target_board_frame)