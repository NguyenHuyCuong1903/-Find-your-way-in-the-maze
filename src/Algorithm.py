from generatorMaze import *
from math import fabs
from queue import PriorityQueue

class BFS:
    def __init__(self, maze: Matrix):
        self.maze = maze
    
    def listAction(self, Node):
        Act = []
        if self.maze.matrix[Node[0][0]-1][Node[0][1]] != 1: #len
            Act.append(((Node[0][0]-1, Node[0][1]), Node[1]))
        if self.maze.matrix[Node[0][0]+1][Node[0][1]] != 1: #xuong
            Act.append(((Node[0][0]+1, Node[0][1]), Node[1]))
        if self.maze.matrix[Node[0][0]][Node[0][1]-1] != 1: #trai
            Act.append(((Node[0][0], Node[0][1]-1), Node[1]))
        if self.maze.matrix[Node[0][0]][Node[0][1]+1] != 1: #phai
            Act.append(((Node[0][0], Node[0][1]+1), Node[1]))
        return Act

    def checkGoal(self, Node):
        return self.maze.end == Node[0]

    def checkinOpenorClose(self, Node):
        for node in self.Open:
            if node[0] == Node[0]:
                return True
        for node in self.Close:
            if node[0] == Node[0]:
                return True
        return False

    def findPath(self, pos):
        path = []
        while self.parent[pos] != None:
            path.append(pos)
            pos = self.parent[pos]
        path.append(pos)
        return path

    def __call__(self):
        Node = (self.maze.start, None)  # Node((x, y), parent)
        self.Open = []
        self.visited = []
        self.visiting = []
        self.Close = []
        self.parent = dict()
        self.parent[Node[0]] = None
        self.Open.append(Node)
        while len(self.Open) != 0:
            Node = self.Open.pop(0)
            # self.visited.append(Node[0])
            self.Close.append(Node)
            if self.checkGoal(Node):
                return Node
            for state in self.listAction(Node):
                if self.checkinOpenorClose(state):
                    continue
                self.Open.append(state)
                self.visited.append(state[0])
                self.parent[state[0]] = Node[0]
        return None
    
class DFS:
    def __init__(self, maze: Matrix):
        self.maze = maze
    
    def listAction(self, Node):
        Act = []
        if self.maze.matrix[Node[0][0]-1][Node[0][1]] != 1: #len
            Act.append(((Node[0][0]-1, Node[0][1]), Node[1]))
        if self.maze.matrix[Node[0][0]+1][Node[0][1]] != 1: #xuong
            Act.append(((Node[0][0]+1, Node[0][1]), Node[1]))
        if self.maze.matrix[Node[0][0]][Node[0][1]-1] != 1: #trai
            Act.append(((Node[0][0], Node[0][1]-1), Node[1]))
        if self.maze.matrix[Node[0][0]][Node[0][1]+1] != 1: #phai
            Act.append(((Node[0][0], Node[0][1]+1), Node[1]))
        return Act

    def checkGoal(self, Node):
        return self.maze.end == Node[0]

    def checkinOpenorClose(self, Node):
        for node in self.Open:
            if node[0] == Node[0]:
                return True
        for node in self.Close:
            if node[0] == Node[0]:
                return True
        return False

    def findPath(self, pos):
        path = []
        while self.parent[pos] != None:
            path.append(pos)
            pos = self.parent[pos]
        path.append(pos)
        return path

    def __call__(self):
        Node = (self.maze.start, None)  # Node((x, y), parent)
        self.Open = []
        self.visited = []
        self.Close = []
        self.parent = dict()
        self.parent[Node[0]] = None
        self.Open.append(Node)
        while len(self.Open) != 0:
            Node = self.Open.pop()
            # self.visited.append(Node[0])
            self.Close.append(Node)
            if self.checkGoal(Node):
                return Node
            for state in self.listAction(Node):
                if self.checkinOpenorClose(state):
                    continue
                self.Open.append(state)
                self.visited.append(state[0])
                self.parent[state[0]] = Node[0]
        return None


class A_Star:
    def __init__(self, maze: Matrix):
        self.maze = maze
    
    def listAction(self, Node):
        Act = []
        if self.maze.matrix[Node[1][0]-1][Node[1][1]] != 1: #len
            Act.append(((Node[1][0]-1, Node[1][1]), Node[2]))
        if self.maze.matrix[Node[1][0]+1][Node[1][1]] != 1: #xuong
            Act.append(((Node[1][0]+1, Node[1][1]), Node[2]))
        if self.maze.matrix[Node[1][0]][Node[1][1]-1] != 1: #trai
            Act.append(((Node[1][0], Node[1][1]-1), Node[2]))
        if self.maze.matrix[Node[1][0]][Node[1][1]+1] != 1: #phai
            Act.append(((Node[1][0], Node[1][1]+1), Node[2]))
        return Act

    def checkGoal(self, Node):
        return self.maze.end == Node[1]

    def checkinOpenorClose(self, Node):
        for node in self.Open:
            if node[1] == Node[1]:
                return True
        for node in self.Close:
            if node[1] == Node[1]:
                return True
        return False

    def heuristic(Node1, Node2): # (x,y)
        return fabs(Node1[0]-Node2[0]) + fabs(Node1[1]-Node2[1])

    def findPath(self, pos):
        path = []
        while self.parent[pos] != None:
            path.append(pos)
            pos = self.parent[pos]
        path.append(pos)
        return path

    def __call__(self):
        queue = PriorityQueue()
        Node = (0, self.maze.start, None)  # Node(f, (x, y), parent)
        queue.put(Node)
        f = {}
        g = {}
        g[self.maze.start] = 0
        f[self.maze.start] = A_Star.heuristic(self.maze.start, self.maze.end)
        self.CheckOpen = {self.maze.start}
        self.visited = []
        self.visiting = []
        self.Close = dict()
        self.parent = dict()
        self.parent[Node[1]] = None
        
        while not queue.empty():
            current = queue.get()  #(f, (x, y), parent)
            self.CheckOpen.remove(current[1])
            # self.visited.append(Node[0])
            
            if self.checkGoal(current):
                return current
            self.Close[current[1]] = (current[0], current[2])  # (f, parent)
        
            for state in self.listAction(current):   # ((x, y), parent)
                if state[0] ==  current[2]:
                    continue
                if state[0] in self.CheckOpen:
                    if g[state[0]] > g[current[1]] + 1:
                        g[state[0]] = g[current[1]] + 1
                        f[state[0]] = g[state[0]] + A_Star.heuristic(state[0], self.maze.end)
                        self.parent[state[0]] = current[1]
                        queue.put((f[state[0]], state[0], current[1]))
                        self.visited.append(state[0])
                if state[0] not in self.CheckOpen:
                    g[state[0]] = g[current[1]] + 1
                    f[state[0]] = g[state[0]] + A_Star.heuristic(state[0], self.maze.end)
                    self.parent[state[0]] = current[1]
                    queue.put((f[state[0]], state[0], current[1]))
                    self.CheckOpen.add(state[0])
                    self.visited.append(state[0])
                if state[0] in self.Close.keys():
                    if g[state[0]] > g[current[1]] + 1:
                        q = self.Close.pop(state[0])
                        queue.put(q[0], state[0], q[1])
                        self.CheckOpen.add(state[0])
                        self.visited.append(state[0])
        return None