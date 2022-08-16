import enum
import random
from re import X
import time
import tkinter as tk

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

    def has_white_in_face(self, face):
        """
            checks if an element in this list is a white piece
        """
        indices = []
        for i in range(len(face)):
            for j in range(len(face[i])):
                if face[i][j] == "W":
                    indices.append((i,j))
        return indices

class Movemaker:
    def __init__(self):
        pass

    def sort_move(self, moveLetter, cube):
        if moveLetter == "R":
            return self.make_right(cube)
        elif moveLetter == "r":
            return self.make_right(cube, inverted = True)
        elif moveLetter == "D":
            return self.make_down(cube)
        elif moveLetter == "d":
            return self.make_down(cube, inverted = True)
        elif moveLetter == "F":
            return self.make_front(cube)
        elif moveLetter == "f":
            return self.make_front(cube, inverted = True)
        elif moveLetter == "B":
            return self.make_back(cube)
        elif moveLetter == "b":
            return self.make_back(cube, inverted = True)
        elif moveLetter == "L":
            return self.make_left(cube)
        elif moveLetter == "l":
            return self.make_left(cube, inverted = True) 
        elif moveLetter == "U":
            return self.make_up(cube)
        elif moveLetter == "u":
            return self.make_up(cube, inverted = True)

    def twist(self, currentSide, inverted = False):
        if not inverted:
            tempRed = currentSide[0][0]
            currentSide[0][0] = currentSide[2][0]
            currentSide[0][2], tempRed = tempRed, currentSide[0][2]
            currentSide[2][2], tempRed = tempRed, currentSide[2][2] 
            currentSide[0][1] = tempRed

            currentSide[0][1], tempRed = currentSide[1][0], currentSide[0][1] 
            currentSide[1][0] = currentSide[2][1]
            currentSide[2][1] = currentSide[1][2]
            currentSide[1][2] = tempRed
        else:
            pass
        return currentSide

    def make_left(self, cube, inverted = False):
        #transform the cube as if a left move was made
        if not inverted:
            whiteA, whiteB, whiteC = cube["white"][0][0], cube["white"][1][0], cube["white"][2][0]
            cube["white"][0][0], cube["white"][1][0], cube["white"][2][0] = cube["green"][0][0], cube["green"][1][0], cube["green"][2][0]

            cube["green"][0][0], cube["green"][1][0], cube["green"][2][0] = cube["yellow"][0][0], cube["yellow"][1][0], cube["yellow"][2][0]

            cube["yellow"][0][0], cube["yellow"][1][0], cube["yellow"][2][0] = cube["blue"][0][0], cube["blue"][1][0], cube["blue"][2][0]

            cube["blue"][0][0], cube["blue"][1][0], cube["blue"][2][0] = whiteA, whiteB, whiteC

            cube["red"] = self.twist(cube["red"])
        else:
            whiteA, whiteB, whiteC = cube["white"][0][0], cube["white"][1][0], cube["white"][2][0]
            cube["white"][0][0], cube["white"][1][0], cube["white"][2][0] = cube["blue"][0][0], cube["blue"][1][0], cube["blue"][2][0]

            cube["blue"][0][0], cube["blue"][1][0], cube["blue"][2][0] = cube["yellow"][0][0], cube["yellow"][1][0], cube["yellow"][2][0]
        
            cube["yellow"][0][0], cube["yellow"][1][0], cube["yellow"][2][0] = cube["green"][0][0], cube["green"][1][0], cube["green"][2][0]

            cube["green"][0][0], cube["green"][1][0], cube["green"][2][0] = whiteA, whiteB, whiteC

            cube["red"] = self.twist(cube["red"], True)
        return cube

    def make_right(self, cube, inverted = False):
        #transform the cube as if a right move was made
        if not inverted:
            whiteA, whiteB, whiteC = cube["white"][0][2], cube["white"][1][2], cube["white"][2][2]
            cube["white"][0][2], cube["white"][1][2], cube["white"][2][2] = cube["blue"][0][2], cube["blue"][1][2], cube["blue"][2][2]

            cube["blue"][0][2], cube["blue"][1][2], cube["blue"][2][2] = cube["yellow"][0][2], cube["yellow"][1][2], cube["yellow"][2][2]

            cube["yellow"][0][2], cube["yellow"][1][2], cube["yellow"][2][2] = cube["green"][0][2], cube["green"][1][2], cube["green"][2][2]

            cube["green"][0][2], cube["green"][1][2], cube["green"][2][2] = whiteA, whiteB, whiteC

            cube["orange"] = self.twist(cube["orange"])
        else:
            whiteA, whiteB, whiteC = cube["white"][0][2], cube["white"][1][2], cube["white"][2][2]
            cube["white"][0][2], cube["white"][1][2], cube["white"][2][2] = cube["green"][0][2], cube["green"][1][2], cube["green"][2][2]
            
            cube["green"][0][2], cube["green"][1][2], cube["green"][2][2] = cube["yellow"][0][2], cube["yellow"][1][2], cube["yellow"][2][2]

            cube["yellow"][0][2], cube["yellow"][1][2], cube["yellow"][2][2] = cube["blue"][0][2], cube["blue"][1][2], cube["blue"][2][2]

            cube["blue"][0][2], cube["blue"][1][2], cube["blue"][2][2] = whiteA, whiteB, whiteC
            
            cube["orange"] = self.twist(cube["orange"], True)
        return cube

    def make_up(self, cube, inverted = False):
        #transform the cube as if a upper move was made
        if not inverted:
            whiteA, whiteB, whiteC = cube["white"][0][0], cube["white"][0][1], cube["white"][0][2]
            cube["white"][0][0], cube["white"][0][1], cube["white"][0][2] = cube["orange"][0][0], cube["orange"][0][1], cube["orange"][0][2]
            
            cube["orange"][0][0], cube["orange"][0][1], cube["orange"][0][2] = cube["yellow"][2][0], cube["yellow"][2][1], cube["yellow"][2][2]

            cube["yellow"][2][0], cube["yellow"][2][1], cube["yellow"][2][2] = cube["red"][0][0], cube["red"][0][1], cube["red"][0][2]

            cube["red"][0][0], cube["red"][0][1], cube["red"][0][2] = whiteA, whiteB, whiteC
            
            cube["green"] = self.twist(cube["green"])
        else:
            whiteA, whiteB, whiteC = cube["white"][0][0], cube["white"][0][1], cube["white"][0][2]
            cube["white"][0][0], cube["white"][0][1], cube["white"][0][2] = cube["red"][0][0], cube["red"][0][1], cube["red"][0][2]

            cube["red"][0][0], cube["red"][0][1], cube["red"][0][2] = cube["yellow"][2][0], cube["yellow"][2][1], cube["yellow"][2][2]

            cube["yellow"][2][0], cube["yellow"][2][1], cube["yellow"][2][2] = cube["orange"][0][0], cube["orange"][0][1], cube["orange"][0][2]

            cube["orange"][0][0], cube["orange"][0][1], cube["orange"][0][2] = whiteA, whiteB, whiteC
            
            cube["green"] = self.twist(cube["green"], True)
        return cube

