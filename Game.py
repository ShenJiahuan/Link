import random
import queue
from Draw import *


class Game(object):
    size = 30
    border = size // 8
    offset = size
    pos = (0, 0)
    d = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    colors = ["#FFFFFF", "#000000", "#C0C0C0", "#FF0000", "#9C661F", "#B03060", "#FF00FF", "#FF9912",
              "#5E2612", "#0000FF", "#1E90FF", "#00C78C", "#7CFC00", ]

    def __init__(self, row, col):
        self.row, self.col = row, col
        self.color_num = len(Game.colors) - 1
        self.matrix = [[0 for _ in range(col)] for _ in range(row)]
        self.chosen = None
        self.highlighted = None
        self.q = queue.Queue()
        self.generate()
        self.height, self.width = self.get_size()
        self.drawer = Draw(self, row, col)
        self.drawer.draw()

    def play(self):
        self.drawer.play()

    def is_full(self):
        return len([1 for row in range(self.row) for col in range(self.col) if self.matrix[row][col] == 0]) == 0

    def is_empty(self):
        return len([1 for row in range(self.row) for col in range(self.col) if self.matrix[row][col] != 0]) == 0

    def generate(self):
        for color in range(1, self.color_num + 1):
            count = 0
            while count < int(self.row * self.col / self.color_num) and not self.is_full():
                random_row, random_col =  random.randint(0, self.row - 1), random.randint(0, self.col - 1)
                if self.matrix[random_row][random_col] == 0:
                    self.matrix[random_row][random_col] = color
                    count += 1

    @staticmethod
    def get_pos(x, y):
        x0, y0 = [_ * (Game.size + Game.border) + Game.border + Game.offset for _ in [x, y]]
        x1, y1 = [_ + Game.size for _ in [x0, y0]]
        return x0, y0, x1, y1

    def get_color(self, x, y):
        return Game.colors[self.matrix[y][x]]

    def get_size(self):
        return [_ * (Game.size + Game.border) + Game.border + Game.offset * 2 for _ in [self.row, self.col]]

    @staticmethod
    def get_coordinate(event):
        return [(_ - Game.offset) // (Game.size + Game.border) for _ in [event.y, event.x]]

    def point_outside_grid(self, event, point):
        row, col = point
        if event.x < (Game.size + Game.border) * col + Game.border \
                or event.y < (Game.size + Game.border) * row + Game.border:
            return True
        if col < 0 or row < 0 or col >= self.col or row >= self.row:
            return True

    def call_back(self, event):
        row, col = self.get_coordinate(event)
        if self.point_outside_grid(event, [row, col]):
            return
        color = self.get_color(col, row)
        if color == "#FFFFFF":
            return
        self.drawer.highlight([row, col])
        self.highlighted = (row, col)
        if self.chosen is None or self.chosen == (row, col):
            self.chosen = (row, col)
        else:
            original_row, original_col = self.chosen
            self.chosen = (row, col)
            original_color = self.get_color(original_col, original_row)
            color = self.get_color(col, row)
            if original_color != color:
                return
            self.q.queue.clear()
            self.q.put((original_row, original_col, [(original_row, original_col)], None, 0))
            self.bfs((original_row, original_col), ((row, col), color))

    def step_result(self, q_elem, target_info, d):
        row, col, used, last_pos, turns = q_elem
        target_point, target_color = target_info
        target_row, target_col = target_point
        d_row, d_col = d
        new_row, new_col = row + d_row, col + d_col
        if (new_row, new_col) in used:
            return 0
        if new_row < -1 or new_row > self.row or new_col < -1 or new_col > self.col:
            return 0
        if 0 <= new_row <= self.row - 1 and 0 <= new_col <= self.col - 1:
            color = self.get_color(new_col, new_row)
            if color != "#FFFFFF" and color != target_color:
                return 0
            if color != "#FFFFFF" and (new_row, new_col) != (target_row, target_col):
                return 0
            if color == "#FFFFFF":
                return 1
            elif (new_row, new_col) == (target_row, target_col) and (d_row, d_col) != last_pos and turns > 2:
                return 0
            elif (new_row, new_col) == (target_row, target_col) and ((d_row, d_col) == last_pos or turns <= 2):
                return 2
        else:
            return 1

    def bfs(self, original_point, target_info):
        original_row, original_col = original_point
        target_point, target_color = target_info
        target_row, target_col = target_point
        while not self.q.empty():
            row, col, used, last_pos, turns = q_elem = self.q.get()
            if turns > 3:
                continue

            finish_d = list(filter(lambda d: self.step_result(q_elem, (target_point, target_color), d) == 2, self.d))
            if len(finish_d) != 0:
                d_row, d_col = finish_d[0]
                new_row, new_col = row + d_row, col + d_col
                used.append((new_row, new_col))
                self.drawer.erase((original_row, original_col), (target_row, target_col))
                self.drawer.draw_line(used)
                if self.is_empty():
                    self.drawer.congratulations()
                self.chosen = None
                return

            step_d = list(filter(lambda d: self.step_result(q_elem, (target_point, target_color), d) == 1, self.d))
            for d_row, d_col in step_d:
                new_row, new_col = row + d_row, col + d_col
                used.append((new_row, new_col))
                last_pos_bak = last_pos
                if (d_row, d_col) != last_pos:
                    turns += 1
                last_pos = (d_row, d_col)
                self.q.put((new_row, new_col, used[:], last_pos, turns))
                used.pop()
                if last_pos_bak != last_pos:
                    last_pos = last_pos_bak
                    turns -= 1

