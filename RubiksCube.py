import enum
import random
import time
import tkinter as tk
from mover import Movemaker

"""
dict = {
    white: [
        [],[],[]
    ],
    ...
}
"""
class CubieLinks:
    def __init__(self):
        self.links = {}



class Faces:
    def __init__(self, color, tiles):
        self.color = color
        self.tiles = tiles
    
    def get_color(self):
        return self.color
    
    def get_tiles(self):
        return self.tiles

class RubiksCubeSolver:
    def __init__(self, mover, cube):
        self.moves = ["R", 'r', "R2", "L", "l", "L2", "U", "u", "U2", "D", "d", "D2", "B", "b", "B2", "F", "f", "F2"]
        self.cube = cube
        self.mover = mover

        self.startTime = None
        self.endTime = None
    
    
    def get_cross_phase(self):
        
        if self.cube["yellow"][0][1] == self.cube["yellow"][2][1] == self.cube["yellow"][1][0] == self.cube["yellow"][1][2] == "Y":
            return 3
        elif self.cube["yellow"][0][1] == self.cube["yellow"][2][1] == "Y" or self.cube["yellow"][1][0] == self.cube["yellow"][1][2] == "Y":
            return 2
        elif self.cube["yellow"][0][1] == self.cube["yellow"][1][0] == "Y" or \
            self.cube["yellow"][0][2] == self.cube["yellow"][1][2] == "Y" or \
                self.cube["yellow"][2][0] == self.cube["yellow"][1][0] == "Y" or \
                    self.cube["yellow"][2][2] == self.cube["yellow"][1][2] == "Y":
                    return 1
        else:
            return 0

    def phase_2_at_right_position(self):
        while not (self.cube["yellow"][1][0] == self.cube["yellow"][1][2] == "Y"):
            self.cube = self.mover.make_back(self.cube)

    def phase_1_at_right_position(self):
        while not (self.cube["yellow"][1][0] == self.cube["yellow"][0][1] == "Y"):
            self.cube = self.mover.make_back(self.cube)
        
    def top_cross_algorithm(self):
        self.cube = self.mover.make_right(self.cube)
        self.cube = self.mover.make_down(self.cube)
        self.cube = self.mover.make_back(self.cube)
        self.cube = self.mover.make_right(self.cube, inverted = True)
        self.cube = self.mover.make_down(self.cube, inverted = True)
        self.cube = self.mover.make_back(self.cube, inverted = True)

    def create_yellow_cross(self):
        hasCross = False
        """
        pahse 0 : only center yellow
        phase 1 : yellow L
        phase 2 : yellow Line
        phase 3 : yellow Cross 
        """
        while not hasCross:
            currentPhase = self.get_cross_phase()
            if currentPhase == 0:
                self.top_cross_algorithm()
            elif currentPhase == 1:
                #reorientate correctly
                self.phase_1_at_right_position()
                self.top_cross_algorithm()
            elif currentPhase == 2:
                #locate correctly
                self.phase_2_at_right_position()
                self.top_cross_algorithm()
            else:
                # yellow cross has been created at this point
                return

    def orientate_top_edges(self):
        # move edges so one is correct
        # do algorithm
        while not self.cube["red"][1][0] == "R":
            self.cube = self.mover.make_back(self.cube)
        if self.cube["blue"][2][1] == "O" and self.cube["orange"][1][2] == "B":
            self.cube = self.execute_edge_change(self.cube, "ol")
        elif self.cube["blue"][2][1] == "O" and self.cube["orange"][1][2] == "G":
            self.cube = self.execute_edge_change(self.cube, "tl")
            # erst orange mit grün vertauschen dann orange mit blau
        elif self.cube["blue"][2][1] == "G" and self.cube["orange"][1][2] == "B":
            self.cube = self.execute_edge_change(self.cube, "ol")
            # orange noch mit grün tauschen
        elif self.cube["blue"][2][1] == "G" and self.cube["orange"][1][2] == "O":
            # erst blau orange switch, dann porrange grün switch, dann blau orange switch
            pass
                
    def check_white_cross(self):
        return (self.cube["white"][0][1] == self.cube["white"][1][0] == self.cube["white"][1][2] == self.cube["white"][2][1] == "W")

    def check_side(self, side):
        return (self.cube[side][0][0] == self.cube[side][0][1] == self.cube[side][0][2] == self.cube[side][1][0] == self.cube[side][1][2] == self.cube[side][2][0] == self.cube[side][2][1] == self.cube[side][2][2])

    def solve_white_cross(self):
        #solve white edges
        colors = ["blue", "red", "green", "yellow", "orange"]
        white_has_cross = self.check_white_cross()
        index = 0
        while not white_has_cross:
            white_in_face = self.has_white_in_face(colors[index])
            if len(white_in_face) > 0:
                for indices in white_in_face:
                    if self.is_edge_piece(indices):
                        if colors[index] == "blue":
                            if indices == (0,1):
                                #2D
                                #check if top free. if not move
                                #B
                                #l
                                #D
                                #L
                                pass
                            elif indices == (1,0):
                                #check if red side is free
                                # if yes l
                                # if no check if blue is free
                                # L
                                # B
                                # l
                                # same as top technically
                                pass
                            elif indices == (1,2):
                                # check if orange is free
                                # if yes R
                                # if no check if blue is free
                                # r
                                # b
                                # R
                                # same as top technically
                                pass
                            elif indices == (2,1):
                                # check if blue free
                                # if yes
                                # b
                                # l
                                # D
                                # L
                                pass
                            pass
                        elif colors[index] == "red":
                            if indices == (0,1):
                                #check if green free
                                # if yes u
                                # if no check if red free
                                # if yes U B 2L
                                pass
                            elif indices == (1,0):
                                # if red free
                                # b
                                # u
                                # L
                                # U
                                # else F til red free
                                pass
                            elif indices == (1,2):
                                #2L and then liek 1,0
                                pass
                            elif indices == (2,1):
                                # L and then like 1,0 and 1,2
                                pass
                            pass
                        elif colors[index] == "green":
                            if indices == (0,1):
                                #check if green free
                                # B
                                # L
                                # u
                                # l
                                pass
                            elif indices == (1,0):
                                # if green free
                                # l
                                # b
                                # L
                                # 2U
                                pass
                            elif indices == (1,2):
                                # if green free
                                # R
                                # B
                                # r
                                # 2U
                                pass
                            elif indices == (2,1):
                                # if green free
                                # 2U
                                # and then like 0,1
                                pass
                        elif colors[index] == "yellow":
                            if indices == (0,1):
                                #check if blue is free
                                # 2D
                                # if not free do F
                                pass
                            elif indices == (1,0):
                                # if red free
                                # 2D
                                # if not free do F
                                pass
                            elif indices == (1,2):
                                # if orange free
                                # 2D
                                # if not free do F
                                pass
                            elif indices == (2,1):
                                # if green free
                                # 2D
                                # if not free do F
                                pass
                        else:
                            if indices == (0,1):
                                #check if green is free
                                # U
                                # if not free do F
                                pass
                            elif indices == (1,0):
                                # if green free
                                # R
                                # U
                                # if blue free
                                # r
                                # d
                                pass
                            elif indices == (1,2):
                                # if green free
                                # r
                                # U
                                # if blue free
                                # R
                                # d
                                pass
                            elif indices == (2,1):
                                # if blue free
                                # d
                                # if not free do F
                                pass
                        break
            index = (index+1) if not (index+1) == 5 else 0
            white_has_cross = self.check_white_cross()
            if white_has_cross:
                break
            
        #orientate white edges
        red_oriented = (self.cube["red"][1][2] == "R" and self.cube["white"][1][0] == "W")
        while not red_oriented:
            self.cube = self.mover.make_front(self.cube)
            red_oriented = (self.cube["red"][1][2] == "R" and self.cube["white"][1][0] == "W")

        blue_oriented = (self.cube["blue"][0][1] == "B" and self.cube["white"][2][1] == "W")
        orange_oriented = (self.cube["orange"][1][0] == "O" and self.cube["white"][1][2] == "W")
        if blue_oriented and not orange_oriented:
            # do one algo to switch orange and green
            pass
        elif not blue_oriented and orange_oriented:
            # do two algs to switch blue and green
            pass
        elif not blue_oriented and not orange_oriented:
            # do one algo to switch orange and blue
            pass

        
            
        
        # solve white corners
        white_is_full = self.check_side("white")    
        while not white_is_full:
            white_in_face = self.has_white_in_face(colors[index])
            if len(white_in_face) > 0:
                for indices in white_in_face:
                    if not self.is_edge_piece(indices):
                        #permute them to white
                        break
            index = (index+1) if not (index+1) == 5 else 0
            white_is_full = self.check_side("white")
            if white_is_full:
                break

        #orient white corners
        pass



    def start_solve(self):
        # find white edge pieces
        # move edge pieces to white face
        # permute the edges to the correct
        # find white corners and permute them to correct side
        # check second layer and permute them correctly (algorithm)
        # get the top cross
        pass

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
                if face[i][j] == "W" and not i == 1 and not j == 1:
                    indices.append((i,j))
        return indices

