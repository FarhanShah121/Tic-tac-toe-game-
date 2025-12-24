import tkinter as tk
import random
import pygame

# ---------------- WINDOW ---------------- #
root = tk.Tk()
root.title("Tic Tac Toe AI")
root.update_idletasks()
root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
root.configure(bg="#141427")
root.resizable(False, False)

# ---------------- PYGAME SOUND INIT ---------------- #
pygame.mixer.init()

SOUNDS = {
    "click": pygame.mixer.Sound("click.mp3"),
    "win": pygame.mixer.Sound("win.mp3"),
    "lose": pygame.mixer.Sound("lose.mp3"),
}

def play_sound(name):
    try:
        SOUNDS[name].play()
    except Exception as e:
        print(f"Sound error: {e}")

# ---------------- VARIABLES ---------------- #
board = [" "] * 9
buttons = []
difficulty = tk.StringVar(value="Easy")
game_over = False

# Theme
BG = "#141427"
PANEL = "#1c1c36"
BTN = "#242447"
BTN_HOVER = "#2e2e5a"
GRID_BORDER = "#34345f"
X_COLOR = "#00ffd5"
O_COLOR = "#ff4d6d"
TEXT = "#ffffff"
SUBTEXT = "#b9b9d6"
WIN_HIGHLIGHT = "#32cd32"

# ---------------- GAME LOGIC ---------------- #
wins = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def check_winner(p):
    for combo in wins:
        if all(board[i] == p for i in combo):
            return combo
    return None

def is_draw():
    return " " not in board

# -------- MINIMAX -------- #
def minimax(is_max):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_max:
        best = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                best = max(best, minimax(False))
                board[i] = " "
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                best = min(best, minimax(True))
                board[i] = " "
        return best

def best_move():
    best_score = -100
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# -------- UI HELPERS -------- #
def empty_cells():
    return [i for i in range(9) if board[i] == " "]

def animate(btn):
    btn.config(relief="sunken")
    root.after(120, lambda: btn.config(relief="flat"))

def set_status(text, color=TEXT):
    status.config(text=text, fg=color)

def highlight_winner(combo):
    if not combo:
        return
    for i in combo:
        buttons[i].config(bg=WIN_HIGHLIGHT, fg="#0b0b15")

def lock_board():
    for b in buttons:
        b.config(state="disabled")

def unlock_board():
    for i, b in enumerate(buttons):
        if board[i] == " ":
            b.config(state="normal")

def end_game(msg, sound=None, win_combo=None):
    global game_over
    game_over = True
    set_status(msg)
    if win_combo:
        highlight_winner(win_combo)
    if sound:
        play_sound(sound)
    lock_board()

# -------- AI MOVE -------- #
def ai_move():
    empties = empty_cells()
    if not empties:
        return

    if difficulty.get() == "Easy":
        move = random.choice(empties)
    elif difficulty.get() == "Medium":
        move = random.choice(empties) if random.choice([True, False]) else best_move()
    else:  # Hard
        move = best_move()

    board[move] = "O"
    animate(buttons[move])
    buttons[move].config(text="O", fg=O_COLOR, state="disabled")

def ai_turn():
    if game_over:
        return

    ai_move()
    win_combo = check_winner("O")
    if win_combo:
        end_game("AI WINS 🤖", "lose", win_combo)
    elif is_draw():
        end_game("DRAW 🤝")

# -------- PLAYER CLICK -------- #
def click(i):
    global game_over
    if game_over or board[i] != " ":
        return

    play_sound("click")
    board[i] = "X"
    animate(buttons[i])
    buttons[i].config(text="X", fg=X_COLOR, state="disabled")

    win_combo = check_winner("X")
    if win_combo:
        end_game("YOU WIN 🏆", "win", win_combo)
        return
    if is_draw():
        end_game("DRAW 🤝")
        return

    lock_board()
    root.after(300, lambda: (unlock_board(), ai_turn()))

# -------- RESET -------- #
def reset():
    global game_over
    game_over = False
    for i in range(9):
        board[i] = " "
        buttons[i].config(
            text=" ",
            state="normal",
            fg=TEXT,
            bg=BTN,
            relief="flat"
        )
    set_status("Your Turn", SUBTEXT)

# ---------------- GUI ---------------- #
title = tk.Label(
    root, text="TIC TAC TOE",
    font=("Segoe UI", 26, "bold"),
    fg=TEXT, bg=BG
)
title.pack(pady=(18, 6))

status = tk.Label(
    root, text="Your Turn",
    font=("Segoe UI", 14, "bold"),
    fg=SUBTEXT, bg=BG
)
status.pack(pady=(0, 12))

# Control panel
panel = tk.Frame(root, bg=PANEL, highlightbackground=GRID_BORDER, highlightthickness=1)
panel.pack(padx=18, pady=10, fill="x")

tk.Label(panel, text="Difficulty", fg=SUBTEXT, bg=PANEL, font=("Segoe UI", 11, "bold")).pack(pady=(10, 4))

opt = tk.OptionMenu(panel, difficulty, "Easy", "Medium", "Hard")
opt.config(
    bg=BTN, fg=TEXT, activebackground=BTN_HOVER,
    relief="flat", highlightthickness=0,
    font=("Segoe UI", 11, "bold"),
)
opt["menu"].config(bg=BTN, fg=TEXT)
opt.pack(pady=(0, 12), ipadx=8, ipady=3)

restart_btn = tk.Button(
    panel, text="Restart",
    font=("Segoe UI", 12, "bold"),
    bg="#ffcc00", fg="#0b0b15",
    relief="flat",
    command=reset
)
restart_btn.pack(pady=(0, 12), ipadx=12, ipady=6)

# Board frame
board_frame = tk.Frame(root, bg=BG)
board_frame.pack(pady=14)

grid = tk.Frame(board_frame, bg=GRID_BORDER, padx=6, pady=6)
grid.pack()

def on_enter(btn):
    if btn["state"] == "normal":
        btn.config(bg=BTN_HOVER)

def on_leave(btn):
    if btn["state"] == "normal":
        btn.config(bg=BTN)

for i in range(9):
    btn = tk.Button(
        grid,
        text=" ",
        font=("Segoe UI", 32, "bold"),
        width=3, height=1,
        bg=BTN, fg=TEXT,
        activebackground=BTN_HOVER,
        relief="flat",
        bd=0,
        command=lambda i=i: click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=6, pady=6)
    btn.bind("<Enter>", lambda e, b=btn: on_enter(b))
    btn.bind("<Leave>", lambda e, b=btn: on_leave(b))
    buttons.append(btn)

footer = tk.Label(
    root,
    text="Tip: Hard = unbeatable 🔥",
    font=("Segoe UI", 10),
    fg=SUBTEXT,
    bg=BG
)
footer.pack(pady=12)

root.mainloop()