#yellow wrong
    def make_down(self, cube, inverted = False):
        #transform the cube as if a down move was made
        if not inverted:
            whiteA, whiteB, whiteC = cube["white"][2][0], cube["white"][2][1], cube["white"][2][2]
            cube["white"][2][0], cube["white"][2][1], cube["white"][2][2] = cube["red"][2][0], cube["red"][2][1], cube["red"][2][2]
            
            cube["red"][2][0], cube["red"][2][1], cube["red"][2][2] = cube["yellow"][0][0], cube["yellow"][0][1], cube["yellow"][0][2]

            cube["yellow"][0][0], cube["yellow"][0][1], cube["yellow"][0][2] = cube["orange"][2][0], cube["orange"][2][1], cube["orange"][2][2]
            
            cube["orange"][2][0], cube["orange"][2][1], cube["orange"][2][2] = whiteA, whiteB, whiteC

            cube["blue"] = self.twist(cube["blue"])
            
        else:
            whiteA, whiteB, whiteC = cube["white"][2][0], cube["white"][2][1], cube["white"][2][2]
            cube["white"][2][0], cube["white"][2][1], cube["white"][2][2] = cube["orange"][2][0], cube["orange"][2][1], cube["orange"][2][2]
            
            cube["orange"][2][0], cube["orange"][2][1], cube["orange"][2][2] = cube["yellow"][2][0], cube["yellow"][2][1], cube["yellow"][2][2]

            cube["yellow"][2][0], cube["yellow"][2][1], cube["yellow"][2][2] = cube["red"][2][0], cube["red"][2][1], cube["red"][2][2]

            cube["red"][2][0], cube["red"][2][1], cube["red"][2][2] = whiteA, whiteB, whiteC
            
            cube["blue"] = self.twist(cube["blue"], True)
        return cube

    def make_back(self, cube, inverted = False):
        #transform the cube as if a back move was made
        if not inverted:
            greenA, greenB, greenC = cube["green"][0][0], cube["green"][0][1], cube["green"][0][2]
            cube["green"][0][0], cube["green"][0][1], cube["green"][0][2] = cube["orange"][0][2], cube["orange"][1][2], cube["orange"][2][2]
            
            cube["orange"][0][2], cube["orange"][1][2], cube["orange"][2][2] = cube["blue"][2][2], cube["blue"][2][1], cube["blue"][2][0]

            cube["blue"][2][0], cube["blue"][2][1], cube["blue"][2][2] = cube["red"][0][0], cube["red"][1][0], cube["red"][2][0]

            cube["red"][0][0], cube["red"][1][0], cube["red"][2][0] = greenA, greenB, greenC
            
            cube["yellow"] = self.twist(cube["yellow"])
            
        else:
            greenA, greenB, greenC = cube["green"][0][0], cube["green"][0][1], cube["green"][0][2]
            cube["green"][0][0], cube["green"][0][1], cube["green"][0][2] = cube["red"][2][0], cube["red"][1][0], cube["red"][0][0]
            
            cube["red"][2][0], cube["red"][1][0], cube["red"][0][0] = cube["blue"][2][2], cube["blue"][2][1], cube["blue"][2][0]

            cube["blue"][2][0], cube["blue"][2][1], cube["blue"][2][2] = cube["orange"][0][2], cube["orange"][1][2], cube["orange"][2][2]

            cube["orange"][0][2], cube["orange"][1][2], cube["orange"][2][2] = greenA, greenB, greenC
            
            cube["yellow"] = self.twist(cube["yellow"], inverted=True)
        return cube

    def make_front(self, cube, inverted = False):
        #transform the cube as if a front move was made
        if not inverted:
            greenA, greenB, greenC = cube["green"][2][0], cube["green"][2][1], cube["green"][2][2]
            cube["green"][2][0], cube["green"][2][1], cube["green"][2][2] = cube["red"][2][2], cube["red"][1][2], cube["red"][0][2]

            cube["red"][0][2], cube["red"][1][2], cube["red"][2][2] = cube["blue"][0][0], cube["blue"][0][1], cube["blue"][0][2]

            cube["blue"][0][0], cube["blue"][0][1], cube["blue"][0][2] = cube["orange"][2][0], cube["orange"][1][0], cube["orange"][0][0]
            
            cube["orange"][0][0], cube["orange"][1][0], cube["orange"][2][0] = greenA, greenB, greenC
            
            cube["white"] = self.twist(cube["white"])
            return cube
        else:
            greenA, greenB, greenC = cube["green"][2][0], cube["green"][2][1], cube["green"][2][2]
            cube["green"][2][0], cube["green"][2][1], cube["green"][2][2] = cube["orange"][2][0], cube["orange"][1][0], cube["orange"][0][0]
            
            cube["orange"][0][0], cube["orange"][1][0], cube["orange"][2][0] = cube["blue"][0][0], cube["blue"][0][1], cube["blue"][0][2]

            cube["blue"][0][0], cube["blue"][0][1], cube["blue"][0][2] = cube["red"][2][2], cube["red"][1][2], cube["red"][0][2]

            cube["red"][0][2], cube["red"][1][2], cube["red"][2][2] = greenA, greenB, greenC
            
            cube["white"] = self.twist(cube["white"])
        return cube