class UserInterface:
    def __init__(self, root, mover, cube):
        self.root = root
        self.mover = mover
        self.cube = cube
        self.create_move_buttons()    
        self.print_cube(self.cube)
        self.color_cycle = ['G', 'W', 'R', 'O', 'B', 'Y']

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

        self.solve_button = tk.Button(self.root, text= "Solve", command=lambda: self.solveCube())
        self.solve_button.place(x=60, y= 500)
        pass

    def solveCube(self):
        solver = RubiksCubeSolver(self.mover, self.cube)
        solver.start_solve()
        

    def get_color(self, color):
        return 'white' if color == "W" else 'red' if color == "R" else 'blue' if color == "B" else 'yellow' if color == "Y" else 'green' if color == "G" else 'orange'

    def changeColor(self, currentColor, currentSide, x, y):
        currentIndex = self.color_cycle.index(currentColor)
        nextIndex = currentIndex+1
        if nextIndex == len(self.color_cycle):
            nextIndex = 0
        self.cube[currentSide][x][y] = self.color_cycle[nextIndex]
        self.print_cube(self.cube)
        

    def print_cube(self, cube):
        self.print_face(cube["green"], 47, 0, "green")
        self.print_face(cube["red"], 0, 75, "red")
        self.print_face(cube["white"], 47, 75, "white")
        self.print_face(cube["orange"], 94, 75, "orange")
        self.print_face(cube["blue"], 47, 150, "blue")
        self.print_face(cube["yellow"], 47, 225, "yellow")

    def print_face(self, colors, gridX, gridY, side):
        tL = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][0]), command=lambda: self.changeColor(colors[0][0], side, 0, 0))
        tL.place(x=gridX, y=gridY)

        tM = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][1]), command=lambda: self.changeColor(colors[0][1], side, 0, 1))
        tM.place(x=gridX+15, y=gridY)

        tR = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][2]), command=lambda: self.changeColor(colors[0][2], side, 0, 2))
        tR.place(x=gridX+30, y=gridY)

        mL = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][0]), command=lambda: self.changeColor(colors[1][0], side, 1, 0))
        mL.place(x=gridX, y=gridY+25)

        mM = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][1]))
        mM.place(x=gridX+15, y=gridY+25)

        mR = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][2]), command=lambda: self.changeColor(colors[1][2], side, 1, 2))
        mR.place(x=gridX+30, y=gridY+25)

        bL = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][0]), command=lambda: self.changeColor(colors[2][0], side, 2, 0))
        bL.place(x=gridX, y=gridY+50)

        bM = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][1]), command=lambda: self.changeColor(colors[2][1], side, 2, 1))
        bM.place(x=gridX+15, y=gridY+50)

        bR = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][2]), command=lambda: self.changeColor(colors[2][2], side, 2, 2))
        bR.place(x=gridX+30, y=gridY+50)
        
    def moveButtonHandler(self, move):
        self.cube = self.mover.sort_move(move, self.cube)
        self.print_cube(self.cube)
        
