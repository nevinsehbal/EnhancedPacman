import math
from Block import *
import numpy as np
import matplotlib.pyplot as plt

def initialize_A_star(vertices_list,wall_list):
  generateVertices(vertices_list,wall_list)
  v,e = generate_graph(vertices_list,wall_list)
#   plotgraph(v,e)
#   path = A_star((v,e),v[15],v[167])
#   print(v[0],v[7])
#   print("Path is ",path)
#   plotgraph(path, e)
  graph = (v,e)
  return graph


# Euclidean Distance between two nodes
def eucledian_distance(node1, node2):
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

# Neighbors of a node inside graph G.
def find_neighbors( edges, node):
    neighbors = []
    for edge in edges:
        # Loop through every edge, inside the edge there are vertices.
        if edge[0] == node:
            # Check if it exists in neighbors before adding
            neighbor_node = edge[1]
            if neighbor_node not in neighbors:
                neighbors.append(neighbor_node)
        elif edge[1] == node:
            neighbor_node = edge[0]
            if neighbor_node not in neighbors:
                neighbors.append(neighbor_node)
    return neighbors

def calculate_cost(successor, current_node, end_node):
    successor.g = current_node.g + eucledian_distance(current_node, successor)
    successor.h = eucledian_distance(end_node, successor)
    successor.f = successor.g + successor.h
    return successor.f


def generateVertices(vertices_list,wall_list):
      # Draw the grid
  for row in range(19):
      for column in range(19):
        block = Block(yellow, 4, 4)
        # Set a random location for the block
        block.rect.x = (30*column+6)+26
        block.rect.y = (30*row+6)+26
        collision = pygame.sprite.spritecollide(block, wall_list, False)
        if collision:
            continue
        else:
            # Add the block to the list of objects
            vertices_list.add(block)
  return

def generate_graph(dot_list, wall_list):
    vertices = []
    edges = []

    # Create vertices from dot positions
    for dot in dot_list:
        vertices.append(Node(dot.rect.x, dot.rect.y))

    # Create edges based on valid connections between vertices (no walls in between)
    for i, start_node in enumerate(vertices):
      for j in range(i + 1, len(vertices)):  # Avoid redundant pairings
          end_node = vertices[j]
          distance = pygame.math.Vector2(end_node.x - start_node.x, end_node.y - start_node.y).length()
          if distance <= 40 and not is_path_blocked(start_node, end_node, wall_list):
                edges.append((start_node, end_node))
                edges.append((end_node, start_node))  # Assuming the graph is undirected
    return vertices, edges


def is_path_blocked(start_node, end_node, walls):
    # Check if there's a wall blocking the path between two nodes
    line = pygame.math.Vector2(end_node.x - start_node.x, end_node.y - start_node.y)
    distance = line.length()
    for wall in walls:
        if is_point_inside_rect(start_node.x, start_node.y, wall.rect) or is_point_inside_rect(end_node.x, end_node.y, wall.rect):
            return True
        for step in range(int(distance)):
            point = start_node.x + line.x * (step / distance), start_node.y + line.y * (step / distance)
            if is_point_inside_rect(point[0], point[1], wall.rect):
                return True
    return False

def is_point_inside_rect(x, y, rect):
    return rect.x <= x <= rect.x + rect.width and rect.y <= y <= rect.y + rect.height

def plotgraph(vertices, edges):
    x, y = [], []
    for v in vertices:
        x.append(v.x)
        y.append(v.y)
    plt.scatter(np.array(x), np.array(y))

    for edge in edges:
        start_node, end_node = edge  # Unpack the tuple
        plt.plot([start_node.x, end_node.x], [start_node.y, end_node.y], 'm')
    plt.gca().invert_yaxis()
    plt.show()

def A_star(G, start_vertex, end_vertex):
    vertices, edges = G

    end_node = Node(end_vertex[0], end_vertex[1])
    start_node = Node(start_vertex[0], start_vertex[1])

    # Assert if start and end are members of G.
    assert start_node in vertices, "Start vertex not in graph."
    assert end_node in vertices, "End vertex not in graph."

    open_list = []  # open list.
    closed_list = []  # closed list

    
    start_node.f = start_node.h = eucledian_distance(start_node, end_node)
    
    # For convenience, put graph G to a Node list struct.
    open_list.append(start_node)
    
    while open_list:
        current_node = min(open_list, key=lambda node: node.f)
        open_list.remove(current_node)
        closed_list.append(current_node)
        # Is finished?
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent
            return path

        # Find successors, neighbors
        successor_list = find_neighbors( edges, current_node)
        for successor in successor_list:
            
            if successor in closed_list:
                continue
            successor.parent = current_node
            cost = calculate_cost(successor, current_node, end_node)
            if successor in open_list:
                continue
            open_list.append(successor)