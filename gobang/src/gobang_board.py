import numpy as np
from queue import Queue
from collections import defaultdict


class Gobang:
    def __init__(self):
        self.board_size = 19
        self.board = np.zeros((self.board_size, self.board_size))
        self.blank = 0
        self.black = 1
        self.white = 2
        self.directions = [[(-1, 0), (1, 0)], [(0, 1), (0, -1)], [(-1, -1), (1, 1)], [(-1, -1), (1, 1)]]
        self.complete_size = 5
        self.turn = self.black
        self.percentage = {
            self.black: {
                1: 0.9,
                0: 0.7
            },
            self.white: {
                1: 0.1,
                0: 0.3
            }
        }
        self.now_role = {
            self.black: 0,
            self.white: 0
        }

        self.wins = [False, False]
        self.diagonal_size = self.board_size - self.complete_size

    def get_opponent(self, color):
        return self.black if color == self.white else self.white

    def reset_wins(self):
        self.wins = [False, False]

    def reset(self):
        self.__init__()

    def put(self, y, x, strong=None):
        if self.board[y, x] != self.blank:
            return False
        strong = int(strong)
        self.board[y, x] = self.get_stone(strong)
        self.change_turn()

    def is_inside(self, y, x):
        return 0 <= y <= self.board_size - 1 and 0 <= x <= self.board_size - 1

    def change_turn(self):
        self.turn = self.black if self.turn == self.white else self.white

    def check_complete(self, y, x):
        for direction in self.directions:
            t = 1
            for s, t in direction:
                yy, xx = y + s, x + t
                while self.is_inside(yy, xx) and self.board[yy, xx] == self.turn:
                    t += 1
                    yy += s
                    xx += t
            if t > self.complete_size:
                return False
            elif t == self.complete_size:
                return True
        return False

    def change_role(self, strong):
        self.now_role[self.turn] = 1 if strong else 0

    def get_stone(self, strong):
        role = 1 if strong else 0
        return self.percentage[self.turn][role]

    def observe(self):
        self.reset_wins()
        observed_board = self.get_observed_board()
        for i in range(self.board_size):
            self.check_complete_of_line(observed_board[i, :])
        for i in range(self.board_size):
            self.check_complete_of_line(observed_board[:, i])
        for i in range(-self.diagonal_size, self.diagonal_size + 1):
            self.check_complete_of_line(np.diag(observed_board, i))
        flip_observed_board = np.fliplr(observed_board)
        for i in range(-self.diagonal_size, self.diagonal_size + 1):
            self.check_complete_of_line(np.diag(flip_observed_board, i))
        return observed_board

    def check_complete_of_line(self, line):
        queue = Queue()
        dic = defaultdict(int)
        for j in line[:self.complete_size]:
            dic[j] += 1
            queue.put(j)
        if dic[self.black] == self.complete_size:
            self.wins[0] = True
        if dic[self.white] == self.complete_size:
            self.wins[1] = True
        for j in line[self.complete_size:]:
            last = queue.get()
            dic[last] -= 1
            queue.put(j)
            dic[j] += 1
            if dic[self.black] == self.complete_size:
                self.wins[0] = True
            if dic[self.white] == self.complete_size:
                self.wins[1] = True
        return line

    def get_observed_board(self):
        board_copy = self.board.copy()
        where = self.board > 0
        probabilities = self.board[where]
        random_array = np.random.random(probabilities.size)
        mask1 = probabilities > random_array
        mask2 = probabilities <= random_array
        probabilities[mask1] = self.black
        probabilities[mask2] = self.white
        board_copy[where] = probabilities
        return board_copy.astype(int)
