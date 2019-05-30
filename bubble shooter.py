from tkinter import *
from random import randint
from time import sleep, time
from math import sqrt
HEIGHT = 500
WIDTH = 800
HIGH_SCORE_FILENAME = 'high_score.txt'
window = Tk()
window.title('Bellenschieter / Bubble Blaster')
c = Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()

ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
ship_id2 = c.create_oval(0, 0, 30, 30, outline='darkred')
SHIP_R = 15
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)
SHIP_SPD = 10


def move_ship(event):
    key = event.keysym
    if key == 'Up':
        c.move(ship_id, 0, -SHIP_SPD)
        c.move(ship_id2, 0, -SHIP_SPD)
    elif key == 'Down':
        c.move(ship_id, 0, SHIP_SPD)
        c.move(ship_id2, 0, SHIP_SPD)
    elif key == 'Left':
        c.move(ship_id, -SHIP_SPD, 0)
        c.move(ship_id2, -SHIP_SPD, 0)
    elif key == 'Right':
        c.move(ship_id, SHIP_SPD, 0)
        c.move(ship_id2, SHIP_SPD, 0)


c.bind_all('<Key>', move_ship)
bub_id = []
bub_r = []
bub_speed = []
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPD = 10
GAP = 100


def create_bubble():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline='white')
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPD))


def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)


def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2]) / 2
    y = (pos[1] + pos[3]) / 2
    return x, y


def del_bubble(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]


def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)


def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def collision():
    points = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):
            points += (bub_r[bub] + bub_speed[bub])
            del_bubble(bub)
    return points


c.create_text(50, 30, text='TIME', fill='white')
c.create_text(150, 30, text='SCORE', fill='white')
c.create_text(250, 30, text='HIGH SCORE', fill='white')
time_text = c.create_text(50, 50, fill='white')
score_text = c.create_text(150, 50, fill='white')
high_score_text = c.create_text(250, 50, fill='white')


def show_score(score):
    c.itemconfig(score_text, text=str(score))


def show_time(time_left):
    c.itemconfig(time_text, text=str(time_left))


BUB_CHANCE = 10
TIME_LIMIT = 30
BONUS_SCORE = 1000
score = 0


def show_high_score(high_score):
    c.itemconfig(high_score_text, text=str(high_score))


def get_high_score():
    try:
        with open(HIGH_SCORE_FILENAME, 'r') as high_score_file:
            high_score = int(high_score_file.read())
    except FileNotFoundError:
        save_high_score(0)
        high_score = 0

    return high_score


def save_high_score(high_score):
    with open(HIGH_SCORE_FILENAME, 'w') as high_score_file:
        high_score_file.write(str(high_score))


bonus = 0
end = time() + TIME_LIMIT
high_score = get_high_score()
show_high_score(high_score)
try:
    # MAIN GAME LOOP
    while time() < end:
        if randint(1, BUB_CHANCE) == 1:
            create_bubble()
        move_bubbles()
        clean_up_bubs()
        score += collision()
        if int(score / BONUS_SCORE) / 2 > bonus:
            bonus += 1
            end += int(TIME_LIMIT / bonus) / 2 + 5
        show_score(score)
        show_time(int(end - time()))
        window.update()
        sleep(0.01)
finally:
    if score > high_score:
        save_high_score(score)