class Tester:
    def __init__(self):
        self.mover = Movemaker()

    def print_cube(self, cube):
        oneLine = " | x | y | z |"
        emptyLines = "              "
        print(emptyLines + oneLine.replace("x", cube["green"][0][0]).replace("y", cube["green"][0][1]).replace("z", cube["green"][0][2]) + emptyLines)
        print(emptyLines + oneLine.replace("x", cube["green"][1][0]).replace("y", cube["green"][1][1]).replace("z", cube["green"][1][2]) + emptyLines)
        print(emptyLines + oneLine.replace("x", cube["green"][2][0]).replace("y", cube["green"][2][1]).replace("z", cube["green"][2][2]) + emptyLines)

        print(oneLine.replace("x", cube["red"][0][0]).replace("y", cube["red"][0][1]).replace("z", cube["red"][0][2]) + oneLine.replace("x", cube["white"][0][0]).replace("y", cube["white"][0][1]).replace("z", cube["white"][0][2]) +oneLine.replace("x", cube["orange"][0][0]).replace("y", cube["orange"][0][1]).replace("z", cube["orange"][0][2]))
        print(oneLine.replace("x", cube["red"][0][0]).replace("y", cube["red"][1][1]).replace("z", cube["red"][1][2]) + oneLine.replace("x", cube["white"][1][0]).replace("y", cube["white"][1][1]).replace("z", cube["white"][1][2]) +oneLine.replace("x", cube["orange"][1][0]).replace("y", cube["orange"][1][1]).replace("z", cube["orange"][1][2]))
        print(oneLine.replace("x", cube["red"][0][0]).replace("y", cube["red"][2][1]).replace("z", cube["red"][2][2]) + oneLine.replace("x", cube["white"][2][0]).replace("y", cube["white"][2][1]).replace("z", cube["white"][2][2]) +oneLine.replace("x", cube["orange"][2][0]).replace("y", cube["orange"][2][1]).replace("z", cube["orange"][2][2]))

        print(emptyLines + oneLine.replace("x", cube["blue"][0][0]).replace("y", cube["blue"][0][1]).replace("z", cube["blue"][0][2]) + emptyLines)
        print(emptyLines + oneLine.replace("x", cube["blue"][1][0]).replace("y", cube["blue"][1][1]).replace("z", cube["blue"][1][2]) + emptyLines)
        print(emptyLines + oneLine.replace("x", cube["blue"][2][0]).replace("y", cube["blue"][2][1]).replace("z", cube["blue"][2][2]) + emptyLines)

        print(emptyLines + oneLine.replace("x", cube["yellow"][0][0]).replace("y", cube["yellow"][0][1]).replace("z", cube["yellow"][0][2]) + emptyLines)
        print(emptyLines + oneLine.replace("x", cube["yellow"][1][0]).replace("y", cube["yellow"][1][1]).replace("z", cube["yellow"][1][2]) + emptyLines)
        print(emptyLines + oneLine.replace("x", cube["yellow"][2][0]).replace("y", cube["yellow"][2][1]).replace("z", cube["yellow"][2][2]) + emptyLines)

    def test_Transformation(self, desired_transform, cube):
        transformedCube = None
        #self.print_cube(cube)
        if desired_transform == "R":
            transformedCube = self.mover.make_right(cube)
        elif desired_transform == "L":
            transformedCube = self.mover.make_left(cube)
        elif desired_transform == "U":
            transformedCube = self.mover.make_up(cube)
        elif desired_transform == "D":
            transformedCube = self.mover.make_down(cube)
        elif desired_transform == "F":
            transformedCube = self.mover.make_front(cube)
        elif desired_transform == "B":
            transformedCube = self.mover.make_back(cube)
        #cube has changes already?
        self.print_cube(cube)
        #print_cube(transformedCube)

