# 2x2 Rubik's cube solver using breadth-first search (BFS)

import copy
import json
from collections import deque

# This is just a random solvable scramble. The scramble can be any possible node.
cube = {
    "front": [
        ["y", "b"],
        ["o", "o"]
    ],
    "top": [
        ["r", "g"],
        ["o", "y"]
    ],
    "left": [
        ["g", "b"],
        ["w", "w"]
    ],
    "right": [
        ["r", "w"],
        ["g", "y"]
    ],
    "bottom": [
        ["b", "y"],
        ["b", "r"]
    ],
    "back": [
        ["o", "w"],
        ["g", "r"]
    ]
}

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# Checks every possible child of a node before moving on to the next. 
class QueueFrontier:
    def __init__(self):
        self.frontier = deque()

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.popleft()

class RubiksCube:
    def __init__(self, cube):
        self.start = copy.deepcopy(cube)

    @staticmethod
    def solved(state):
        for face in ["front","top","left","right","bottom","back"]:
            first_color = state[face][0][0]
            for row in state[face]:
                for color in row:
                    if color != first_color:
                        return False
        return True

    @staticmethod
    def copy_cube(state):
        return {face: [row[:] for row in state[face]] for face in state}
    
    # Cube turning logic
    def apply_move(self, state, move):
        new_state = copy.deepcopy(state)

        # U
        if move == "U":
            new_state["top"] = [
                [new_state["top"][0][1], new_state["top"][1][1]],
                [new_state["top"][0][0], new_state["top"][1][0]]
            ]

            front_top = new_state["front"][0][:]
            left_top = new_state["left"][0][:]
            back_top = new_state["back"][0][:]
            right_top = new_state["right"][0][:]

            new_state["front"][0] = left_top
            new_state["left"][0] = back_top
            new_state["back"][0] = right_top
            new_state["right"][0] = front_top

        # D
        elif move == "D":
            new_state["bottom"] = [
                [new_state["bottom"][1][0], new_state["bottom"][0][0]],
                [new_state["bottom"][1][1], new_state["bottom"][0][1]]
            ]

            front_bottom = new_state["front"][1][:]
            left_bottom = new_state["left"][1][:]
            back_bottom = new_state["back"][1][:]
            right_bottom = new_state["right"][1][:]

            new_state["front"][1] = left_bottom
            new_state["left"][1] = back_bottom
            new_state["back"][1] = right_bottom
            new_state["right"][1] = front_bottom

        # R
        elif move == "R":
            new_state["right"] = [
                [new_state["right"][0][1], new_state["right"][1][1]],
                [new_state["right"][0][0], new_state["right"][1][0]]
            ]

            front_right = [new_state["front"][0][1], new_state["front"][1][1]]
            top_right = [new_state["top"][0][1], new_state["top"][1][1]]
            back_left = [new_state["back"][1][0], new_state["back"][0][0]]
            bottom_right = [new_state["bottom"][0][1], new_state["bottom"][1][1]]

            new_state["front"][0][1], new_state["front"][1][1] = top_right
            new_state["top"][0][1], new_state["top"][1][1] = back_left
            new_state["back"][1][0], new_state["back"][0][0] = bottom_right
            new_state["bottom"][0][1], new_state["bottom"][1][1] = front_right

        # L
        elif move == "L":
            new_state["left"] = [
                [new_state["left"][1][0], new_state["left"][0][0]],
                [new_state["left"][1][1], new_state["left"][0][1]]
            ]

            front_left = [new_state["front"][0][0], new_state["front"][1][0]]
            top_left = [new_state["top"][0][0], new_state["top"][1][0]]
            back_right = [new_state["back"][1][1], new_state["back"][0][1]]
            bottom_left = [new_state["bottom"][0][0], new_state["bottom"][1][0]]

            new_state["front"][0][0], new_state["front"][1][0] = top_left
            new_state["top"][0][0], new_state["top"][1][0] = back_right
            new_state["back"][1][1], new_state["back"][0][1] = bottom_left
            new_state["bottom"][0][0], new_state["bottom"][1][0] = front_left

        # F
        elif move == "F":
            new_state["front"] = [
                [new_state["front"][0][1], new_state["front"][1][1]],
                [new_state["front"][0][0], new_state["front"][1][0]]
            ]

            left_right = [new_state["left"][0][1], new_state["left"][1][1]]
            top_bottom = [new_state["top"][1][1], new_state["top"][1][0]]
            right_left = [new_state["right"][1][0], new_state["right"][0][0]]
            bottom_top = [new_state["bottom"][0][0], new_state["bottom"][0][1]]

            new_state["left"][0][1], new_state["left"][1][1] = top_bottom
            new_state["top"][1][1], new_state["top"][1][0] = right_left
            new_state["right"][1][0], new_state["right"][0][0] = bottom_top
            new_state["bottom"][0][0], new_state["bottom"][0][1] = left_right

        # B
        elif move == "B":
            new_state["back"] = [
                [new_state["back"][1][0], new_state["back"][0][0]],
                [new_state["back"][1][1], new_state["back"][0][1]]
            ]

            left_left = [new_state["left"][0][0], new_state["left"][1][0]]
            top_top = [new_state["top"][0][1], new_state["top"][0][0]]
            right_right = [new_state["right"][1][1], new_state["right"][0][1]]
            bottom_bottom = [new_state["bottom"][1][0], new_state["bottom"][1][1]]

            new_state["left"][0][0], new_state["left"][1][0] = top_top
            new_state["top"][0][1], new_state["top"][0][0] = right_right
            new_state["right"][1][1], new_state["right"][0][1] = bottom_bottom
            new_state["bottom"][1][0], new_state["bottom"][1][1] = left_left

        return new_state

    @staticmethod
    def serialize(state):
        return json.dumps(state, separators=(',', ':'), sort_keys=True)
    
    # Not necessary, but can be used to visualize the process. (makes the process slower)
    def print_cube(self, state):
        print("Front:", state["front"])
        print("Top:", state["top"])
        print("Left:", state["left"])
        print("Right:", state["right"])
        print("Bottom:", state["bottom"])
        print("Back:", state["back"])
        print("-" * 20)

    def solve(self):
        start_state = self.copy_cube(self.start)
        start_node = Node(state=start_state, parent=None, action=None)

        frontier = QueueFrontier()
        frontier.add(start_node)

        explored = set()
        num_explored = 0
        frontier_serials = {RubiksCube.serialize(start_state)}

        moves = ["U", "D", "L", "R", "F", "B"]

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            frontier_serials.remove(RubiksCube.serialize(node.state))

            # self.print_cube(node.state) # a bit slower
            num_explored += 1
            print(num_explored)


            if self.solved(node.state):
                actions = []
                cells = []
                current_node = node
                while current_node.parent is not None:
                    actions.append(current_node.action)
                    cells.append(current_node.state)
                    current_node = current_node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                print("SOLVED! moves:", self.solution)
                return

            explored.add(self.serialize(node.state))

            for move in moves:
                new_state = self.apply_move(node.state, move)
                s = self.serialize(new_state)

                if s not in explored and s not in frontier_serials:
                    child = Node(state=new_state, parent=node, action=move)
                    frontier.add(child)
                    frontier_serials.add(s)

if __name__ == "__main__":
    solver = RubiksCube(cube)
    solution = solver.solve()