def setupTesterInConsole():
    white = [["W" for row in range(3)] for line in range(3)]
    red = [["R" for row in range(3)] for line in range(3)]
    blue = [["B" for row in range(3)] for line in range(3)]
    green = [["G" for row in range(3)] for line in range(3)]
    yellow = [["Y" for row in range(3)] for line in range(3)]
    orange = [["O" for row in range(3)] for line in range(3)]

    cube = {
                'white': white,
                'red': red,
                'blue': blue,
                'green': green,
                'yellow': yellow,
                'orange': orange
            }

    tester = Tester()

    tester.test_Transformation('R', cube)

def setup_main_program():

    white = [["W" for row in range(3)] for line in range(3)]
    red = [["R" for row in range(3)] for line in range(3)]
    blue = [["B" for row in range(3)] for line in range(3)]
    green = [["G" for row in range(3)] for line in range(3)]
    yellow = [["Y" for row in range(3)] for line in range(3)]
    orange = [["O" for row in range(3)] for line in range(3)]

    cube = {
        'white': white,
        'red': red,
        'blue': blue,
        'green': green,
        'yellow':yellow,
        'orange': orange
    }

    root = tk.Tk()
    root.geometry('600x600')
    interface = UserInterface(root, Movemaker(), cube)

    root.mainloop()

setup_main_program()
