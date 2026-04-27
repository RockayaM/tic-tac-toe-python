#Tic-Tac-Toe Game for GENG0033 Labwork 2.
#Created by: Rockaya Marmoush (ID: 37428756)
#Features: AI Opponent, Score Saving, Modern UI, Dynamic Turn Colours

import tkinter as tk
import random
import os

#Game mode: "Single" for vs AI, "Multi" for two human players
game_mode = "Single"
#Checks who's turn it is
current_player = "X"
#Tracks if game has ended to prevent further moves
game_over = False
#Initialize score variables
score_x = 0
score_o = 0

#Saves the current X and O scores into a text file
def save_scores():
    #Open scores.txt in write mode ('w') to save the latest numbers
    try:
        with open("scores.txt", "w") as f:
            f.write(f"{score_x},{score_o}")
    except OSError:
        #If file can't be written, silently skip saving
        pass


#Loads previous scores from the text file on startup
#Handles missing file, empty file, or corrupted data safely
def load_scores():
    global score_x, score_o
    if os.path.exists("scores.txt"):
        try:
            with open("scores.txt", "r") as f:
                data = f.read().split(",")
                score_x = int(data[0])
                score_o = int(data[1])
        except (ValueError, IndexError):
            #If data is missing or not a valid number, reset to zero
            score_x = 0
            score_o = 0

#Updates the score for the winner and saves it to file
def update_score(winner):
    global score_x, score_o
    if winner == "X":
        score_x += 1
    else:
        score_o += 1
    
    score_label.config(text=f"PLAYER X: {score_x}  |  PLAYER O: {score_o}")
    save_scores()

#Helper function to change the background of winning buttons
def highlight_winner(winning_buttons):
    for btn in winning_buttons:
        btn.config(bg="#A8DADC", fg="white")

#This function checks if there is a winner
def check_winner():
    global game_over

    #Check rows
    for r in range(3):
        if buttons[r][0]["text"] == buttons[r][1]["text"] == buttons[r][2]["text"] != " ":
            winner = buttons[r][0]["text"]
            player_turn.config(text=f"Player {winner} Wins!", fg="green")
            highlight_winner([buttons[r][0], buttons[r][1], buttons[r][2]])
            update_score(winner)
            game_over = True
            return
  
    #Check columns
    for c in range(3):
        if buttons[0][c]["text"] == buttons[1][c]["text"] == buttons[2][c]["text"] != " ":
            winner = buttons[0][c]["text"]
            player_turn.config(text=f"Player {winner} Wins!", fg="green")
            highlight_winner([buttons[0][c], buttons[1][c], buttons[2][c]])
            update_score(winner)
            game_over = True
            return 
            
    #Check diagonal (top left to bottom right)
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != " ":
        winner = buttons[0][0]["text"]
        player_turn.config(text=f"Player {winner} Wins!", fg="green")
        highlight_winner([buttons[0][0], buttons[1][1], buttons[2][2]])
        update_score(winner)
        game_over = True
        return 

    #Check diagonal (top right to bottom left)
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != " ":
        winner = buttons[0][2]["text"]
        player_turn.config(text=f"Player {winner} Wins!", fg="green")
        highlight_winner([buttons[0][2], buttons[1][1], buttons[2][0]])
        update_score(winner)
        game_over = True
        return
        
    #Check for a draw
    if all(buttons[r][c]["text"] != " " for r in range(3) for c in range(3)):
        player_turn.config(text="It's a Draw!", fg="orange")
        game_over = True
        return

#Checks if player can win in one move, and returns that cell
def find_winning_move(player):
    for r in range(3):
        for c in range(3):
            if buttons[r][c]["text"] == " ":
                buttons[r][c]["text"] = player
                win = is_winning(player)
                buttons[r][c]["text"] = " "
                if win:
                    return (r, c)
    return None

#Checks if player currently has three in a row
def is_winning(player):
    for r in range(3):
        if all(buttons[r][c]["text"] == player for c in range(3)):
            return True
    for c in range(3):
        if all(buttons[r][c]["text"] == player for r in range(3)):
            return True
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] == player:
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] == player:
        return True
    return False

#AI tries to win first, then blocks opponent, then picks randomly
def ai_move():
    if game_over:
        return

    #First, try to win
    move = find_winning_move("O")
    #Second, block the player from winning
    if not move:
        move = find_winning_move("X")
    #Third, fall back to a random empty cell
    if not move:
        empty_cells = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]["text"] == " "]
        if empty_cells:
            move = random.choice(empty_cells)

    if move:
        button_click(move[0], move[1])

