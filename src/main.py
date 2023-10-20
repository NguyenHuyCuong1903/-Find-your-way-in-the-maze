from pygame.locals import *
import pygame, sys
import time
import random
from Algorithm import BFS, DFS, A_Star
from generatorMaze import Matrix

SCR_WIDTH = 1400
SCR_HEIGHT = 1000
HEADER = 100
MAZE_WIDTH = 900
MAZE_HEIGHT = 900
MENU_WIDTH = SCR_WIDTH - MAZE_WIDTH
MENU_HEIGHT = SCR_HEIGHT - MAZE_HEIGHT
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 70
WHITE =     (255, 255, 255)
BLACK =     ( 32,  32,  32)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
VISITED =   (51, 51, 255)
TEXTCOLOR = (  0,   0,  0)
BGCOLOR = (160, 160, 160)
COLOR_CELL = (224, 224, 224)
COLOR_CLICK = (0,0,0)
COLOR_OVER = GREEN
COLOR_BUTTON = BLUE

pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption("Game Maze Rabbit")
pygame.display.update()
clock = pygame.time.Clock()


def font(size):
    font = pygame.font.SysFont('Arial', size)
    return font

########################################################################################################

########################################################################################################

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.changed_color = False
        self.img = pygame.image.load('./Picture/wall1.png')
        self.surface = pygame.transform.scale(self.img, (self.size, self.size))

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        
    
    def resetColor(self):
        # if self.changed_color == True:
            
            self.changed_color = False
            if (int(self.x // self.size) + int((self.y - HEADER) // self.size)) % 2 == 0:
                self.color = WHITE
            else:
                self.color = COLOR_CELL
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
    def cell_wall(self):
        self.color = BLACK
        self.changed_color = True
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.size, self.size))
        screen.blit(self.surface, (self.x, self.y))
    
    def drawSolution(self):
        pygame.draw.rect(screen, GREEN, (self.x+2, self.y+2, self.size-2, self.size-2))
        pygame.display.update()

    def drawVisited(self):
        pygame.draw.rect(screen, VISITED, (self.x+2, self.y+2, self.size-2, self.size-2))
        pygame.display.update()

    def drawVisiting(self):
        pygame.draw.rect(screen, RED, (self.x+2, self.y+2, self.size-2, self.size-2))
        pygame.display.update()
    
    def is_wall(self):
        return self.color == BLACK


