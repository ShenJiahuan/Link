from tkinter import *


class Draw(object):
    def __init__(self, game, row, col):
        self.row = row
        self.col = col
        self.game = game
        self.root = Tk()
        self.root.title("连连看")
        self.w = Canvas(self.root, width=game.width, height=game.height, background="white")
        self.w.pack()
        self.w.bind_all("<Button-1>", game.call_back)

    def draw(self):
        for row in range(self.row):
            for col in range(self.col):
                x0, y0, x1, y1 = self.game.get_pos(col, row)
                color = self.game.get_color(col, row)
                self.w.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    @staticmethod
    def _mean(x, y):
        return (x + y) / 2

    def draw_line(self, used):
        for i in range(len(used) - 1):
            begin_row, begin_col = used[i]
            end_row, end_col = used[i + 1]
            x0, y0, x1, y1 = self.game.get_pos(begin_col, begin_row)
            x2, y2, x3, y3 = self.game.get_pos(end_col, end_row)
            self.w.create_line(self._mean(x0, x1), self._mean(y0, y1), self._mean(x2, x3), self._mean(y2, y3),
                               fill="red", width=2)
            self.w.after(300, self.erase_line, used)

    def erase_line(self, used):
        for i in range(len(used) - 1):
            begin_row, begin_col = used[i]
            end_row, end_col = used[i + 1]
            x0, y0, x1, y1 = self.game.get_pos(begin_col, begin_row)
            x2, y2, x3, y3 = self.game.get_pos(end_col, end_row)
            self.w.create_line(self._mean(x0, x1), self._mean(y0, y1), self._mean(x2, x3), self._mean(y2, y3),
                               fill="white", width=2)

    def highlight(self, point):
        row, col = point
        if self.game.highlighted is not None:
            highlighted_row, highlighted_col = self.game.highlighted
            x0, y0, x1, y1 = self.game.get_pos(highlighted_col, highlighted_row)
            highlighted_color = self.game.get_color(highlighted_col, highlighted_row)
            self.w.create_rectangle(x0, y0, x1, y1, fill=highlighted_color, outline=highlighted_color)
        x2, y2, x3, y3 = self.game.get_pos(col, row)
        color = self.game.get_color(col, row)
        self.w.create_rectangle(x2, y2, x3, y3, fill=color, outline="#FFFFFF", dash=(10, 10))

    def erase(self, original_point, target_point):
        original_row, original_col = original_point
        target_row, target_col = target_point
        self.game.matrix[original_row][original_col] = 0
        self.game.matrix[target_row][target_col] = 0
        x0, y0, x1, y1 = self.game.get_pos(original_col, original_row)
        original_color = self.game.get_color(original_col, original_row)
        self.w.create_rectangle(x0, y0, x1, y1, fill=original_color, outline=original_color)
        x2, y2, x3, y3 = self.game.get_pos(target_col, target_row)
        target_color = self.game.get_color(target_col, target_row)
        self.w.create_rectangle(x2, y2, x3, y3, fill=target_color, outline=target_color)

    def congratulations(self):
        self.w.delete("all")
        label = Label(self.root, text="恭喜你，通关啦！")
        label.pack()

    @staticmethod
    def play():
        mainloop()