#Function to handle button clicks
def button_click(row, col):
    global current_player, game_over

    #Stop if game is already over
    if game_over:
        return
    
    #Find button using coordinates
    btn = buttons[row][col]
    
    if btn["text"] == " ":
        btn["text"] = current_player

        if current_player == "X":
            btn.config(fg="#457B9D")
        else:
            btn.config(fg="#E63946")

        check_winner()

        if not game_over:
            current_player = "O" if current_player == "X" else "X"
            color = "#457B9D" if current_player == "X" else "#E63946"
            player_turn.config(text=f"Player {current_player}'s Turn", fg=color)

            #Only trigger AI if mode is Single and it's O's turn
            if game_mode == "Single" and current_player == "O":
                root.after(500, ai_move)

#This function clears the board and resets the game so players can play again.
def restart_game(): 
    global current_player, game_over
    current_player = "X"
    game_over = False
    player_turn.config(text="Player X's Turn", fg="#457B9D")

    for row in buttons:
        for btn in row:
            btn.config(text=" ", bg="#FFFFFF", fg="black")

#Resets both scores to zero and deletes the scores file
def reset_scores():
    global score_x, score_o
    score_x = 0
    score_o = 0
    score_label.config(text="PLAYER X: 0   |   PLAYER O: 0")
    if os.path.exists("scores.txt"):
        os.remove("scores.txt")

#--- Main GUI setup ---#
root = tk.Tk()
root.title("Tic-Tac-Toe")

root.config(bg="#F1FAEE", padx=15, pady=10)
root.resizable(False, False)

main_title = tk.Label(root, text="Tic-Tac-Toe", font=("Arial", 30, "bold"), fg="#1D3557", bg="#F1FAEE")
main_title.pack(side="top", pady=(20, 0))

#Brief instruction label shown below the title
instructions = tk.Label(root, text="Take turns clicking the board to place your mark. Get 3 in a row to win!", font=("Arial", 12), fg="#457B9D", bg="#F1FAEE", wraplength=350)
instructions.pack(side="top", pady=(5, 0))

#Create a frame to hold the mode selection
mode_frame = tk.Frame(root, bg="#F1FAEE")
mode_frame.pack(pady=5)

mode_var = tk.StringVar(value="Single")

def change_mode():
    global game_mode
    game_mode = mode_var.get()
    restart_game() #Reset the board when switching modes

#Radio buttons allow users to toggle between AI and Human opponents
tk.Radiobutton(mode_frame, text="vs AI", variable=mode_var, value="Single", 
               command=change_mode, bg="#F1FAEE", font=("Arial", 12)).pack(side="left", padx=10)
tk.Radiobutton(mode_frame, text="2-Player", variable=mode_var, value="Multi", 
               command=change_mode, bg="#F1FAEE", font=("Arial", 12)).pack(side="left", padx=10)

#Label to display whose turn it is and the game outcome
player_turn = tk.Label(root, text="Player X's Turn", font=("Arial", 16, "bold"), bg="#F1FAEE", fg="#457B9D")
player_turn.pack(side="top", pady=8)

#Frame for scores to keep spacing balanced
score_frame = tk.Frame(root, bg="#F1FAEE")
score_frame.pack(pady=5)

#Label to display the scores
score_label = tk.Label(score_frame, text="PLAYER X: 0   |   PLAYER O: 0", font=("Courier", 16, "bold"), fg="#1D3557", bg="#F1FAEE", width=30)
score_label.pack(pady=5)

#Container frame to organize the 3x3 grid of buttons
board_frame = tk.Frame(root, bg="#A8DADC", padx=5, pady=5)
board_frame.pack(pady=8)

#2D list used to store references to all buttons in the grid
buttons = [[None for _ in range(3)] for _ in range(3)]

#Nested loops to automatically create and grid 9 buttons
for r in range(3):
    for c in range(3):
        btn = tk.Button(board_frame, text=" ", width=3, height=1, font=("Arial", 26, "bold"), bg="#FFFFFF", relief="flat", activebackground="#F1FAEE")
        btn.grid(row=r, column=c, padx=5, pady=5)

        btn.config(command=lambda row=r, col=c: button_click(row, col))

        buttons[r][c] = btn

#Frame to hold both buttons side by side
button_frame = tk.Frame(root, bg="#F1FAEE")
button_frame.pack(pady=(8, 8))

restart_button = tk.Button(button_frame, text="Restart", bg="#CD5C5C", fg="white", font=("Arial", 14, "bold"), padx=20, pady=10, command=restart_game)
restart_button.pack(side="left", padx=10)

reset_scores_button = tk.Button(button_frame, text="Reset Scores", bg="#457B9D", fg="white", font=("Arial", 14, "bold"), padx=20, pady=10, command=reset_scores)
reset_scores_button.pack(side="left", padx=10)

#--- Startup Logic ---#
#Load scores from the file when the app starts
load_scores()
score_label.config(text=f"PLAYER X: {score_x}  |  PLAYER O: {score_o}")

#Center the window on the screen when the app launches
root.eval('tk::PlaceWindow . center')
root.mainloop()