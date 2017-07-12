import random, time, queue
from tkinter import *

colors = ["#FFFFFF", "#000000", "#C0C0C0", "#FF0000", "#9C661F", "#B03060", "#FF00FF", "#FF9912",
          "#5E2612", "#0000FF", "#1E90FF", "#00C78C", "#7CFC00",]
size = 30
border = size // 8
pos = (0, 0)
d = [[-1, 0], [0, -1], [1, 0], [0, 1]]


class GameGrid(object):
    def __init__(self, row, col, colors):
        self.row = row
        self.col = col
        self.colors = colors
        self.matrix = [[0 for i in range(col)] for j in range(row)]
        self.chosen = None
        self.highlighted = None
        self.q = queue.Queue()
    '''
    def print(self):
        for row in range(self.row):
            for col in range(self.col):
                print("%2d" % (self.matrix[row][col],), end=" ")
            print()
    '''
    def is_full(self):
        for row in range(self.row):
            for col in range(self.col):
                if self.matrix[row][col] == 0:
                    return False
        return True

    def generate(self):
        for color in range(1, self.colors + 1):
            color_num = 0
            while color_num < self.row * self.col / self.colors and not self.is_full():
                random_row = random.randint(0, self.row - 1)
                random_col = random.randint(0, self.col - 1)
                if self.matrix[random_row][random_col] == 0:
                    self.matrix[random_row][random_col] = color
                    color_num += 1

    def get_pos(self, x, y):
        x0 = x * (size + border) + border
        y0 = y * (size + border) + border
        x1 = x0 + size
        y1 = y0 + size
        return x0, y0, x1, y1

    def get_color(self, x, y):
        return colors[self.matrix[y][x]]

    def get_size(self):
        return self.row * (size + border) + border, self.col * (size + border) + border

    def call_back(self, event):
        col = event.x // (size + border)
        row = event.y // (size + border)
        if event.x < (size + border) * col + border or event.y < (size + border) * row + border or col < 0 or row < 0 \
                or col >= self.col or row >= self.row:
            return
        color = self.get_color(col, row)
        if color == "#FFFFFF":
            return
        self.highlight(row, col)
        if self.chosen is None or self.chosen == (row, col):
            self.chosen = (row, col)
        else:
            original_row, original_col = self.chosen
            self.chosen = (row, col)
            original_color = self.get_color(original_col, original_row)
            color = self.get_color(col, row)
            if original_color != color:
                return
            #self.dfs(original_row, original_col, original_row, original_col, row, col, color,
            #         [(original_row, original_col)], 0, None, 0)
            self.q.queue.clear()
            self.q.put((original_row, original_col, [(original_row, original_col)], 0, None, 0))
            self.bfs(original_row, original_col, row, col, color)

    def draw(self):
        for row in range(self.row):
            for col in range(self.col):
                x0, y0, x1, y1 = self.get_pos(col, row)
                color = self.get_color(col, row)
                w.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    def draw_line(self, used):
        for i in range(len(used) - 1):
            begin_row, begin_col = used[i]
            end_row, end_col = used[i + 1]
            print((begin_row, begin_col), (end_row, end_col))
            x0, y0, x1, y1 = self.get_pos(begin_col, begin_row)
            x2, y2, x3, y3 = self.get_pos(end_col, end_row)
            print((x0+x1)/2, (y0+y1)/2, (x2+x3)/2, (y2+y3)/2)
            w.create_line((x0+x1)/2, (y0+y1)/2, (x2+x3)/2, (y2+y3)/2, fill="red", width=10)
            w.after(1000)
        for i in range(len(used) - 1):
            begin_row, begin_col = used[i]
            end_row, end_col = used[i + 1]
            print((begin_row, begin_col), (end_row, end_col))
            x0, y0, x1, y1 = self.get_pos(begin_col, begin_row)
            x2, y2, x3, y3 = self.get_pos(end_col, end_row)
            print((x0+x1)/2, (y0+y1)/2, (x2+x3)/2, (y2+y3)/2)
            w.create_line((x0+x1)/2, (y0+y1)/2, (x2+x3)/2, (y2+y3)/2, fill="white", width=10)

    def highlight(self, row, col):
        if self.highlighted is not None:
            highlighted_row, highlighted_col = self.highlighted
            x0, y0, x1, y1 = self.get_pos(highlighted_col, highlighted_row)
            highlighted_color = self.get_color(highlighted_col, highlighted_row)
            w.create_rectangle(x0, y0, x1, y1, fill=highlighted_color, outline=highlighted_color)
        x2, y2, x3, y3 = self.get_pos(col, row)
        color = self.get_color(col, row)
        w.create_rectangle(x2, y2, x3, y3, fill=color, outline="#FFFFFF", dash=(10, 10))
        self.highlighted = (row, col)

    def erase(self, original_row, original_col, target_row, target_col):
        self.matrix[original_row][original_col] = 0
        self.matrix[target_row][target_col] = 0
        x0, y0, x1, y1 = self.get_pos(original_col, original_row)
        original_color = self.get_color(original_col, original_row)
        w.create_rectangle(x0, y0, x1, y1, fill=original_color, outline=original_color)
        x2, y2, x3, y3 = self.get_pos(target_col, target_row)
        target_color = self.get_color(target_col, target_row)
        w.create_rectangle(x2, y2, x3, y3, fill=target_color, outline=target_color)

    def dfs(self, row, col, original_row, original_col, target_row, target_col, target_color, used, depth, last_pos,
            turns):
        if turns > 3:
            return
        for d_row, d_col in d:
            if (row + d_row, col + d_col) in used:
                continue
            if row + d_row < -1 or row + d_row > self.row or col + d_col < -1 or col + d_col > self.col:
                continue
            if 0 <= row + d_row <= self.row - 1 and 0 <= col + d_col <= self.col - 1:
                color = self.get_color(col + d_col, row + d_row)
                if color != "#FFFFFF" and color != target_color:
                    continue
                elif color == "#FFFFFF":
                    used.append((row + d_row, col + d_col))
                    last_pos_bak = last_pos
                    if (d_row, d_col) != last_pos:
                        turns += 1
                    last_pos = (d_row, d_col)
                    self.dfs(row + d_row, col + d_col, original_row, original_col, target_row, target_col, target_color,
                             used, depth + 1, last_pos, turns)
                    used.pop()
                    if last_pos_bak != last_pos:
                        last_pos = last_pos_bak
                        turns -= 1
                elif color == target_color and row + d_row == target_row and col + d_col == target_col:
                    if (d_row, d_col) != last_pos and turns > 2:
                        return
                    used.append((target_row, target_col))
                    self.erase(original_row, original_col, target_row, target_col)
                    #self.draw_line(used)
                    #print(used)
                    self.chosen = None
            if row + d_row == -1 or row + d_row == self.row or col + d_col == -1 or col + d_col == self.col:
                used.append((row + d_row, col + d_col))
                last_pos_bak = last_pos
                if (d_row, d_col) != last_pos:
                    turns += 1
                last_pos = (d_row, d_col)
                self.dfs(row + d_row, col + d_col, original_row, original_col, target_row, target_col, target_color,
                         used, depth + 1, last_pos, turns)
                used.pop()
                if last_pos_bak != last_pos:
                    last_pos = last_pos_bak
                    turns -= 1
    #Although DFS is somehow a little faster than BFS, it has many disadvantages and I am considering of removing
    #it in the future editions.
    def bfs(self, original_row, original_col, target_row, target_col, target_color):
        found = False
        while not self.q.empty() and not found:
            row, col, used, depth, last_pos, turns = self.q.get()
            if used == [(3, 1), (3, 2), (3, 3), (2, 3)]:
                print("Searching...")
            if turns > 3:
                continue
            for d_row, d_col in d:
                if (row + d_row, col + d_col) in used:
                    continue
                elif row + d_row < -1 or row + d_row > self.row or col + d_col < -1 or col + d_col > self.col:
                    continue
                elif 0 <= row + d_row <= self.row - 1 and 0 <= col + d_col <= self.col - 1:
                    color = self.get_color(col + d_col, row + d_row)
                    if color != "#FFFFFF" and color != target_color:
                        continue
                    elif color == "#FFFFFF":
                        used.append((row + d_row, col + d_col))
                        if used == [(3, 1), (3, 2), (3, 3), (2, 3)]:
                            print("used found")
                        #print(used)
                        last_pos_bak = last_pos
                        if (d_row, d_col) != last_pos:
                            turns += 1
                        last_pos = (d_row, d_col)
                        self.q.put((row+d_row, col+d_col, used[:], depth+1, last_pos, turns))
                        used.pop()
                        if last_pos_bak != last_pos:
                            last_pos = last_pos_bak
                            turns -= 1
                    elif color == target_color and row + d_row == target_row and col + d_col == target_col:
                        if (d_row, d_col) != last_pos and turns > 2:
                            continue
                        used.append((target_row, target_col))
                        self.erase(original_row, original_col, target_row, target_col)
                        # self.draw_line(used)
                        # print(used)
                        self.chosen = None
                        found = True
                        break
                elif row + d_row == -1 or row + d_row == self.row or col + d_col == -1 or col + d_col == self.col:
                    used.append((row + d_row, col + d_col))
                    if used == [(3, 1), (3, 2), (3, 3), (2, 3)]:
                        print("used found")
                    #print(used)
                    last_pos_bak = last_pos
                    if (d_row, d_col) != last_pos:
                        turns += 1
                    last_pos = (d_row, d_col)
                    self.q.put((row + d_row, col + d_col, used[:], depth + 1, last_pos, turns))
                    used.pop()
                    if last_pos_bak != last_pos:
                        last_pos = last_pos_bak
                        turns -= 1



game_grid = GameGrid(16, 24, len(colors) - 1)
#game_grid = GameGrid(4, 4, 1)
game_grid.generate()
#game_grid.print()
height, width = game_grid.get_size()
root = Tk()
root.title("连连看")
w = Canvas(root, width=width, height=height, background="white")
w.pack()
w.bind_all("<Button-1>", game_grid.call_back)
game_grid.draw()
mainloop()
