import enum
import random
import time
import tkinter as tk
from mover import Movemaker
import sys

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
    def __init__(self, mover, cube):
        self.moves = ["R", 'r', "R2", "L", "l", "L2", "U", "u", "U2", "D", "d", "D2", "B", "b", "B2", "F", "f", "F2"]
        self.cube = cube
        self.mover = mover
        self.moveString = ""
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
        return (self.cube[side][0][0] == self.cube[side][0][1] == self.cube[side][0][2] == self.cube[side][1][0] == self.cube[side][1][2] == self.cube[side][2][0] == self.cube[side][2][1] == self.cube[side][2][2] )

    def execute_moves(self, move_list):
        if len(move_list) == 1:
            self.cube = self.executeMove(move_list[0])
            self.moveString += " " + move_list[0] + " "
        elif not len(move_list) == 0:
            for move in move_list:
                self.cube = self.executeMove(move)
                self.moveString += " " + move + " "

    def front_moves_handler(self, front_moves):
        if front_moves == 1:
            self.execute_moves(["f"])
        elif front_moves == 2:
            self.execute_moves(["2F"])
        elif front_moves == 3:
            self.execute_moves(["F"])

    def solve_white_cross(self):
        #solve white edges
        colors = ["blue", "red", "green", "yellow", "orange"]
        white_has_cross = self.check_white_cross()
        index = 0
        solved = 0
        # solves white cross
        while not white_has_cross:
            white_in_face = self.has_white_in_face(self.cube[colors[index]])
            if len(white_in_face) > 0:
                for indices in white_in_face:
                    if self.is_edge_piece(indices):
                        if colors[index] == "blue":
                            if indices == (0,1):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["d", "L", "B", "l", "2D"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["d", "l"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["D", "2D", "R"])
                                else:
                                    self.execute_moves(["F", "d", "R"])
                            elif indices == (1,0):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["L", "B", "l", "2D"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["l"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["2D", "R"])
                                else:
                                    self.execute_moves(["F", "2D", "R"])
                            elif indices == (1,2):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["r", "b", "R", "2D"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["R"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["2D", "l"])
                                else:
                                    self.execute_moves(["D", "F", "R"])
                            elif indices == (2,1):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["D", "L", "B", "l", "2D"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["d", "R"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["D", "L", "d", "B", "2D"])
                                else:
                                    self.execute_moves(["F", "d", "R", "D"])
                        elif colors[index] == "red":
                            if indices == (0,1):
                                if not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["U", "B", "u", "2L"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["u"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["2L", "D", "2L"])
                                else:
                                    self.execute_moves(["l", "2B", "L", "2R"])
                            elif indices == (1,0):
                                if not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["b", "u", "L", "U"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["L", "u", "l"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["l", "D", "L"])
                                else:
                                    self.execute_moves(["b", "U", "r", "u"])
                            elif indices == (1,2):
                                self.execute_moves(["l", "U", "B", "u", "2L"])    
                            elif indices == (2,1):
                                if not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["d", "b", "2L"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["D"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["2L", "u", "2L"])
                                else:
                                    self.execute_moves(["d", "B", "D", "2R"])
                        elif colors[index] == "green":
                            if indices == (0,1):
                                if not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["B", "L", "u", "l"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["u", "L", "U"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["2U", "r", "2U"])
                                else:
                                    self.execute_moves(["U", "l", "D", "L"])
                            elif indices == (1,0):
                                if not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["f", "L", "F", "l"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["L"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["2U", "r", "2U"])
                                else:
                                    self.execute_moves(["F", "L", "F"])
                            elif indices == (1,2):
                                if not self.cube["white"][0][1]:
                                    self.execute_moves(["F", "r", "f"])
                                elif not self.cube["white"][1][2]:
                                    self.execute_moves(["r"])
                                elif not self.cube["white"][1][0]:
                                    self.execute_moves(["2U", "L", "2U"])
                                else:
                                    self.execute_moves(["f", "r", "F"])
                            elif indices == (2,1):
                                self.execute_moves(["2U", "B", "L", "u", "l"])
                        elif colors[index] == "yellow":
                            if indices == (0,1):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["2D"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["B", "2R"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["B", "2L"])
                                else:
                                    self.execute_moves(["2B", "2U"])
                            elif indices == (1,0):
                                if not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["2L"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["F", "2L", "f"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["f", "2L", "F"])
                                else:
                                    self.execute_moves(["2F", "2L", "2F"])
                            elif indices == (1,2):
                                if not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["2R"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["f", "2R", "F"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["F", "2R", "f"])
                                else:
                                    self.execute_moves(["2F", "2R", "2F"])
                            elif indices == (2,1):
                                if not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["2U"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["B", "2L"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["b", "2R"])
                                else:
                                    self.execute_moves(["2F", "2U", "2F"])
                        else:
                                if indices == (0,1):
                                    if not self.cube["white"][1][2] == "W":
                                        self.execute_moves(["f", "U", "F"])
                                    elif not self.cube["white"][0][1] == "W":
                                        self.execute_moves(["U"])
                                    elif not self.cube["white"][2][1] == "W":
                                        self.execute_moves(["2F", "U", "2F"])
                                    else:
                                        self.execute_moves(["F", "U", "f"])
                                elif indices == (1,0):
                                    self.execute_moves(["R", "f", "U", "F"])
                                elif indices == (1,2):
                                    if not self.cube["white"][1][2] == "W":
                                        self.execute_moves(["B", "U", "r", "u"])
                                    elif not self.cube["white"][0][1] == "W":
                                        self.execute_moves(["r", "U", "R"])
                                    elif not self.cube["white"][2][1] == "W":
                                        self.execute_moves(["R", "d", "r"])
                                    else:
                                        self.execute_moves(["B", "u", "L", "U"])
                                elif indices == (2,1):
                                    if not self.cube["white"][1][2] == "W":
                                        self.execute_moves(["F", "d", "f"])
                                    elif not self.cube["white"][2][1] == "W":
                                        self.execute_moves(["d"])
                                    elif not self.cube["white"][0][1] == "W":
                                        self.execute_moves(["2F", "d", "2F"])
                                    else:
                                        self.execute_moves(["f", "d", "F"])
                        solved += 1            
                        
            index = (index+1) if not (index+1) == 5 else 0
            white_has_cross = self.check_white_cross()
            if white_has_cross:
                break
            
        #orientate white edges
        while not (self.cube["red"][1][2] == "R" and self.cube["white"][1][0] == "W"):
            self.execute_moves(["F"])

        # blue edge is correct but orange edge is wrong
        if (self.cube["blue"][0][1] == "B" and self.cube["white"][2][1] == "W") and not (self.cube["orange"][1][0] == "O" and self.cube["white"][1][2] == "W"):
            self.execute_moves(["2R", "B", "2U", "b", "2R"])
        # blue is not oriented but orange is oriented
        elif not (self.cube["blue"][0][1] == "B" and self.cube["white"][2][1] == "W") and (self.cube["orange"][1][0] == "O" and self.cube["white"][1][2] == "W"):
            self.execute_moves(["2U", "2B", "2D", "2B", "2U"])
        # blue is not oriented and orange is not oriented
        elif not (self.cube["blue"][0][1] == "B" and self.cube["white"][2][1] == "W") and not (self.cube["orange"][1][0] == "O" and self.cube["white"][1][2] == "W"):
            if self.cube["blue"][0][1] == "G":
                # orange has blue and green has orange
                self.execute_moves(["F", "2L", "b", "2U", "B", "2L"])
            elif self.cube["blue"][0][1] == "O":
                # orange has green and green has blue
                self.execute_moves(["f", "2D", "b", "2L", "B", "2D"])
        
        # solve white corners  
        while not self.check_side("white")    :
            #checking every corner
            if self.cube["red"][2][2] == "W":
                self.execute_moves(["L", "B", "l", "b", "L", "B", "l"])
            elif self.cube["red"][0][2] == "W":
                self.execute_moves(["l", "b", "L", "B", "l", "b", "L"])
            elif self.cube["red"][0][0] == "W":
                frontMoves = 0
                while self.cube["white"][0][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1

                self.execute_moves(["l", "b", "L"])
                self.front_moves_handler(frontMoves)
            elif self.cube["red"][2][0] == "W":
                frontMoves = 0
                while self.cube["white"][2][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                self.execute_moves(["b", "d", "B", "D"])
                self.front_moves_handler(frontMoves)         
            elif self.cube["blue"][0][0] == "W":
                while not self.cube["white"][2][0] == "W":
                    self.execute_moves(["L", "B", "l", "b"])
            elif self.cube["blue"][0][2] == "W":
                while not self.cube["white"][2][2] == "W":
                    self.execute_moves(["r", "b", "R", "B"])
            elif self.cube["blue"][2][0] == "W":
                frontMoves = 0
                while self.cube["white"][2][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                self.execute_moves(["B", "L", "b", "l"])
                self.front_moves_handler(frontMoves)
            elif self.cube["blue"][2][2] == "W":
                frontMoves = 0
                while self.cube["white"][2][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                while not self.cube["white"][2][2] == "W":
                    self.execute_moves(["b", "r", "B", "R"])
                self.front_moves_handler(frontMoves)
            elif self.cube["orange"][0][0] == "W":
                while not self.cube["white"][0][2] == "W":
                    self.execute_moves(["R", "B", "r", "b"])
            elif self.cube["orange"][2][0] == "W":
                self.execute_moves(["r", "b", "R", "B", "r", "b", "R"])
            elif self.cube["orange"][0][2] == "W":
                frontMoves = 0
                while self.cube["white"][0][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                self.execute_moves(["R", "B", "r"])
                self.front_moves_handler(frontMoves)
            elif self.cube["orange"][2][2] == "W":
                frontMoves = 0
                while self.cube["white"][2][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                self.execute_moves(["r", "b", "R"])
                self.front_moves_handler(frontMoves)
            elif self.cube["green"][2][0] == "W":
                self.execute_moves(["U", "B", "u", "b", "U", "B", "u"])
            elif self.cube["green"][2][2] == "W":
                self.execute_moves(["u", "b", "U", "B", "u", "b", "U"])
            elif self.cube["green"][0][0] == "W":
                frontMoves = 0
                while self.cube["white"][0][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                self.execute_moves(["U", "B", "u"])
                self.front_moves_handler(frontMoves)
            elif self.cube["green"][0][2] == "W":
                frontMoves = 0
                while self.cube["white"][0][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                self.execute_moves(["u", "b", "U"])
                self.front_moves_handler(frontMoves)
            elif self.cube["yellow"][0][0] == "W":
                frontMoves = 0
                while self.cube["white"][2][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                while not self.cube["white"][2][0] == "W":
                    self.execute_moves(["L", "B", "l", "b"])
                self.front_moves_handler(frontMoves)
            elif self.cube["yellow"][0][2] == "W":
                frontMoves = 0
                while self.cube["white"][2][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                while not self.cube["white"][2][2] == "W":
                    self.execute_moves(["r", "b", "R", "B"])
                self.front_moves_handler(frontMoves)
            elif self.cube["yellow"][2][0] == "W":
                frontMoves = 0
                while self.cube["white"][0][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                while not self.cube["white"][0][0] == "W":
                    self.execute_moves(["l", "b", "L", "B"])
                self.front_moves_handler(frontMoves)
            elif self.cube["yellow"][2][2] == "W":
                frontMoves = 0
                while self.cube["white"][0][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                while not self.cube["white"][0][2] == "W":
                    self.execute_moves(["R", "B", "r", "b"])
                self.front_moves_handler(frontMoves)
        
        while not (self.cube["red"][1][2] == "R" and self.cube["white"][1][0] == "W"):
            self.execute_moves(["F"])
        self.moveString += " aligned edges\n"
        #orient white corners
        while not (self.cube["red"][0][2] == "R" and self.cube["green"][2][0] == "G"):
            if self.cube["red"][0][2] == "G" and self.cube["green"][2][0] == "O":
                self.execute_moves(["l", "b", "L", "R", "B", "r", "l", "b", "L"])
            elif self.cube["red"][0][2] == "O" and self.cube["green"][2][0] == "B":
                self.execute_moves(["l", "b", "L", "b", "D", "B", "d", "2B", "U", "b", "u"])
            elif self.cube["red"][0][2] == "B" and self.cube["green"][2][0] == "R":
                self.execute_moves(["U", "B", "u", "d", "b", "D", "U", "B", "u"])
        self.moveString += "RotGrün ecke nun richtig \n"
        
        while not (self.cube["red"][2][2] == "R" and self.cube["blue"][0][0] == "B"):
            if self.cube["red"][2][2] == "G" and self.cube["blue"][0][0] == "R":
                self.execute_moves(["U", "B", "u", "d", "b", "D", "U", "B", "u"])
            elif self.cube["red"][2][2] == "B" and self.cube["blue"][0][0] == "O":
                self.execute_moves(["L", "b", "l", "B", "D", "B", "d", "2B", "d", "b", "D"])
            elif self.cube["red"][2][2] == "O" and self.cube["blue"][0][0] == "G":
                self.execute_moves(["d", "b", "D", "b", "R", "B", "r", "B", "d", "b", "D"])
        self.moveString += "RotBlau ecke nun richtig\n"
        while not (self.cube["blue"][0][2] == "B" and self.cube["orange"][2][0] == "O"):
            if self.cube["blue"][0][2] == "O" and self.cube["orange"][2][0] == "G":
                self.execute_moves(["r", "B", "R", "B", "u", "b", "U", "D", "B", "d"])
            elif self.cube["blue"][0][2] == "G" and self.cube["orange"][2][0] == "R":
                self.execute_moves(["r", "B", "R", "2B", "l", "b", "L"])
            elif self.cube["blue"][0][2] == "R" and self.cube["orange"][2][0] == "B":
                self.execute_moves(["r", "b", "R", "L", "B", "l", "r", "b", "R"])
        self.moveString += "BlauOrange ecke nun richtig\n"
        while not (self.cube["green"][2][2] == "G" and self.cube["orange"][0][0] == "O"):
            if self.cube["green"][2][2] == "R" and self.cube["orange"][0][0] == "G":
                self.execute_moves(["R", "B", "r", "l", "b", "L", "R", "B", "r"])
            elif self.cube["green"][2][2] == "O" and self.cube["orange"][0][0] == "B":
                self.execute_moves(["R", "B", "r", "b", "D", "b", "d", "B", "R", "B", "r"])
            elif self.cube["green"][2][2] == "B" and self.cube["orange"][0][0] == "R":
                self.execute_moves(["R", "B", "r", "B", "d", "b", "D", "b", "R", "B", "r"])

        print(self.moveString)
        sys.exit()

    def start_solve(self):
        while not self.check_side("white"):
            self.solve_white_cross()
        

        # find white edge pieces
        # move edge pieces to white face
        # permute the edges to the correct
        # find white corners and permute them to correct side
        # check second layer and permute them correctly (algorithm)
        # get the top cross
        

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
        if move == "R":
            return self.mover.make_right(self.cube)
        elif move == "r":
            return self.mover.make_right(self.cube, inverted = True)
        elif move == "2R":
            return self.mover.make_right(self.mover.make_right(self.cube))
        elif move == "L":
            return self.mover.make_left(self.cube)
        elif move == "l":
            return self.mover.make_left(self.cube, inverted = True)
        elif move == "2L":
            return self.mover.make_left(self.mover.make_left(self.cube))
        elif move == "U":
            return self.mover.make_up(self.cube)
        elif move == "u":
            return self.mover.make_up(self.cube, inverted = True)
        elif move == "2U":
            return self.mover.make_up(self.mover.make_up(self.cube))
        elif move == "B":
            return self.mover.make_back(self.cube)
        elif move == "b":
            return self.mover.make_back(self.cube, inverted = True)
        elif move == "2B":
            return self.mover.make_back(self.mover.make_back(self.cube))
        elif move == "D":
            return self.mover.make_down(self.cube)
        elif move == "d":
            return self.mover.make_down(self.cube, inverted = True)
        elif move == "2D":
            return self.mover.make_down(self.mover.make_down(self.cube))
        elif move == "F":
            return self.mover.make_front(self.cube)
        elif move == "f":
            return self.mover.make_front(self.cube, inverted = True)
        elif move == "2F":
            return self.mover.make_front(self.mover.make_front(self.cube))
    
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
                if face[i][j] == "W" and not( i == 1 and j == 1 ):
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
        'white': [
            ["R", "Y", "G"],
            ["B", "W", "R"],
            ["W", "Y", "O"]
        ],
        'red': [
            ["O", "B", "B"],
            ["R", "R", "R"],
            ["W", "R", "G"]
        ],
        'blue': [
            ["R", "G", "W"],
            ["Y", "B", "G"],
            ["B", "Y", "G"]
        ],
        'green': [
            ["B", "B", "O"],
            ["W", "G", "O"],
            ["Y", "B", "Y"]
        ],
        'yellow': [
            ["R", "O", "Y"],
            ["G", "Y", "O"],
            ["Y", "O", "W"]
        ],
        'orange': [
            ["O", "G", "G"],
            ["W", "O", "W"],
            ["B", "W", "R"]
        ]
    }

    root = tk.Tk()
    root.geometry('600x600')
    interface = UserInterface(root, Movemaker(), cube)

    root.mainloop()

setup_main_program()
