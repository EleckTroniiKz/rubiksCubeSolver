import enum
import random
import time

#Think about using a dictionary for the cube sides, so every color is a key and every key contains a list with Color strings per indes

"""
dict = {
    white: [
        [],[],[]
    ],
    ...
}
"""


class Faces:
    def __init__(self, color, tiles):
        self.color = color
        self.tiles = tiles
    
    def get_color(self):
        return self.color
    
    def get_tiles(self):
        return self.tiles

class RubiksCubeSolver:
    def __init__(self):
        self.moves = ["R", 'r', "R2", "L", "l", "L2", "U", "u", "U2", "D", "d", "D2", "B", "b", "B2", "F", "f", "F2"]
        self.white = [["W" for row in range(3)] for line in range(3)]
        self.red = [["R" for row in range(3)] for line in range(3)]
        self.blue = [["B" for row in range(3)] for line in range(3)]
        self.green = [["G" for row in range(3)] for line in range(3)]
        self.yellow = [["Y" for row in range(3)] for line in range(3)]
        self.orange = [["O" for row in range(3)] for line in range(3)]

        self.cube_constallation = {
            'white': self.white,
            'red': self.red,
            'blue': self.blue,
            'green': self.green,
            'yellow': self.yellow,
            'orange': self.orange
        }

        self.mover = Movemaker()

        self.startTime = None
        self.endTime = None

    def startTimer(self):
        self.startTime = time.time()

    def calculate_solving_time(self):
        """
        returns the needed time as a tuple (hours, minutes, seconds)
        """
        timeDifference = self.endTime - self.startTime #i guess the time will be gottin seconds.

        if timeDifference >= 60:
            multiplicated = 0
            while 60 * multiplicated <= timeDifference:
                multiplicated += 1
            timeDifference -= (multiplicated * 60)
            if multiplicated >= 60:
                hours = multiplicated // 60
                multiplicated -= hours * 60
                return (hours, multiplicated, timeDifference)
            else:
                return (0, multiplicated, timeDifference)
        else:
            return (0, 0, timeDifference)

    def endTimer(self):
        self.endTime = time.time()
        self.calculate_solving_time()

    #probably irrelevant
    def get_current_cubescramble(self):
        return self.cube_constallation

    def get_solve_time(self):
        return self.endTime - self.startTime

    def get_scramble(self, length=20):
        random_moves = []
        lastMadeMove = ""
        while len(random_moves) < length:
            random_number = random.randint(0, len(self.moves)-1)
            if lastMadeMove.capitalize() == self.moves[random_number].capitalize():
                continue
            else:
                lastMadeMove = self.moves[random_number][0]
                random_moves.append(lastMadeMove)
        
        
    def set_scramble(self, white, red, blue, yellow, green, orange):
        self.white(white)
        self.red(red)
        self.blue(blue)
        self.yellow(yellow)
        self.green(green)
        self.orange(orange)
    
    def executeMove(self, move):
        if move == None:
            return False
        mover = Movemaker(self.get_current_cubescramble())
        if move == "R":
            mover.make_right()
            pass
        elif move == "r":
            mover.make_right(True)
            pass
        elif move == "L":
            mover.make_left()
            pass
        elif move == "l":
            mover.make_left(True)
            pass
        elif move == "U":
            mover.make_up()
            pass
        elif move == "u":
            mover.make_up(True)
            pass
        elif move == "B":
            mover.make_back()
            pass
        elif move == "b":
            mover.make_back(True)
            pass
        elif move == "D":
            mover.make_down()
            pass
        elif move == "d":
            mover.make_down(True)
            pass
        elif move == "F":
            mover.make_front()
            pass
        elif move == "f":
            mover.make_front(True)
            pass
    
    def is_edge_piece(self, indices):
        """
            checks if the index of the current piece indicates if its an edge piece or not
        """
        return ((indices[0] == 0 or indices[0] == 2) and indices[1] == 1) or (indices[0] == 1 and (indices[1] == 0 or indices[1] == 2))

    def is_center(self, indices):
        """
        checks if the provided indices belong to a center piece
        """
        return indices[0] == 1 and indices[0] == 1

class Movemaker:
    def __init__(self):
        pass

    def make_left(self, cube, inverted = False):
        #transform the cube as if a left move was made
        pass

    def make_right(self, cube, inverted = False):
        #transform the cube as if a right move was made
        pass

    def make_up(self, cube, inverted = False):
        #transform the cube as if a upper move was made
        pass

    def make_down(self, cube, inverted = False):
        #transform the cube as if a down move was made
        pass

    def make_back(self, cube, inverted = False):
        #transform the cube as if a back move was made
        pass

    def make_front(self, cube, inverted = False):
        #transform the cube as if a front move was made
        pass
