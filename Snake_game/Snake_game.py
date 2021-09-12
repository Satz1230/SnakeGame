import time
from tkinter import *
import random
import threading
import pickle
from tkinter import messagebox

# CONSTANTS ----
colors = ['#9400D3','#4B0082','#0000FF','#00FF00','#FFFF00','#FF7F00','#FF0000']
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 150
PARTS_SIZE = 40
BODY_PARTS = 3
# -----------

# To pick a random colors for the game
color_list = []
for i in range(3):
    col = colors.pop(random.randint(0,6-i))
    color_list.append(col)
SNAKE_COLOR = color_list[0]
FOOD_COLOR = color_list[1]
# If background color == Red; pick another color from the list
BACKGROUND_COLOR = [random.choice(colors) if color_list[2] == "#FF0000" else color_list[2]][0]
# ----------------

# load high score
high_score = int
try:
    with open('data.txt', 'rb') as f:
        high_score = pickle.load(f)
except:
    high_score = 0


# RGB MODE -------------------------------------
def rainbows():
    global SNAKE_COLOR, FOOD_COLOR
    while True:
        for i in reversed(colors):
            FOOD_COLOR = i
            SNAKE_COLOR = i
            time.sleep(1)
def rainbowb():
    while True:
        for j in colors:
            BACKGROUND_COLOR = j
            canvas.config(bg=BACKGROUND_COLOR)
            label.config(bg=BACKGROUND_COLOR)
            score_label.config(bg=BACKGROUND_COLOR)
            highscore_label.config(bg=BACKGROUND_COLOR)
            frame.config(bg=BACKGROUND_COLOR)
            time.sleep(2)
# ----------------------------------------------

# snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0,BODY_PARTS):
            self.coordinates.append([i,i])
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y,x+PARTS_SIZE,y+PARTS_SIZE,fill=SNAKE_COLOR,tag="snake")
            self.squares.append(square)

# food class
class Food:
    def __init__(self):
        x = random.randint(0,(GAME_WIDTH/PARTS_SIZE)-1) * PARTS_SIZE
        y = random.randint(0, (GAME_HEIGHT/PARTS_SIZE) - 1) * PARTS_SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x,y,x+PARTS_SIZE,y+PARTS_SIZE,fill=FOOD_COLOR,tag="food")


# main Function
def next_turn(snake, food):
    x,y = snake.coordinates[0]
    global high_score

    if direction == 'up':
        y -= PARTS_SIZE
    elif direction == 'down':
        y += PARTS_SIZE
    elif direction == 'left':
        x -= PARTS_SIZE
    elif direction == 'right':
        x += PARTS_SIZE


    snake.coordinates.insert(0,(x,y))

    square = canvas.create_rectangle(x, y, x + PARTS_SIZE, y + PARTS_SIZE, fill=SNAKE_COLOR, tag="snake")

    snake.squares.insert(0,square)


    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        global SPEED
        score += 1
        score_label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
        if SPEED > 50:
            SPEED -= 2
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if score > high_score:
        high_score = score
        highscore_label.config(text=f"Highscore: {high_score}")
        try:
            with open('data.txt', 'wb') as f:
                pickle.dump(high_score, f)
        except:
            pass
    else:
        pass

    if check_collision(snake):
        game_over()

    else:
     window.after(SPEED, next_turn, snake, food)


# to change direction
def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

# to check collision
def check_collision(snake):
    x,y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return "x"
    elif y < 0 or y >= GAME_HEIGHT:
        return "y"

    for i in snake.coordinates[1:]:
        if x == i[0] and y == i[1]:
            return True
    return False

# game over function
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,font=("ds-digital",100),text="Game Over",fill="red",tag="gameover")

    #
    ask = messagebox.askyesno(title="Re-match(BETA)",message="Wanna play again!")
    if ask:
        new_game()
    else:
        quit(0)

# new game function
def new_game():
    global score
    global SPEED
    snake = Snake()
    food = Food()
    next_turn(snake, food)

    SPEED = 150
    canvas.delete("gameover")
    score = 0
    score_label.config(text=f"Score: {score}")


# GUI Window Loop
window = Tk()
# Window Configs.
window.title("Snake got RGB Lights")
window.resizable(False, False)
window.iconphoto(True,PhotoImage(file="media file/iconphoto.png"))
# main frame
frame = Frame(window,bg=BACKGROUND_COLOR)
frame.pack()

score = 0
direction = 'right'

# frame items
label = Label(frame,text="",font=("ds-digital",30),bg=BACKGROUND_COLOR)
label.grid(row=0,column=0,sticky=NW)
score_label = Label(frame,text=f"Score: {score}",font=("ds-digital",40),bg=BACKGROUND_COLOR)
score_label.grid(row=0,columnspan=2)
highscore_label = Label(frame,text=f"Highscore: {high_score}",font=("ds-digital",20),bg=BACKGROUND_COLOR)
highscore_label.grid(row=0,column=1,sticky=NE)
canvas = Canvas(frame,bg=BACKGROUND_COLOR,width=GAME_WIDTH,height=GAME_HEIGHT)
canvas.grid(row=1,columnspan=2)

# to update window after each iteration
window.update()

# To Display The window in the center of the screen
frame_width = frame.winfo_width()
frame_height = frame.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2)-(frame_width/2))
y = int((screen_height/2)-(frame_height/2))
window.geometry(f"{frame_width}x{frame_height}+{x}+{y}")
# ---------------------------------------------

# Key Binds --------------------------------------
window.bind("<w>", lambda event:change_direction('up'))
window.bind("<s>", lambda event:change_direction('down'))
window.bind("<a>", lambda event:change_direction('left'))
window.bind("<d>", lambda event:change_direction('right'))
window.bind("<Up>", lambda event:change_direction('up'))
window.bind("<Down>", lambda event:change_direction('down'))
window.bind("<Left>", lambda event:change_direction('left'))
window.bind("<Right>", lambda event:change_direction('right'))
# --------------------------------------------------

ask = messagebox.askyesno(title="RGB MODE",message="Wanna Destroy your eyes!",icon="question")
if ask:
    rainbowt = threading.Thread(target=rainbows,daemon=True)
    rainbowtb = threading.Thread(target=rainbowb, daemon=True)
    rainbowt.start()
    rainbowtb.start()
snake = Snake()
food = Food()
next_turn(snake,food)
window.mainloop()
# dump the high score after the loop breaks
