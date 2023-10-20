import generatorMaze
from Algorithm import A_Start, BFS

matrix = generatorMaze.Matrix(15,15)
matrix.generate_maze()
matrix.print_matrix()
bfs = A_Start(matrix)
node = bfs()
path = bfs.findPath(node[1])
print(path)