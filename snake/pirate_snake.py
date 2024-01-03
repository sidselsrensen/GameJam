import curses
from random import randint, choice
import pythonji

border_x = 60
border_y = 20

# setup window
curses.initscr()
win = curses.newwin(border_y, border_x, 0, 0)  # y, x
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)  # -1


for b in range(border_y):
    win.addstr(b, 0, '💀')

# snake and food
snake_sign = '*'
food_sign = ['🎁', '🎄', '🌟']

snake = [(10, 10), (10, 9), (10, 8)]
food = (randint(1, border_y - 2), randint(0, border_x - 2))

win.addch(food[0], food[1], choice(food_sign))

# game logic
score = 0

ESC = 27
key = curses.KEY_RIGHT

while key != ESC:
    win.addstr(0, 2, f'🥧 Pirate score = {score} 💀️')

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC] or (key in [curses.KEY_LEFT, curses.KEY_RIGHT] and prev_key in [curses.KEY_LEFT, curses.KEY_RIGHT]) or (key in [curses.KEY_UP, curses.KEY_DOWN] and prev_key in [curses.KEY_UP, curses.KEY_DOWN]):
        key = prev_key

    # calculate the next coordinates
    y = snake[0][0]
    x = snake[0][1]

    prev_y, prev_x = y, x

    if key == curses.KEY_DOWN:
        y += 1
        win.timeout(250 - (len(snake) // 2 + len(snake)))  # increase speed)
    if key == curses.KEY_UP:
        y -= 1
        win.timeout(250 - (len(snake) // 2 + len(snake)))  # increase speed)
    if key == curses.KEY_RIGHT:
        x += 1
        win.timeout(int(150 - (len(snake)/5 + len(snake)/10)))  # increase speed
    if key == curses.KEY_LEFT:
        x -= 1
        win.timeout(int(150 - (len(snake)/5 + len(snake)/10)))  # increase speed

    snake.insert(0, (y, x))  # append 0(n)

    # check if we hit the border
    if y == 0:
        break
    if y == border_y - 1:
        break
    if x == 0:
        break
    if x == border_x - 1:
        break

    # if snake runs over itself
    if snake[0] in snake[1:]:
        break

    # eat the food
    if snake[0] == food:
        score += 1
        food = ()
        while food == ():
            food = (randint(1, border_y - 2), randint(0, border_x - 2))
            if food in snake:
                food = ()
        sign = choice(food_sign)
        win.addch(food[0], food[1], sign)
    else:
        # move snake
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    win.addch(snake[0][0], snake[0][1], snake_sign)

curses.endwin()
print(f"🥧 Pirate score = {score}")