class UserInterface:
    def __init__(self, root, mover, cube):
        self.root = root
        self.mover = mover
        self.cube = cube
        self.create_move_buttons()    
        self.print_cube(self.cube)

    def create_move_buttons(self):
        self.L_button = tk.Button(self.root, text="  L  ", command=lambda: self.moveButtonHandler('L'))
        self.L_button.place(x=25, y=450)
        self.l_button = tk.Button(self.root, text="  l  ", command=lambda: self.moveButtonHandler('l'))
        self.l_button.place(x=25, y=475)

        self.R_button = tk.Button(self.root, text="  R  ", command=lambda: self.moveButtonHandler('R'))
        self.R_button.place(x=60, y=450)
        self.r_button = tk.Button(self.root, text="  r  ", command=lambda: self.moveButtonHandler('r'))
        self.r_button.place(x=60, y=475)

        self.U_button = tk.Button(self.root, text="  U  ", command=lambda: self.moveButtonHandler('U'))
        self.U_button.place(x=95, y=450)
        self.u_button = tk.Button(self.root, text="  u  ", command=lambda: self.moveButtonHandler('u'))
        self.u_button.place(x=95, y=475) 

        self.F_button = tk.Button(self.root, text="  F  ", command=lambda: self.moveButtonHandler('F'))
        self.F_button.place(x=130, y=450)
        self.f_button = tk.Button(self.root, text="  f  ", command=lambda: self.moveButtonHandler('f'))
        self.f_button.place(x=130, y=475)

        self.D_button = tk.Button(self.root, text="  D  ", command=lambda: self.moveButtonHandler('D'))
        self.D_button.place(x=165, y=450)
        self.d_button = tk.Button(self.root, text="  d  ", command=lambda: self.moveButtonHandler('d'))
        self.d_button.place(x=165, y=475)

        self.B_button = tk.Button(self.root, text="  B  ", command=lambda: self.moveButtonHandler('B'))
        self.B_button.place(x=200, y=450)
        self.b_button = tk.Button(self.root, text="  b  ", command=lambda: self.moveButtonHandler('b'))
        self.b_button.place(x=200, y=475)
        pass

    def get_color(self, color):
        return 'white' if color == "W" else 'red' if color == "R" else 'blue' if color == "B" else 'yellow' if color == "Y" else 'green' if color == "G" else 'orange'

    def print_cube(self, cube):
        self.print_face(cube["green"], 47, 0)
        self.print_face(cube["red"], 0, 75)
        self.print_face(cube["white"], 47, 75)
        self.print_face(cube["orange"], 94, 75)
        self.print_face(cube["blue"], 47, 150)
        self.print_face(cube["yellow"], 47, 225)

    def print_face(self, colors, gridX, gridY):
        tL = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][0]))
        tL.place(x=gridX, y=gridY)

        tM = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][1]))
        tM.place(x=gridX+15, y=gridY)

        tR = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][2]))
        tR.place(x=gridX+30, y=gridY)

        mL = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][0]))
        mL.place(x=gridX, y=gridY+25)

        mM = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][1]))
        mM.place(x=gridX+15, y=gridY+25)

        mR = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][2]))
        mR.place(x=gridX+30, y=gridY+25)

        bL = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][0]))
        bL.place(x=gridX, y=gridY+50)

        bM = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][1]))
        bM.place(x=gridX+15, y=gridY+50)

        bR = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][2]))
        bR.place(x=gridX+30, y=gridY+50)
        
    def moveButtonHandler(self, move):
        self.cube = self.mover.sort_move(move, self.cube)
        self.print_cube(self.cube)
        self.print_cube(self.cube)


