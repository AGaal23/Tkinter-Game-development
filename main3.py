from tkinter import *
import random
import time

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100  # speed inc. factor
INITIAL_SPEED = 300  # Initial speed
SPEED_DECREMENT = 10
SPACE_SIZE = 25
BODY_PARTS = 2
PLAYER_COLOR = "#00FF00"
OBSTACLE_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Player:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([GAME_WIDTH / 2, GAME_HEIGHT])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=PLAYER_COLOR, tag="player")
            self.squares.append(square)


class Obstacle:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = 0

        self.coordinates = [x, y]

        self.shape = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")


def obs_move():
    # Calculate the speed for this level
    current_speed = INITIAL_SPEED - (level - 1) * SPEED_DECREMENT

    for obstacle in obstacles:
        canvas.move(obstacle.shape, 0, SPACE_SIZE)
        obstacle.coordinates[1] += SPACE_SIZE
        if obstacle.coordinates[1] >= GAME_HEIGHT:
            canvas.delete(obstacle.shape)
            obstacles.remove(obstacle)
            new_obstacle = Obstacle()
            obstacles.append(new_obstacle)

    canvas.after(current_speed, obs_move)  # Use the calculated speed for this level


def next_turn(player, obstacle):
    if is_it_game_over:
        return

    x, y = player.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    player.coordinates.insert(0, (x, y))

    for obstacle in obstacles:
        if x == obstacle.coordinates[0] and y == obstacle.coordinates[1]:
            game_over()

    if not is_it_game_over:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=PLAYER_COLOR)

        player.squares.insert(0, square)

        del player.coordinates[-1]
        canvas.delete(player.squares[-1])
        del player.squares[-1]

        if check_collisions(player, obstacle):
            game_over()
        else:
            window.after(SPEED, next_turn, player, obstacle)

    # Increase the game speed every 10 seconds
    if time.time() - start_time >= 10:
        level_inc()

def change_direction(new_direction):
    global direction

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

def check_collisions(player, obstacle):
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

def game_over():
    global is_it_game_over, frozen_time

    is_it_game_over = True
    canvas.delete(ALL)
    frozen_time = time.time() - start_time
    score_label.config(text=f"Score: {score}")
    time_label.config(text=f"Time: {format_time(frozen_time)}")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text="Game Over",
                       fill="red", tag="game over")

def restart_game():
    global player, obstacles, score, direction, level, is_it_game_over, start_time

    reset()
    is_it_game_over = False
    level = 1
    canvas.delete(ALL)
    player = Player()
    obstacles = [Obstacle() for _ in range(10)]
    score = 0
    direction = 'up'
    score_label.config(text=f"Score: {score}")
    time_label.config(text="Time: 00:00:00")
    start_time = time.time()
    next_turn(player, obstacles)
    obs_move()

def update_stopwatch():
    if not is_it_game_over:
        current_time = time.time() - start_time
        time_string = format_time(current_time)
        time_label.config(text=f"Time: {time_string}")
    window.after(1000, update_stopwatch)

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def start_stop():
    global running, start_time

    if running:
        running = False
        start_time = time.time() - (frozen_time if is_it_game_over else 0)
        start_stop_button.config(text="Resume")
    else:
        running = True
        start_stop_button.config(text="Pause")
        update_stopwatch()

def reset():
    global start_time, running
    start_time = time.time()
    running = False
    time_label.config(text="Time: 00:00:00")
    start_stop_button.config(text="Start")

def level_inc():
    global level

    level += 1
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 40),
                       text=f"Level {level}", fill="white")
    canvas.update()
    time.sleep(2)
    canvas.delete(ALL)
    obstacles.clear()
    restart_game()

window = Tk()
window.title("Game")

score = 0
direction = 'up'
is_it_game_over = False
frozen_time = 0
level = 1
running = False
start_time = time.time()

score_label = Label(window, text=f"Score: {score}", font=('consolas', 40))
score_label.pack(pady=20)

time_label = Label(window, text="Time: 00:00:00", font=('consolas', 20))
time_label.pack(pady=20)

update_stopwatch()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

player = Player()
obstacles = [Obstacle() for _ in range(10)]

start_stop_button = Button(window, text="Start", command=start_stop, font=('consolas', 20))
start_stop_button.pack(pady=20)

restart_button = Button(window, text="Restart", command=restart_game, font=('consolas', 20))
restart_button.pack()

next_turn(player, obstacles)
obs_move()

window.mainloop()

'''
    # add restart button to window
    restart_button = Button(window, text="Restart", command=restart_game, font=('consolas', 20))
    restart_button.place(x=0, y=0)
'''
'''
    if x == obstacle.coordinates[0] and y == obstacle.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("obstacle")
        obstacle = Obstacle()
        obstacles.append(obstacle)
        game_over()
'''
'''
def restart_game():
    global player, obstacle, running, direction, obs_speed, is_it_game_over, start_time, frozen_time

    # Reset game variables to initial values
    reset()
    direction = 'up'
    is_it_game_over = False
    frozen_time = 0
    obs_speed = 1
    running = False
    start_time = time.time()
    canvas.delete(ALL)
    player = Player()
    obstacle = [Obstacle() for _ in range(10)]
    time_label.config(text="Time: 00:00:00")
    start_time = time.time()
    next_turn(player, obstacle)
    obs_move()
'''
'''
def reset():
    global start_time, running
    start_time = time.time()
    running = False
    time_label.config(text="Time: 00:00:00")
'''
'''
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack(pady=20)
'''
'''
#add timer to window
stopwatch_label = Label(window, text="Time: 00:00:00", font=('consolas', 20))
stopwatch_label.pack()
'''
'''
label = Label(window, text="Time: 00:00:00", font=('consolas', 20))
label.pack(pady=20)
'''
    # oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

        # canvas.move(oval,0,10)
