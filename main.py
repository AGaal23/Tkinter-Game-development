from tkinter import *
from tkinter import font
import random
import time

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 150  # PLAYER speed
SPACE_SIZE = 50
BODY_PARTS = 2
SPAWN_NUMBER = 10
PLAYER_COLOR = "#588BAE"
OBSTACLE_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "#B8B09B"

#Player class for player logic
class Player:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        #Initialize player coordinates and size
        for i in range(0, BODY_PARTS):
            self.coordinates.append([GAME_WIDTH / 2, GAME_HEIGHT])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=PLAYER_COLOR, tag="player")
            self.squares.append(square)

#Obstacle class for obstacle logic
class Obstacle:
    def __init__(self):
        x = random.randint(0, (int(GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE  # range is x coor. to y coor. 700/50=14
        y= 0

        self.coordinates = [x, y]

        #Create obstacle
        self.shape = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")

#Function to move obstacle downward
def obs_move():
    global obs_speed
    for obs in obstacles:
        canvas.move(obs.shape, 0, SPACE_SIZE)
        obs.coordinates[1] += SPACE_SIZE
        if obs.coordinates[1] >= GAME_HEIGHT:
            # If obstacle goes below the screen, remove it and create a new one
            canvas.delete(obs.shape)
            obstacles.remove(obs)
            new_obstacle = Obstacle()
            obstacles.append(new_obstacle)
            if obs_speed < 7:
                obs_speed += 1
    window.after(1000 - (obs_speed*100), obs_move)

#function to handle player's turn
def game_turn(player, obstacle):

    if is_it_game_over:
        return

    x, y = player.coordinates[0]
    x2, y2 = player.coordinates[1]

    #player movement
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    player.coordinates.insert(0, (x, y))

    #Check for collisions between player and obstacles
    for obstacle in obstacles:
        if (x == obstacle.coordinates[0] and y == obstacle.coordinates[1]) or (x2 == obstacle.coordinates[0] and y2 == obstacle.coordinates[1]):
            game_over()

    #if the game is not over, continue the player movement
    if not is_it_game_over:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=PLAYER_COLOR)

        player.squares.insert(0, square)

        #remove the tail of the player to maintain body size
        del player.coordinates[-1]
        canvas.delete(player.squares[-1])
        del player.squares[-1]

        #check for collisions if player collides with its own body if you change the BODY_PARTS to more than 3
        if check_collisions(player, obstacle):
            game_over()
        else:
            window.after(SPEED, game_turn, player, obstacle)

#function to change player direction
def change_direction(new_direction):
    global direction

    #stops a 360 degree movement
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

#function to check collisions between player and obstacles
def check_collisions(player,obstacle):
    x, y = player.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    if x == obstacle.coordinates[0] and y == obstacle.coordinates[1]:
        return True
    for body_part in player.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

#function to handle game over conditions
def game_over():
    global is_it_game_over, frozen_time, obstacles

    is_it_game_over = True
    start_stop()
    canvas.delete(ALL)
    frozen_time = time.time() - start_time
    time_label.config(text=f"Time: {format_time(frozen_time)}")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() - 500, font=('Times', 70, 'bold'), text="GAME OVER",
                       fill="red", tag="game over")

#function to update the stopwatch
def update_stopwatch():
    if not is_it_game_over:
        current_time = time.time() - start_time
        time_string = format_time(current_time)
        time_label.config(text=f"Time: {time_string}")
    window.after(1000, update_stopwatch)  # Update every 1000 milliseconds (1 second)

#function to format time in HH:MM:SS format
def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

#function to start or stop game
def start_stop():
    global start_time, running
    if running:
        running = False
        start_time = time.time() - (frozen_time if is_it_game_over else 0)
    else:
        running = True
        update_stopwatch()

#create the game window
window = Tk()
window.title("Game")

#initial variables of the game
direction = 'up'
is_it_game_over = False
frozen_time = 0
obs_speed = 0
running = False
start_time = time.time()

#label to display time
time_label = Label(window, text="Time: 00:00:00", font=('Courier', 20))
time_label.pack(pady=20)

update_stopwatch()

#Game canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

#Window positioning
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# window position
window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

#Bind keys for player movement
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

#Initialize the player and obstacles and start the game loop
player = Player()

obstacles = [Obstacle() for _ in range(SPAWN_NUMBER)]

game_turn(player, obstacles)

obs_move()

window.mainloop()
