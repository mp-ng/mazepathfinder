import numpy as np

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.pos = position     
        self.c = 0 #cost (each move = 1)
        self.h = 0 #heuristic (Euclidean distance)
        self.t = self.c + self.h #total
        
    def __eq__(self, other):
        return self.pos == other.pos
    
def return_path(current_node, maze):
    path = []
    no_rows, no_columns = np.shape(maze)   
    # initialise result maze with -1 in every position
    result = [[0 for i in range(no_columns)] for j in range(no_rows)] 
    # create path (backwards)
    current = current_node
    while current is not None:
        path.append(current.pos)
        current = current.parent
    # reverse path
    path = path[::-1]
    # update path with incrementing steps
    start_value = 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result

def search(maze, start, end):
    """
    1) First get the current node by comparing all total cost and selecting the lowest cost node for further expansion
    2) Remove the selected node from yet_to_visit list and add this node to visited list
    3) Perform goal test and return the path, else perform below steps:
    4) For selected node find out all children (use move to find children)
        a) get the current postion for the selected node (this becomes parent node for the children)
        b) check if a valid position exist (boundary/walls will make few nodes invalid)
        c) add to valid children node list for the selected parent
    5) For all the children node
        a) if child in visited list then ignore it and try next node
        b) calculate child node g, h and f values
        c) if child in yet_to_visit list and that cost is cheaper then ignore it
        d) else move the child to yet_to_visit list
    """
    # create start and end nodes
    start_node = Node(None, tuple(start))
    end_node = Node(None, tuple(end))
    # create yet to visit and visited lists
    yet_to_visit_list = []
    visited_list = []
    yet_to_visit_list.append(start_node)
    # search movement (up, down, left, right)
    moves = [[-1,0],[1,0],[0,-1],[0,1]]
    no_rows, no_columns = np.shape(maze)
    # loop until end
    while len(yet_to_visit_list) > 0:
        # get the current node
        current_node = yet_to_visit_list[0]
        # move to next node
        for index, node in enumerate(yet_to_visit_list):
            if node.t < current_node.t:
                current_node = node
        # remove current node from yet_to_visit list, add to visited list
        yet_to_visit_list.remove(current_node)
        visited_list.append(current_node)
        # return path if goal reached
        if current_node == end_node:
            return return_path(current_node,maze)
        # generate children from adjacent squares
        children = []
        # loop through the four possible moves
        for move in moves:
            # get node position
            node_pos = (current_node.pos[0] + move[0], current_node.pos[1] + move[1])
            # check if within range
            if (node_pos[0] > (no_rows - 1) or node_pos[0] < 0 or node_pos[1] > (no_columns -1) or node_pos[1] < 0):
                continue
            # check if it is a wall
            if maze[node_pos[0]][node_pos[1]] != 0:
                continue
            # create node
            new_node = Node(current_node, node_pos)
            children.append(new_node)
        # loop through children
        for child in children:
            # if child is on visited list
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                    continue
            # create cost
            child.c = current_node.c + 1
            # create heuristic using Euclidean distance
            child.h = (((child.pos[0] - end_node.pos[0]) ** 2) + ((child.pos[1] - end_node.pos[1]) ** 2)) ** 0.5
            # if child is in the yet_to_visit list and that cost is lower
            if len([i for i in yet_to_visit_list if child == i and child.c > i.c]) > 0:
                continue
            # add the child to the yet_to_visit list
            yet_to_visit_list.append(child)

maze1 = [[0, 0, 1, 0, 0, 0], #5x6
         [0, 1, 1, 0, 1, 0],
         [0, 0, 0, 0, 1, 0],
         [0, 1, 0, 1, 1, 0],
         [0, 1, 0, 1, 0, 0]]

maze2 = [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #21x21
         [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
         [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
         [1, 0, 1, 1, 1, 1, 1, 0 ,1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
         [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
         [1, 0, 1, 1 ,1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
         [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
         [1, 0, 1, 1, 1, 1, 1, 1 ,1 ,1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],          
         [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
         [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
         [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
         [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
         [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
         [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
         [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
         [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1 ,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]

path = search(maze=maze2, start=[0,0], end=[20,20])

print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))