def setupTesterInConsole():
    white = [["W" for row in range(3)] for line in range(3)]
    red = [["R" for row in range(3)] for line in range(3)]
    blue = [["B" for row in range(3)] for line in range(3)]
    green = [["G" for row in range(3)] for line in range(3)]
    yellow = [["Y" for row in range(3)] for line in range(3)]
    orange = [["O" for row in range(3)] for line in range(3)]

    cube_constallation = {
                'white': white,
                'red': red,
                'blue': blue,
                'green': green,
                'yellow': yellow,
                'orange': orange
            }

    tester = Tester()

    tester.test_Transformation('R', cube_constallation)

def setup_main_program():

    white = [["W" for row in range(3)] for line in range(3)]
    red = [["R" for row in range(3)] for line in range(3)]
    blue = [["B" for row in range(3)] for line in range(3)]
    green = [["G" for row in range(3)] for line in range(3)]
    yellow = [["Y" for row in range(3)] for line in range(3)]
    orange = [["O" for row in range(3)] for line in range(3)]

    cube_constallation = {
        'white': white,
        'red': red,
        'blue': blue,
        'green': green,
        'yellow':yellow,
        'orange': orange
    }

    root = tk.Tk()
    root.geometry('1500x800')
    interface = UserInterface(root, Movemaker(), cube_constallation)

    root.mainloop()

setup_main_program()
