import random

# A node class to hold cost functions and position of a point in the graph.
class Node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.g = 0  # cost from start node to current node
        self.h = 0  # heuristic cost from current node to goal node
        self.f = 0  # total cost (g + h)
        self.parent = None
    def __str__(self): #For printing purposes
      return f'({self.x},{self.y})'
    def __repr__(self):#For printing purposes
      return str(self)
    def __eq__(self,other):
       return isinstance(other, Node) and self.x == other.x and self.y == other.y
    def get_coordinates(self):
      return (self.x,self.y)
    


black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow   = ( 255, 255, 0)

def create_walls():
   frame_walls = [[0,0,6,600], [0,0,600,6], [0,600,606,6],[600,0,6,606]]
   starts = [60,120,180,240,300,360,420,480]
   maze = recursive_backtracking(starts, starts)
   return maze+frame_walls

def recursive_backtracking(x_starts, y_starts):
    # Recursive backtracking algorithm for maze generation
    stack = []
    maze = []
    for x in x_starts:
        for y in y_starts:
            stack.append((x, y))
    while stack:
        x, y = stack.pop()
        if [x, y, 64, 6] not in maze and [x, y, 6, 64] not in maze and not is_frame_wall(x, y):
            maze.append([x, y, 64, 6]) if random.choice([True, False]) else maze.append([x, y, 6, 64])
            directions = [(0, 60), (0, -60), (60, 0), (-60, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx <= 480 and 0 <= ny <= 480 and [nx, ny, 64, 6] not in maze \
                        and [nx, ny, 6, 64] not in maze and not is_frame_wall(nx, ny):
                    stack.append((nx, ny))
    return maze

def is_frame_wall(x, y):
    # Check if the position is within the frame walls
    return (0 < x < 600 and y == 0) or (x == 0 and 0 < y < 600) or (0 < x < 600 and y == 600) or (x == 600 and 0 < y < 600)