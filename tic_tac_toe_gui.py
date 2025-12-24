import tkinter as tk
import random
import pygame

# ---------------- WINDOW ---------------- #
root = tk.Tk()
root.title("Tic Tac Toe AI")
root.geometry("360x520")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

# ---------------- PYGAME SOUND INIT ---------------- #
pygame.mixer.init()

# Pre-load sounds (put these files in the SAME folder as your .py)
SOUNDS = {
    "click": pygame.mixer.Sound("click.mp3"),
    "win": pygame.mixer.Sound("win.mp3"),
    "lose": pygame.mixer.Sound("lose.mp3"),
}

def play_sound(name):
    """Non-blocking sound (pygame mixer plays asynchronously)."""
    try:
        SOUNDS[name].play()
    except Exception as e:
        print(f"Sound error: {e}")

# ---------------- VARIABLES ---------------- #
board = [" "] * 9
buttons = []
difficulty = tk.StringVar(value="Easy")

BG = "#1e1e2f"
BTN = "#2a2a40"
X_COLOR = "#00ffcc"
O_COLOR = "#ff4d6d"
TEXT = "white"

# ---------------- GAME LOGIC ---------------- #
def check_winner(p):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    return any(all(board[i] == p for i in combo) for combo in wins)

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
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# -------- AI MOVE -------- #
def empty_cells():
    return [i for i in range(9) if board[i] == " "]

def animate(btn):
    btn.config(relief="sunken")
    root.after(120, lambda: btn.config(relief="raised"))

def end_game(msg, sound=None):
    status.config(text=msg)
    if sound:
        play_sound(sound)
    for b in buttons:
        b.config(state="disabled")

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
    ai_move()
    if check_winner("O"):
        end_game("AI WINS 🤖", "lose")
    elif is_draw():
        end_game("DRAW 🤝")

def click(i):
    if board[i] != " ":
        return

    play_sound("click")
    board[i] = "X"
    animate(buttons[i])
    buttons[i].config(text="X", fg=X_COLOR, state="disabled")

    if check_winner("X"):
        end_game("YOU WIN 🏆", "win")
        return
    if is_draw():
        end_game("DRAW 🤝")
        return

    root.after(300, ai_turn)

def reset():
    for i in range(9):
        board[i] = " "
        buttons[i].config(text=" ", state="normal", fg=TEXT)
    status.config(text="Your Turn")

# ---------------- GUI ---------------- #
status = tk.Label(root, text="Your Turn",
                  font=("Arial", 18, "bold"),
                  fg=TEXT, bg=BG)
status.pack(pady=15)

frame = tk.Frame(root, bg=BG)
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text=" ",
                    font=("Arial", 28, "bold"),
                    width=4, height=2,
                    bg=BTN, fg=TEXT,
                    activebackground="#3a3a55",
                    command=lambda i=i: click(i))
    btn.grid(row=i//3, column=i%3, padx=6, pady=6)
    buttons.append(btn)

tk.Label(root, text="Difficulty",
         fg=TEXT, bg=BG, font=("Arial", 12)).pack(pady=10)

tk.OptionMenu(root, difficulty, "Easy", "Medium", "Hard").pack()

tk.Button(root, text="Restart",
          font=("Arial", 12, "bold"),
          bg="#ffcc00",
          command=reset).pack(pady=20)

root.mainloop()