########################################################################################################
class Maze(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super().__init__()
        self.row = row
        self.col = col
        self.totalCell = row*col
        self.matrix = None
        self.size = int(MAZE_WIDTH//row)
        self.start = None
        self.end = None
        self.colorBackground = color
        self.L = [[None for i in range(col)] for j in range(row)]
        self.neighbor = [[None for i in range(col)] for j in range(row)]

    def draw(self, screen):
        self.L = [[None for i in range(self.col)] for j in range(self.row)]
        self.neighbor = [[None for i in range(self.col)] for j in range(self.row)]
        self.background(self.colorBackground)
        self.start = None
        self.end = None
        #draw cell
        for i in range(self.row):
            for j in range(self.col):
                if (i+j)%2==0:
                    cell = Cell(j*self.size, i*self.size + HEADER, self.size, WHITE)
                    self.L[i][j] = cell
                    cell.draw()
                    
                else:
                    cell = Cell(j*self.size, i*self.size + HEADER, self.size, COLOR_CELL)
                    self.L[i][j] = cell
                    self.neighbor[i][j] = cell
                    cell.draw()
        


    def grid(self, screen):
        # draw line maze
        for i in range(1, self.row+1):
            pygame.draw.line(screen, BLACK, (0, i*self.size + HEADER), (MAZE_WIDTH, i*self.size + HEADER) , 2)
            pygame.draw.line(screen, BLACK, (i*self.size, HEADER), (i*self.size, SCR_HEIGHT), 2)

    def background(self, color):
        pygame.draw.rect(screen, color, (0, 0, SCR_WIDTH, SCR_HEIGHT))
        # pygame.display.update()
    def change_click(self, x, y):
        if not (x < 0 or x > MAZE_WIDTH or y < HEADER or y > MAZE_HEIGHT + HEADER):
            i = int((y - HEADER)//self.size)
            j = int((x)//self.size)
            if self.L[i][j].is_wall():
                self.L[i][j].resetColor()
            else:
                self.L[i][j].cell_wall()
    def reset(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.L[i][j].is_wall():
                    self.L[i][j].cell_wall()
                elif self.L[i][j].x == self.start.x and self.L[i][j].y == self.start.y:
                    continue
                else:
                    if (i+j)%2==0 and self.L[i][j] != self.end and self.L[i][j] != self.start:
                        cell = Cell(j*self.size, i*self.size + HEADER, self.size, WHITE)
                        cell.draw()
                    elif (i+j)%2!=0 and self.L[i][j] != self.end and self.L[i][j] != self.start:
                        cell = Cell(j*self.size, i*self.size + HEADER, self.size, COLOR_CELL)
                        cell.draw()
                


    def positionCell(self, x, y):
        if not (x < 0 or x >= MAZE_WIDTH or y < HEADER or y >= MAZE_HEIGHT + HEADER):
            return int((y - HEADER)//self.size)*self.col + int(x//self.size)
        return self.totalCell


########################################################################################################
class RandomMaze(pygame.sprite.Sprite):
    def __init__(self, maze: Maze):
        super().__init__()
        self.maze = maze

    # def enforcement(self):
    #     maze.start = (random.randint(0, int(self.maze.row//2)), random.randint(0, int(self.maze.col//2)))
    #     maze.end = (random.randint(int(self.maze.row//2)+1, self.maze.row-1), random.randint(int(self.maze.col//2)+1, self.maze.col-1))
    #     matrix = random_maze_generator(self.maze.row, self.maze.col, maze.start, maze.end)
    #     for i in range(self.maze.row):
    #         for j in range(self.maze.col):
    #             if matrix[i][j] == 0:
    #                 self.maze.L[i*self.maze.col+j].cell_wall()
    #             if matrix[i][j] == 2:
    #                 self.maze.start = self.maze.L[i*self.maze.col+j]
    #             if matrix[i][j] == 3:
    #                 self.maze.end = self.maze.L[i*self.maze.col+j]
    def enforcement(self):
        m = Matrix(self.maze.row, self.maze.col)
        [(x_start, y_start), (x_end, y_end)] = m.generate_maze()
        self.maze.start = self.maze.L[x_start][y_start]
        self.maze.end = self.maze.L[x_end][y_end]
        self.maze.matrix = m
        for i in range(self.maze.row):
            for j in range(self.maze.col):
                if m.matrix[i][j] == 1:
                    self.maze.L[i][j].cell_wall()
                # if m.matrix[i][j] == 2:
                #     self.maze.start = self.maze.L[i*self.maze.col+j]
                # if m.matrix[i][j] == 3:
                #     self.maze.end = self.maze.L[i*self.maze.col+j]
        m.print_matrix()

########################################################################################################

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.img = pygame.image.load('./Picture/confused.png')
        self.surface = pygame.transform.scale(self.img, (self.size, self.size))
        
    def draw(self):
        screen.blit(self.surface, (self.x, self.y))
    
    def move(self, maze: Maze, type):
        cell = maze.L[(self.y-HEADER)//self.size][self.x//self.size]
        cell.resetColor()
        if type == 'Up':
            self.y -= self.size
            if self.y >= HEADER:
                cell = maze.L[(self.y-HEADER)//self.size][self.x//self.size]
                if cell.is_wall():
                    self.y += self.size
            else:
                self.y += self.size
        if type == 'Down':
            self.y += self.size
            if self.y < MAZE_HEIGHT + HEADER:
                cell = maze.L[(self.y-HEADER)//self.size][self.x//self.size]
                if cell.is_wall():
                    self.y -= self.size
            else:
                self.y -= self.size
        if type == 'Left':
            self.x -= self.size
            if self.x >= 0:
                cell = maze.L[(self.y-HEADER)//self.size][self.x//self.size]
                if cell.is_wall():
                    self.x += self.size
            else:
                self.x += self.size
        if type == 'Right':
            self.x += self.size
            if self.x < MAZE_WIDTH:
                cell = maze.L[(self.y-HEADER)//self.size][self.x//self.size]
                if cell.is_wall():
                    self.x -= self.size
            else:
                self.x -= self.size
        maze.matrix.start = ((self.y-HEADER)//maze.size, self.x//maze.size)
        maze.start = maze.L[(self.y-HEADER)//self.size][self.x//self.size]
        position = maze.positionCell(self.x, self.y)
        # maze.L[position].changed_color = True
        self.draw()

    @classmethod
    def drawPlayer(cls, maze: Maze):
        x_rabbit = maze.start.x
        y_rabbit = maze.start.y
        x_carrot = maze.end.x
        y_carrot = maze.end.y
        # draw rabbit(start)
        rabbit = Player(x_rabbit, y_rabbit, maze.size)
        rabbit.draw()
        # draw carrot(target)
        img = pygame.image.load('./Picture/carrot.png')
        surface = pygame.transform.scale(img, (maze.size, maze.size))
        screen.blit(surface, (x_carrot, y_carrot))
        return rabbit     
        
    def checkGoal(self, maze: Maze):
        return self.x == maze.end.x and self.y == maze.end.y and maze.start != None


########################################################################################################
class Title(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, text, colortext, font, size):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.colorText = colortext
        self.font = font
        self.size = size
    
    def draw(self):
        surface = pygame.Rect(self.x, self.y, self.width, self.height)
        surface.centerx = int((MAZE_WIDTH + SCR_WIDTH)/2)
        self.surface_title = pygame.draw.rect(screen, self.color, (surface.topleft[0], surface.topleft[1], self.width, self.height))
        text = pygame.font.Font.render(pygame.font.SysFont(self.font, self.size), self.text, True, self.colorText)
        surface_text = text.get_rect()
        surface_text.center = surface.center
        screen.blit(text, surface_text)


class Button():
    def __init__(self, x, y, width, height, color, text, colortext = RED, flag = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.colorText = colortext
        self.flag = flag
        self.surface_button = None
    
    def draw(self):
        surface = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.flag:
            surface.centerx = int((MAZE_WIDTH + SCR_WIDTH)/2)
        self.surface_button = pygame.draw.rect(screen, self.color, (surface.topleft[0], surface.topleft[1], self.width, self.height))
        pygame.draw.rect(screen, WHITE, (surface.topleft[0], surface.topleft[1], self.width, self.height), width=5)
        # self.surface_button.centerx = int((MAZE_WIDTH + SCR_WIDTH)/2)
        text = pygame.font.Font.render(font(30), self.text, True, self.colorText)
        surface_text = text.get_rect()
        surface_text.center = surface.center
        screen.blit(text, surface_text)
    
    def over(self):
        x, y = pygame.mouse.get_pos()
        if self.surface_button.collidepoint(x, y):
            self.color = COLOR_OVER
            self.draw()
        else:
            self.color = COLOR_BUTTON
            self.draw()

    def click(self):
        x, y = pygame.mouse.get_pos()
        if self.surface_button.collidepoint(x, y):
            return True
        return False

########################################################################################################

def draw_screen(maze: Maze):
    menu.draw()
    img_header = pygame.image.load('./Picture/img_header.png')
    img_header = pygame.transform.scale(img_header, (MAZE_WIDTH+2, HEADER))
    # img_menu = pygame.image.load('./NLCS_NguyenHuyCuong_B2016949/Picture/background_menu.png')
    # img_menu = pygame.transform.scale(img_menu, (MENU_WIDTH, MAZE_HEIGHT))
    screen.blit(img_header, (0, 0))
    # screen.blit(img_menu, (MAZE_WIDTH, HEADER))
    button_random.draw()
    button_random.over()
    button_reset.draw()
    button_reset.over()
    button_BFS.draw()
    button_BFS.over()
    button_DFS.draw()
    button_DFS.over()
    button_A_star.draw()
    button_A_star.over()
    button_11.draw()
    button_21.draw()
    button_31.draw()
    button_41.draw()
    button_51.draw()
    maze.grid(screen)
    pygame.draw.line(screen, RED, (0, HEADER - 1), (SCR_WIDTH, HEADER - 1), 2)
    pygame.draw.line(screen, RED, (MAZE_WIDTH, 0), (MAZE_WIDTH, SCR_HEIGHT), 2)
    pygame.draw.line(screen, RED, (0, SCR_HEIGHT-2), (SCR_WIDTH, SCR_HEIGHT-2), 2)

########################################################################################################
title_win = Button(0,400, 200, 100, RED, "WIN", WHITE)
menu = Title(MAZE_WIDTH+2, 0, MENU_WIDTH, HEADER, BLUE, 'Menu', WHITE, 'Arial', 80)
button_random = Button(0, 250, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, 'RANDOM')
button_reset = Button(0, 370, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, 'RESET')
button_BFS = Button(0, 490, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, 'BFS')
button_DFS = Button(0, 610, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, 'DFS')
button_A_star = Button(0, 730, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, 'A_star')


button_11 = Button(900, 100, 100, BUTTON_HEIGHT, BLUE, '11', WHITE, flag=False)
button_21 = Button(1000, 100, 100, BUTTON_HEIGHT, BLUE, '21', WHITE, flag=False)
button_31 = Button(1100, 100, 100, BUTTON_HEIGHT, BLUE, '31', WHITE, flag=False)
button_41 = Button(1200, 100, 100, BUTTON_HEIGHT, BLUE, '41', WHITE, flag=False)
button_51 = Button(1300, 100, 100, BUTTON_HEIGHT, BLUE, '51', WHITE, flag=False)
maze = Maze(31, 31, BLACK)
speed = 30

def drawVisit(visited, speed):
    for item in visited:
        pygame.event.pump()
        if item[0] == (maze.end.y-HEADER)//maze.size and item[1] == maze.end.x//maze.size:
            continue
        (i, j) = item
        maze.L[i][j].drawVisiting()
        clock.tick(20)
        maze.L[i][j].drawVisited()

def drawPath(path):
    for item in path:
        pygame.event.pump()
        clock.tick(40)
        (i, j) = item
        maze.L[i][j].drawSolution()

def updateMatrix():
    for i in range(maze.row):
        for j in range(maze.col):
            if maze.L[i][j].is_wall():
                maze.matrix.matrix[i][j] = 1
            else:
                maze.matrix.matrix[i][j] = 0


def main():
    running = True
    global maze
    global speed
    maze.draw(screen)
    player:Player = None
    mouse = False
    move = False
    player_Win = False
    while running:
        clock.tick(60)
        pygame.event.pump()
        for event in pygame.event.get():
            pygame.event.pump()
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            # try:
            #     if player.checkGoal(maze):
            #         player_Win = True
            # except:
            #     pass
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = False
            
            if event.type == pygame.MOUSEMOTION and mouse and not move:
                x, y = pygame.mouse.get_pos()
                try:
                    cell = maze.L[(y-HEADER)//maze.size][x//maze.size].cell_wall()
                    cell.cell_wall()
                except:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                left, _, right = pygame.mouse.get_pressed()
                if not move:
                    mouse = True
                    x, y = pygame.mouse.get_pos()
                    try:
                        maze.change_click(x, y)
                    except:
                        pass
                #----------------------#
                if button_random.click():
                    try:
                        pygame.event.pump()
                        maze.draw(screen)
                        RandomMaze(maze).enforcement()
                        player = Player.drawPlayer(maze)
                    except:
                        pass
                    move = False
                    player_Win = False
                if button_reset.click():
                    # maze.draw(screen)
                    try:
                        maze.reset()
                        move = False
                        player_Win = False
                    except:
                        pass

                if button_BFS.click():
                    try:
                        maze.reset()
                        move = False
                        player_Win = False
                        draw_screen(maze)
                        updateMatrix()
                        bfs = BFS(maze.matrix)
                        Node = bfs()
                        visited = bfs.visited
                        drawVisit(visited, speed)
                        # print(visited)
                        path = bfs.findPath(Node[0])
                        drawPath(path[1:-1])
                    except:
                        pass

                if button_DFS.click():
                    try:
                        maze.reset()
                        move = False
                        player_Win = False
                        draw_screen(maze)
                        updateMatrix()
                        dfs = DFS(maze.matrix)
                        Node = dfs()
                        visited = dfs.visited
                        drawVisit(visited, speed)
                        # print(visited)
                        path = dfs.findPath(Node[0])
                        drawPath(path[1:-1])
                    except:
                        pass
                
                if button_A_star.click():
                    try:
                        maze.reset()
                        move = False
                        player_Win = False
                        draw_screen(maze)
                        updateMatrix()
                        a_star = A_Star(maze.matrix)
                        Node = a_star()
                        visited = a_star.visited
                        drawVisit(visited,speed)
                        # print(visited)
                        path = a_star.findPath(Node[1])
                        drawPath(path[1:-1])
                    except:
                        pass

                if button_11.click():
                    maze = Maze(11, 11, BLACK)
                    draw_screen(maze)
                    maze.draw(screen)
                if button_21.click():
                    maze = Maze(21, 21, BLACK)
                    draw_screen(maze)
                    maze.draw(screen)
                if button_31.click():
                    maze = Maze(31, 31, BLACK)
                    draw_screen(maze)
                    maze.draw(screen)
                if button_41.click():
                    maze = Maze(41, 41, BLACK)
                    draw_screen(maze)
                    maze.draw(screen)
                if button_51.click():
                    maze = Maze(51, 51, BLACK)
                    draw_screen(maze)
                    maze.draw(screen)

            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    speed += 3
                if event.key == K_DOWN:
                    speed -= 3 
                try:
                    if event.key == K_a:
                        move = True
                        player.move(maze, 'Left')
                        # player.draw()
                    if event.key == K_d:
                        move = True
                        player.move(maze, 'Right')
                        # player.draw()
                    if event.key == K_w:
                        move = True
                        player.move(maze, 'Up')
                        
                        # player.draw()
                    if event.key == K_s:
                        move = True
                        player.move(maze, 'Down')
                except:
                    pass
                    # player.draw()
        
        pygame.event.pump()
        draw_screen(maze)
        # if player_Win:
        #     title_win.draw()
        
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()