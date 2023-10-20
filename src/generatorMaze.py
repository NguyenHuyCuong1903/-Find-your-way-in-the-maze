import random

class Matrix:
    def __init__(self, row, col):
        self.rows = row
        self.cols = col
        self.matrix = [[1 for i in range(col)] for j in range(row)]
        self.start = None
        self.end = None
        self.visited = {}
        self.cell = 0
        for i in range(row):
            for j in range(col):
                if i%2 and j%2:
                    self.matrix[i][j] = 0
                    self.visited[(i, j)] = False
                    self.cell += 1

    def check_cell(self, i, j):
        if not (i<0 or i>=self.rows or j<0 or j>=self.cols):
            if i%2 and j%2:
                return (i, j)
        return False
    
    def check_neighbors(self, x, y):
        neighbors = []
        top = self.check_cell(x, y - 2)
        right = self.check_cell(x + 2, y)
        bottom = self.check_cell(x, y + 2)
        left = self.check_cell(x - 2, y)
        if top and not self.visited[top]:
            neighbors.append(top)
        if right and not self.visited[right]:
            neighbors.append(right)
        if bottom and not self.visited[bottom]:
            neighbors.append(bottom)
        if left and not self.visited[left]:
            neighbors.append(left)
        return random.choice(neighbors) if neighbors else False


    def remove_walls(self, current, next):
        i_current, j_current = current[0], current[1]
        i_next, j_next = next[0], next[1]
        # remove wall top
        if i_next == i_current-2:
            self.matrix[i_current-1][j_current] = 0
        # remove wall bottom
        if i_next == i_current+2:
            self.matrix[i_current+1][j_current] = 0
        # remove wall left
        if j_next == j_current-2:
            self.matrix[i_current][j_current-1] = 0
        # remove wall right
        if j_next == j_current+2:
            self.matrix[i_current][j_current+1] = 0

    def generate_maze(self):
        # current_cell = self.matrix[1][1]
        x_start = random.randint(1, self.rows-1)
        y_start = random.randint(1, self.cols-1)
        if x_start%2 == 0:
            x_start -= 1
        if y_start%2 == 0:
            y_start -= 1
        current_cell = (1,1)
        array = []
        break_count = 1

        while break_count != self.cell:
            self.visited[current_cell] = True
            next_cell = self.check_neighbors(current_cell[0], current_cell[1])
            if next_cell:
                self.visited[next_cell] = True
                break_count += 1
                array.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
                # current_cell = random.choice(array)
        x_end = random.randint(1, self.rows-1)
        y_end = random.randint(1, self.cols-1)
        while self.matrix[x_end][y_end] == 1 or (x_start == x_end and y_start == y_end):
            x_end = random.randint(1, self.rows-1)
            y_end = random.randint(1, self.cols-1)
        self.matrix[x_start][y_start] = 2
        self.matrix[x_end][y_end] = 3
        self.start = (x_start, y_start)
        self.end = (x_end, y_end)
        return [(x_start, y_start), (x_end, y_end)]


    def print_matrix(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.matrix[i][j], end=' ')
            print('\n')

def Create():
    m = Matrix(9,9)
    m.generate_maze()
    m.print_matrix()
