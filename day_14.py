from collections import defaultdict
from dataclasses import dataclass
from enum import auto, Enum
import re
import numpy as np
from time import sleep
from typing import Optional

SECONDS = 100
# WIDTH, HEIGHT = 11, 7
WIDTH, HEIGHT = 101, 103

SIZE = np.array((WIDTH, HEIGHT))

MID_COL = np.int64((WIDTH - 1)/ 2 )
MID_ROW = np.int64((HEIGHT - 1) / 2)

ROBOT_PATTERN = r"p=(?P<p_x>[\-]{0,1}\d+),(?P<p_y>[\-]{0,1}\d+) v=(?P<v_x>[\-]{0,1}\d+),(?P<v_y>[\-]{0,1}\d+)"

class Quadrant(Enum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()

@dataclass
class Robot:
    pos: np.ndarray
    vec: np.ndarray

    def move(self, seconds: int = 1):
        self.pos = self.pos + self.vec * seconds
        self.pos = np.remainder(self.pos, SIZE)

    def quadrant(self) -> Optional[Quadrant]:
        if self.pos[0] == MID_COL:
            return
        
        if self.pos[1] == MID_ROW:
            return

        if self.pos[0] < MID_COL:
            if self.pos[1] < MID_ROW:
                return Quadrant.TOP_LEFT
            else:
                return Quadrant.BOTTOM_LEFT
        elif self.pos[1] < MID_ROW:
            return Quadrant.TOP_RIGHT
        else:
            return Quadrant.BOTTOM_RIGHT

robots: list[Robot] = []

with open("day_14.txt", "r") as f:
    for bot_str in f.readlines():
        m = re.search(ROBOT_PATTERN, bot_str)
        assert m

        robots.append(Robot(
            np.array((int(m.group("p_x")), int(m.group("p_y")))),
            np.array((int(m.group("v_x")), int(m.group("v_y"))))
        ))

for sec in range(SECONDS):
    for bot in robots:
        bot.move()

quadrant_counts: dict[Quadrant, int] = defaultdict(int)
for bot in robots:
    quadrant = bot.quadrant()
    if quadrant:
        quadrant_counts[quadrant] += 1

safety_factor = 1
for count in quadrant_counts.values():
    safety_factor *= count

print(safety_factor)


from matplotlib import animation, pyplot as plt

START = 14  # 84 - 33
INCREMENT = 101  # 101 - 103

mat = np.zeros((HEIGHT, WIDTH, 3))
for bot in robots:
    bot.move(START)
    mat[bot.pos[1]][bot.pos[0]] = [255, 0, 0]

seconds = START

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

img = ax.imshow(mat.astype("uint8"), animated=True)
# comp = np.load("mat.npy")[26:59, 37:68, :]

lowest = np.int64(9999999)

def update_img(i):
    global seconds
    global lowest

    mat = np.zeros((HEIGHT, WIDTH, 3))
    for bot in robots:
        bot.move(INCREMENT)
        mat[bot.pos[1]][bot.pos[0]] = [np.int64(255), np.int64(0), np.int64(0)]

    # diff = np.abs(np.sum(np.subtract(mat[26:59, 37:68, :], comp)))
    seconds += INCREMENT

    # if diff <= lowest:
    #     lowest = diff
    #     print(f"Seconds {seconds} - {diff}")

    plt.title(f"Seconds: {seconds}")
    img.set_array(mat.astype("uint8"))

    # if seconds == 7828:
    #     np.save("mat.npy", mat)
    #     plt.savefig("my.png")
    
    
# 7861
# 7286

ani = animation.FuncAnimation(fig, update_img, interval=1, save_count=200)
# plt.show()
video_writer = animation.FFMpegWriter(fps=1)
ani.save('animation.mp4', writer = video_writer)