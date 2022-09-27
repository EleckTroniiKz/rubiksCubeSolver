import tkinter as tk
from mover import Movemaker
from helper import RubiksHelper

class RubiksCubeSolver:
    def __init__(self, mover, cube):
        self.moves = ["R", 'r', "R2", "L", "l", "L2", "U", "u", "U2", "D", "d", "D2", "B", "b", "B2", "F", "f", "F2"]
        self.cube = cube
        self.mover = mover
        self.moveString = ""
        self.movesToSolveWhiteCross = ""
        self.movesToSolveWhiteFace = ""
        self.movesToSolveSecondLayer = ""
        self.movesToSolveYellowCross = ""
        self.movesToSolveYellowEdges = ""
        self.movesToSolveYellowCorners = ""
        self.startTime = None
        self.endTime = None
    
    def get_cross_phase(self) -> int:
        """ returns Integer according to current CrossPhase """
        
        # There are 4 cross phases. cross (3), Line (2), L-Shape(1), or just dot(0)
        if self.cube["yellow"][0][1] == self.cube["yellow"][2][1] == self.cube["yellow"][1][0] == self.cube["yellow"][1][2] == "Y":
            return 3
        elif self.cube["yellow"][0][1] == self.cube["yellow"][2][1] == "Y" or self.cube["yellow"][1][0] == self.cube["yellow"][1][2] == "Y":
            return 2
        elif self.cube["yellow"][0][1] == self.cube["yellow"][1][0] == "Y":
            return 1 
        else:
            return 0

    def create_yellow_cross(self) -> None:
        """ permute the current cube to the state, where a yellow cross has formed """ 
        hasCross = False
        
        while not hasCross:
            currentPhase = self.get_cross_phase()
            if currentPhase == 0:
                # L Shape (top to right)
                if self.cube["yellow"][0][1] == self.cube["yellow"][1][2] == "Y":
                    self.execute_moves(["b"])
                    self.execute_moves(["U", "R", "B", "r", "b", "u"])
                # L Shape (right to bottom)
                elif self.cube["yellow"][1][2] == self.cube["yellow"][2][1] == "Y":
                    self.execute_moves(["2B"])
                    self.execute_moves(["U", "R", "B", "r", "b", "u"])
                # L Shape (left to bottom)
                elif self.cube["yellow"][1][0] == self.cube["yellow"][2][1] == "Y":
                    self.execute_moves(["B"])
                    self.execute_moves(["U", "R", "B", "r", "b", "u"])
                # L Shape (left to top)
                else:
                    self.execute_moves(["U", "R", "B", "r", "b", "u"])
            elif currentPhase == 1:
                # L shape correct -> after algorithm yellow has a Phase 2 Line
                self.execute_moves(["U", "R", "B", "r", "b", "u"])
            elif currentPhase == 2:
                # Line -> after algorithm there will be a yellow cross
                while not self.cube["yellow"][1][0] == self.cube["yellow"][1][2] == "Y":
                    self.execute_moves(["B"])
                self.execute_moves(["U", "R", "B", "r", "b", "u"])
            else:
                hasCross = True
                # yellow cross has been created at this point
                return
                
    def check_white_cross(self) -> bool:
        """ true, if white cross is present on white layer """
        return (self.cube["white"][0][1] == self.cube["white"][1][0] == self.cube["white"][1][2] == self.cube["white"][2][1] == "W")

    def check_side(self, side: str) -> bool:
        """ controls if a given side, is solved or not """
        return (self.cube[side][0][0] == self.cube[side][0][1] == self.cube[side][0][2] == self.cube[side][1][0] == self.cube[side][1][2] == self.cube[side][2][0] == self.cube[side][2][1] == self.cube[side][2][2] )

    def execute_moves(self, move_list: list) -> None:
        """ executes and adds moves from move_list to move String """
        if len(move_list) == 1:
            self.cube = self.executeMove(move_list[0])
            self.moveString += " " + move_list[0] + " "
        elif not len(move_list) == 0:
            for move in move_list:
                self.cube = self.executeMove(move)
                self.moveString += " " + move + " "

    def front_moves_handler(self, front_moves: int) -> None:
        """ sorts amount of front_moves to reverse done moves. """
        if front_moves == 1:
            self.execute_moves(["f"])
        elif front_moves == 2:
            self.execute_moves(["2F"])
        elif front_moves == 3:
            self.execute_moves(["F"])

    def orientate_white_edges(self) -> None:
        """ sort white edges """
        # blue edge is correct but orange edge is wrong
        if (self.cube["blue"][0][1] == "B" and self.cube["white"][2][1] == "W") and not (self.cube["orange"][1][0] == "O" and self.cube["white"][1][2] == "W"):
            self.execute_moves(["2R", "B", "2U", "b", "2R"])
        # blue is not oriented but orange is oriented
        elif not (self.cube["blue"][0][1] == "B" and self.cube["white"][2][1] == "W") and (self.cube["orange"][1][0] == "O" and self.cube["white"][1][2] == "W"):
            self.execute_moves(["2U", "2B", "2D", "2B", "2U"])
        # blue is not oriented and orange is not oriented
        elif not (self.cube["blue"][0][1] == "B" and self.cube["white"][2][1] == "W") and not (self.cube["orange"][1][0] == "O" and self.cube["white"][1][2] == "W"):
            if self.cube["blue"][0][1] == "G":
                if self.cube["orange"][1][0] == "O":
                    self.execute_moves(["2D", "2U", "2B", "2U", "2B", "2D"])
                elif self.cube["orange"][1][0] == "B":
                    self.execute_moves(["2D", "2B", "2U", "b" ,"2R", "b", "2D"])
            elif self.cube["blue"][0][1] == "O":
                if self.cube["orange"][1][0] == "B":
                    self.execute_moves(["2D", "B", "2R", "b", "2D"])
                elif self.cube["orange"][1][0] == "G":
                    self.execute_moves(["f", "2D", "b", "2L", "B", "2D"])

    def solve_white_corners(self) -> None:     
        """ solve the white corners """

        while not self.check_side("white"):
            # check white pieces in red side
            if self.cube["red"][2][2] == "W":
                # white piece at bottom right in red side
                self.execute_moves(["L", "B", "l", "b", "L", "B", "l"])
            elif self.cube["red"][0][2] == "W":
                # white piece at top right in red side
                self.execute_moves(["l", "b", "L", "B", "l", "b", "L"])
            elif self.cube["red"][0][0] == "W":
                # white piece at top left in red side
                frontMoves = 0
                while self.cube["white"][0][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                self.execute_moves(["l", "b", "L"])
                self.front_moves_handler(frontMoves)
            elif self.cube["red"][2][0] == "W":
                # white piece at bottom left in red side
                frontMoves = 0
                while self.cube["white"][2][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                self.execute_moves(["b", "d", "B", "D"])
                self.front_moves_handler(frontMoves)         
            
            # check white pieces in blue side
            elif self.cube["blue"][0][0] == "W":
                # white piece at top left in blue side
                while not self.cube["white"][2][0] == "W":
                    self.execute_moves(["L", "B", "l", "b"])
            elif self.cube["blue"][0][2] == "W":
                # white piece at top right in blue side
                while not self.cube["white"][2][2] == "W":
                    self.execute_moves(["r", "b", "R", "B"])
            elif self.cube["blue"][2][0] == "W":
                # white piece at bottom left in blue side
                frontMoves = 0
                while self.cube["white"][2][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                self.execute_moves(["B", "L", "b", "l"])
                self.front_moves_handler(frontMoves)
            elif self.cube["blue"][2][2] == "W":
                # white piece at bottom right in blue side
                frontMoves = 0
                while self.cube["white"][2][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                while not self.cube["white"][2][2] == "W":
                    self.execute_moves(["b", "r", "B", "R"])
                self.front_moves_handler(frontMoves)
            
            # check white pieces in orange side
            elif self.cube["orange"][0][0] == "W":
                # white piece at top left in orange side
                while not self.cube["white"][0][2] == "W":
                    self.execute_moves(["R", "B", "r", "b"])
            elif self.cube["orange"][2][0] == "W":
                # white piece at bottom left in orange side
                self.execute_moves(["r", "b", "R", "B", "r", "b", "R"])
            elif self.cube["orange"][0][2] == "W":
                # white piece at top right in orange side
                frontMoves = 0
                while self.cube["white"][0][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                self.execute_moves(["R", "B", "r"])
                self.front_moves_handler(frontMoves)
            elif self.cube["orange"][2][2] == "W":
                # white piece at bottom right in orange side
                frontMoves = 0
                while self.cube["white"][2][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                self.execute_moves(["r", "b", "R"])
                self.front_moves_handler(frontMoves)
            
            # check white pieces in red side
            elif self.cube["green"][2][0] == "W":
                # white piece at bottom left in green side
                self.execute_moves(["U", "B", "u", "b", "U", "B", "u"])
            elif self.cube["green"][2][2] == "W":
                # white piece at bottom right in green side
                self.execute_moves(["u", "b", "U", "B", "u", "b", "U"])
            elif self.cube["green"][0][0] == "W":
                # white piece at top left in green side
                frontMoves = 0
                while self.cube["white"][0][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                self.execute_moves(["U", "B", "u"])
                self.front_moves_handler(frontMoves)
            elif self.cube["green"][0][2] == "W":
                # white piece at top right in green side
                frontMoves = 0
                while self.cube["white"][0][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                self.execute_moves(["u", "b", "U"])
                self.front_moves_handler(frontMoves)
            
            # check white pieces in yellow side
            elif self.cube["yellow"][0][0] == "W":
                # white piece at top left in yellow side
                frontMoves = 0
                while self.cube["white"][2][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                while not self.cube["white"][2][0] == "W":
                    self.execute_moves(["L", "B", "l", "b"])
                self.front_moves_handler(frontMoves)
            elif self.cube["yellow"][0][2] == "W":
                # white piece at top right in yellow side
                frontMoves = 0
                while self.cube["white"][2][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                while not self.cube["white"][2][2] == "W":
                    self.execute_moves(["r", "b", "R", "B"])
                self.front_moves_handler(frontMoves)
            elif self.cube["yellow"][2][0] == "W":
                # white piece at bottom left in yellow side
                frontMoves = 0
                while self.cube["white"][0][0] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                while not self.cube["white"][0][0] == "W":
                    self.execute_moves(["l", "b", "L", "B"])
                self.front_moves_handler(frontMoves)
            elif self.cube["yellow"][2][2] == "W":
                # white piece at bottom right in yellow side
                frontMoves = 0
                while self.cube["white"][0][2] == "W":
                    self.execute_moves(["F"])
                    frontMoves += 1
                
                while not self.cube["white"][0][2] == "W":
                    self.execute_moves(["R", "B", "r", "b"])
                self.front_moves_handler(frontMoves)   

    def solve_to_white_cross(self) -> None:
        """ solving a white cross """
        colors = ["blue", "red", "green", "yellow", "orange"]
        white_has_cross = self.check_white_cross()
        index = 0
        solved = 0
        # solves white cross
        while not white_has_cross:
            # receives list of index-tuples, where a white piece is located
            white_in_face = self.has_white_in_face(self.cube[colors[index]])
            if len(white_in_face) > 0:
                for indices in white_in_face:
                    if self.is_edge_piece(indices):
                        # white piece is in blue side
                        if colors[index] == "blue":
                            # white piece is located in the top middle
                            if indices == (0,1):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["d", "L", "B", "l", "2D"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["d", "l"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["D", "2D", "R"])
                                else:
                                    self.execute_moves(["F", "d", "R"])
                            # white piece is located in the left middle
                            elif indices == (1,0):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["L", "B", "l", "2D"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["l"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["2D", "R"])
                                else:
                                    self.execute_moves(["F", "2D", "R"])
                            # white piece is located in the right middle
                            elif indices == (1,2):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["r", "b", "R", "2D"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["R"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["2D", "l"])
                                else:
                                    self.execute_moves(["D", "F", "R"])
                            # white piece is located in the bottom middle
                            elif indices == (2,1):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["D", "L", "B", "l", "2D"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["d", "R"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["D", "L", "d", "B", "2D"])
                                else:
                                    self.execute_moves(["F", "d", "R", "D"])
                        # white piece is in red side
                        elif colors[index] == "red":
                            # white piece is located in the top middle
                            if indices == (0,1):
                                if not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["U", "B", "u", "2L"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["u"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["2L", "D", "2L"])
                                else:
                                    self.execute_moves(["l", "2B", "L", "2R"])
                            # white piece is located in the left middle
                            elif indices == (1,0):
                                if not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["b", "u", "L", "U"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["L", "u", "l"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["l", "D", "L"])
                                else:
                                    self.execute_moves(["b", "U", "r", "u"])
                            # white piece is located in the right middle
                            elif indices == (1,2):
                                self.execute_moves(["l", "U", "B", "u", "2L"])    
                            # white piece is located in the bottom middle
                            elif indices == (2,1):
                                if not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["d", "b", "2L"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["D"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["2L", "u", "2L"])
                                else:
                                    self.execute_moves(["d", "B", "D", "2R"])
                        # white piece is in green side
                        elif colors[index] == "green":
                            # white piece is located in the top middle
                            if indices == (0,1):
                                if not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["B", "L", "u", "l"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["u", "L", "U"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["2U", "r", "2U"])
                                else:
                                    self.execute_moves(["b", "R", "d", "r"])
                            # white piece is located in the left middle
                            elif indices == (1,0):
                                if not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["f", "L", "F", "l"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["L"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["2U", "r", "2U"])
                                else:
                                    self.execute_moves(["F", "L", "F"])
                            # white piece is located in the right middle
                            elif indices == (1,2):
                                if not self.cube["white"][0][1]:
                                    self.execute_moves(["F", "r", "f"])
                                elif not self.cube["white"][1][2]:
                                    self.execute_moves(["r"])
                                elif not self.cube["white"][1][0]:
                                    self.execute_moves(["2U", "L", "2U"])
                                else:
                                    self.execute_moves(["f", "r", "F"])
                            # white piece is located in the bottom middle
                            elif indices == (2,1):
                                self.execute_moves(["2U", "B", "L", "u", "l"])
                        # white piece is in yellow side
                        elif colors[index] == "yellow":
                            # white piece is located in the top middle
                            if indices == (0,1):
                                if not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["2D"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["B", "2R"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["B", "2L"])
                                else:
                                    self.execute_moves(["2B", "2U"])
                            # white piece is located in the left middle
                            elif indices == (1,0):
                                if not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["2L"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["F", "2L", "f"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["f", "2L", "F"])
                                else:
                                    self.execute_moves(["2F", "2L", "2F"])
                            # white piece is located in the right middle
                            elif indices == (1,2):
                                if not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["2R"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["f", "2R", "F"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["F", "2R", "f"])
                                else:
                                    self.execute_moves(["2F", "2R", "2F"])
                            # white piece is located in the bottom middle
                            elif indices == (2,1):
                                if not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["2U"])
                                elif not self.cube["white"][1][0] == "W":
                                    self.execute_moves(["B", "2L"])
                                elif not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["b", "2R"])
                                else:
                                    self.execute_moves(["2F", "2U", "2F"])
                        # white piece is in orange side
                        else:
                            # white piece is located in the top middle
                            if indices == (0,1):
                                if not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["f", "U", "F"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["U"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["2F", "U", "2F"])
                                else:
                                    self.execute_moves(["F", "U", "f"])
                            # white piece is located in the left middle
                            elif indices == (1,0):
                                self.execute_moves(["R", "f", "U", "F"])
                            # white piece is located in the right middle
                            elif indices == (1,2):
                                if not self.cube["white"][1][2] == "W":
                                    self.execute_moves(["B", "U", "r", "u"])
                                elif not self.cube["white"][0][1] == "W":
                                    self.execute_moves(["r", "U", "R"])
                                elif not self.cube["white"][2][1] == "W":
                                    self.execute_moves(["R", "d", "r"])
                                else:
                                    self.execute_moves(["B", "u", "L", "U"])
                            # white piece is located in the bottom middle
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
                        break          

            # cycle through all colors. If end is reached -> set to 0        
            index = (index+1) if not (index+1) == 5 else 0
            
            if self.check_white_cross():
                break
        
    def orientate_white_corners(self) -> None:
        """ orientate white corners """

        # While the corner, where Red and Green should be, is not solved
        while not (self.cube["red"][0][2] == "R" and self.cube["green"][2][0] == "G"):
            # green-orange corner
            if self.cube["red"][0][2] == "G" and self.cube["green"][2][0] == "O":
                self.execute_moves(["l", "b", "L", "R", "B", "r", "l", "b", "L"])
            # orange-blue corner
            elif self.cube["red"][0][2] == "O" and self.cube["green"][2][0] == "B":
                self.execute_moves(["l", "b", "L", "b", "D", "B", "d", "2B", "U", "b", "u"])
            # red-blue corner
            elif self.cube["red"][0][2] == "B" and self.cube["green"][2][0] == "R":
                self.execute_moves(["U", "B", "u", "d", "b", "D", "U", "B", "u"])
        # While the corner, where Red and Blue should be, is not solved
        while not (self.cube["red"][2][2] == "R" and self.cube["blue"][0][0] == "B"):
            # red-green corner
            if self.cube["red"][2][2] == "G" and self.cube["blue"][0][0] == "R":
                self.execute_moves(["U", "B", "u", "d", "b", "D", "U", "B", "u"])
            # orange-blue corner
            elif self.cube["red"][2][2] == "B" and self.cube["blue"][0][0] == "O":
                self.execute_moves(["L", "b", "l", "B", "D", "B", "d", "2B", "d", "b", "D"])
            # green-orange corner
            elif self.cube["red"][2][2] == "O" and self.cube["blue"][0][0] == "G":
                self.execute_moves(["d", "b", "D", "b", "R", "B", "r", "B", "d", "b", "D"])
        # While the corner, where Blue and Orange should be, is not solved
        while not (self.cube["blue"][0][2] == "B" and self.cube["orange"][2][0] == "O"):
            # green-orange corner
            if self.cube["blue"][0][2] == "O" and self.cube["orange"][2][0] == "G":
                self.execute_moves(["r", "B", "R", "B", "u", "b", "U", "D", "B", "d"])
            # red-green corner
            elif self.cube["blue"][0][2] == "G" and self.cube["orange"][2][0] == "R":
                self.execute_moves(["r", "B", "R", "2B", "l", "b", "L", "b", "D", "B", "d"])
            # red-blue corner
            elif self.cube["blue"][0][2] == "R" and self.cube["orange"][2][0] == "B":
                self.execute_moves(["r", "b", "R", "L", "B", "l", "r", "b", "R"])
        # While the corner, where Green and Orange should be, is not solved
        while not (self.cube["green"][2][2] == "G" and self.cube["orange"][0][0] == "O"):
            # red-green corner
            if self.cube["green"][2][2] == "R" and self.cube["orange"][0][0] == "G":
                self.execute_moves(["R", "B", "r", "l", "b", "L", "R", "B", "r"])
            # orange-blue corner
            elif self.cube["green"][2][2] == "O" and self.cube["orange"][0][0] == "B":
                self.execute_moves(["R", "B", "r", "b", "D", "b", "d", "B", "R", "B", "r"])
            # red-blue corner
            elif self.cube["green"][2][2] == "B" and self.cube["orange"][0][0] == "R":
                self.execute_moves(["R", "B", "r", "B", "d", "b", "D", "b", "R", "B", "r"])

    def solve_white_side(self) -> None:
        """ permutes the current cube in a way, so that the white side is solved """

        self.solve_to_white_cross()

        #orientate white edges
        while not (self.cube["red"][1][2] == "R" and self.cube["white"][1][0] == "W"):
            self.execute_moves(["F"])
        
        self.orientate_white_edges()
        self.solve_white_corners()
        
        while not (self.cube["red"][1][2] == "R" and self.cube["white"][1][0] == "W"):
            self.execute_moves(["F"])

        #orient white corners
        self.orientate_white_corners()
        
    def get_cube(self) -> dict:
        """ return current cube"""
        return self.cube

    def finished_second_layer(self) -> bool:
        """ check if the seconmd layer has been solved correctly """
        return ((self.cube["red"][1][0] == "Y" or self.cube["yellow"][1][0] == "Y") and (self.cube["blue"][2][1] == "Y" or self.cube["yellow"][0][1] == "Y") and (self.cube["green"][0][1] == "Y" or self.cube["yellow"][2][1] == "Y") and (self.cube["orange"][1][2] == "Y" or self.cube["yellow"][1][2] == "Y")) \
            and ((self.cube["red"][0][1] == "R" and self.cube["green"][1][0] == "G") and (self.cube["red"][2][1] == "R" or self.cube["blue"][1][0] == "B") and (self.cube["blue"][1][2] == "B" and self.cube["orange"][2][1] == "O") and (self.cube["orange"][0][1] == "O" and self.cube["green"][1][2] == "G")) 

    def solve_second_layer(self) -> None:
        """ permute the cube, so that the second layer of the cube is solved """

        red_green_edge, red_blue_edge, orange_green_edge, orange_blue_edge = False, False, False, False
        old_correct = 0
        current_correct = 0
        
        while not self.finished_second_layer():
            # red-green-edge not solved
            if not red_green_edge:
                # red-edge correct, but wrong at green side
                if self.cube["red"][0][1] == "R" and not self.cube["green"][1][0] == "Y":
                    # red-blue edge
                    if self.cube["green"][1][0] == "B":
                        self.execute_moves(["U", "b", "u", "b", "l", "B", "L", "L", "b", "l", "b", "d", "B", "D"])
                        red_blue_edge = True 
                        current_correct += 1
                # red-edge either green blue, red at green side
                elif (self.cube["red"][0][1] == "B" or self.cube["red"][0][1] == "G") and self.cube["green"][1][0] == "R":
                    # blue-red edge
                    if self.cube["red"][0][1] == "B":
                        self.execute_moves(["U", "b", "u", "b", "l", "B", "L"])
                        if self.cube["yellow"][1][2] == "B":
                            self.execute_moves(["B", "d", "B", "D", "B", "L", "b", "l"])
                        elif self.cube["yellow"][1][2] == "R":
                            self.execute_moves(["L", "b", "l", "b", "d", "B", "D"])
                        red_blue_edge = True
                        current_correct += 1
                    # green-red edge
                    else:
                        self.execute_moves(["U", "b", "u", "b", "l", "B", "L", "b", "U", "b", "u", "b", "l", "B", "L"])
                        red_green_edge = True
                        current_correct += 1
                # red-edge is blue, green edge is orange
                elif (self.cube["red"][0][1] == "B" and self.cube["green"][1][0] == "O"):
                    self.execute_moves(["U", "b", "u", "b", "l", "B", "L", "B", "D", "b", "d", "b", "r", "B", "R"])
                    orange_blue_edge = True
                    current_correct += 1
                # red-edge is green, green edge is orange
                elif (self.cube["red"][0][1] == "G" and self.cube["green"][1][0] == "O"):
                    self.execute_moves(["U", "b", "u", "b", "l", "B", "L", "b", "u", "B", "U", "B", "R", "b", "r"])
                    orange_green_edge = True
                    current_correct += 1
                # red-edge is orange, green edge is either green ord blue
                elif (self.cube["red"][0][1] == "O") and not self.cube["green"][1][0] == "Y":
                    # orange-green edge
                    if self.cube["green"][1][0] == "G":
                        self.execute_moves(["U", "b", "u", "b", "l", "B", "L", "2B", "R", "b", "r", "b", "u", "B", "U"])
                        orange_green_edge = True
                        current_correct += 1
                    # orange-blue edge
                    elif self.cube["green"][1][0] == "B":
                        self.execute_moves(["U", "b", "u", "b", "l", "B", "L", "2B", "r", "B", "R", "B", "D", "b", "d"])
                        orange_blue_edge = True
                        current_correct += 1
            # red-blue-edge not solved
            if not red_blue_edge:
                # red edge correct, but wrong at blue side
                if (self.cube["red"][2][1] == "R") and not self.cube["blue"][1][0] == "Y":
                    # red-green edge
                    if self.cube["blue"][1][0] == "G":
                        self.execute_moves(["L", "b", "l", "b", "d", "B", "D", "2B", "U", "b", "u", "b", "l", "B", "L"])
                        red_green_edge = True
                        current_correct += 1
                # red has green, blue is wrong but not yellow
                elif self.cube["red"][2][1] == "G" and not self.cube["blue"][1][0] == "Y":
                    # green-red edge
                    if self.cube["blue"][1][0] == "R":
                        self.execute_moves(["L", "b", "l", "b", "d", "B", "D", "b", "l", "B", "L", "B", "U", "b", "u"])
                        red_green_edge = True
                        current_correct += 1
                    # green-orange edge
                    elif self.cube["blue"][1][0] == "O":
                        self.execute_moves(["L", "b", "l", "b", "d", "B", "D", "B", "R", "b", "r", "b", "u", "B", "U"])
                        orange_green_edge = True
                        current_correct += 1
                # red has blue, blue is wrong but not yellow
                elif self.cube["red"][2][1] == "B" and not self.cube["blue"][1][0] == "Y":
                    # blue-orange edge
                    if self.cube["blue"][1][0] == "O":
                        self.execute_moves(["L", "b", "l", "b", "d", "B", "D", "b", "L", "b", "l", "b", "d", "B", "D"])
                        orange_blue_edge = True
                        current_correct += 1
                    # blue-red edge
                    elif self.cube["blue"][1][0] == "R":
                        self.execute_moves(["L", "b", "l", "b", "d", "B", "D", "b", "L", "b", "l", "b", "d", "B", "D"])
                        red_blue_edge = True
                        current_correct += 1
                # red has orange, blue is wrong but has not yellow
                elif self.cube["red"][2][1] == "O" and not self.cube["blue"][1][0] == "Y":
                    # orange-blue edge
                    if self.cube["blue"][1][0] == "B":
                        self.execute_moves(["L", "b", "l", "b", "d", "B", "D", "D", "b", "d" ,"b", "r", "B", "R"])
                        orange_blue_edge = True
                        current_correct += 1
                    # orange-green edge
                    elif self.cube["blue"][1][0] == "G":
                        self.execute_moves(["L", "b", "l", "b", "d", "B", "D", "2B", "U", "B", "u", "B", "R", "b", "r"])
                        orange_green_edge = True
                        current_correct += 1
            # orange-blue-edge is wrong
            if not orange_blue_edge:
                # blue is correct, but orange is wrong and not yellow
                if self.cube["blue"][1][2] == "B" and not self.cube["orange"][2][1] == "Y":
                    # blue-red edge
                    if self.cube["orange"][2][1] == "R":
                        self.execute_moves(["D", "b", "d", "b", "r", "B", "R", "2B", "L", "b", "l", "b", "d", "B", "D" ])
                        red_blue_edge = True
                        current_correct += 1
                # blue is red, but orange is wrong and not yellow
                elif self.cube["blue"][1][2] == "R" and not self.cube["orange"][2][1] == "Y":
                    # red-blue edge
                    if self.cube["orange"][2][1] == "B":
                        self.execute_moves(["r", "B", "R", "B", "D", "b", "d", "b", "L", "b", "l", "b", "d", "B", "D" ])
                        red_blue_edge = True
                        current_correct += 1
                    # red-green edge
                    elif self.cube["orange"][2][1] == "G":
                        self.execute_moves(["B", "D", "b", "d", "b", "r", "B", "R", "B", "U", "b", "u", "b", "l", "B", "L"])
                        red_green_edge = True
                        current_correct += 1
                # blue is orange, but orange is wrong and not yellow
                elif self.cube["blue"][1][2] == "O" and not self.cube["orange"][2][1] == "Y":
                    # orange-blue edge
                    if self.cube["orange"][2][1] == "B":
                        self.execute_moves(["r", "B", "R", "B", "D", "b", "d", "B", "r", "B", "R", "B", "D", "b", "d"])
                        orange_blue_edge = True
                        current_correct += 1
                    # orange-green edge
                    elif self.cube["orange"][2][1] == "G":
                        self.execute_moves(["r", "B", "R", "B", "D", "b", "d", "B", "R", "b", "r", "b", "u", "B", "U"])
                        orange_green_edge = True
                        current_correct += 1
                # blue is green, and orange is wrong and not yellow
                elif self.cube["blue"][1][2] == "G" and not self.cube["orange"][2][1] == "Y":
                    # green-red edge
                    if self.cube["orange"][2][1] == "R":
                        self.execute_moves(["r", "B", "R", "B", "D", "b", "d", "2B", "U", "b", "u", "b", "l", "B", "L"])
                        red_green_edge = True
                        current_correct += 1
                    # green-orange edge
                    elif self.cube["orange"][2][1] == "O":
                        self.execute_moves(["r", "B", "R", "B", "D", "b", "d", "2B", "u", "B", "U", "B", "R", "b", "r"])
                        orange_green_edge = True
                        current_correct += 1
            # orange-green-edge is wrong
            if not orange_green_edge:
                # orange is correct, green is blue
                if self.cube["orange"][0][1] == "O" and self.cube["green"][1][2] == "B":
                    self.execute_moves(["R", "b", "r", "b", "u", "B", "U", "2B", "D", "b", "d", "b", "r", "B", "R"])
                    orange_blue_edge = True
                    current_correct += 1
                # orange is green and green is not correct and not yellow
                elif self.cube["orange"][0][1] == "G" and not self.cube["green"][1][2] == "Y":
                    #green-red edge
                    if self.cube["green"][1][2] == "R":
                        self.execute_moves(["R", "b", "r", "b", "u", "B", "U", "B", "l", "B", "L", "B", "U", "b", "u"]) 
                        red_green_edge = True
                        current_correct += 1
                    #green-orange edge
                    elif self.cube["green"][1][2] == "O":
                        self.execute_moves(["R", "b", "r", "b", "u", "B", "U", "b", "R", "b", "r", "b", "u", "B", "U"])
                        orange_green_edge = True
                        current_correct += 1
                # orange is blue and green is not correct and not yellow
                elif self.cube["orange"][0][1] == "B" and not self.cube["green"][1][2] == "Y":
                    # blue-red edge
                    if self.cube["green"][1][2] == "R":
                        self.execute_moves(["R", "b", "r", "b", "u", "B", "U", "B", "L", "b", "l", "b", "d", "B", "D"])
                        red_blue_edge = True
                        current_correct += 1
                    # blue-orange edge
                    elif self.cube["green"][1][2] == "O":
                        self.execute_moves(["R", "b", "r", "b", "u", "B", "U", "b", "r", "B", "R", "B", "D", "b", "d"])
                        orange_blue_edge = True
                        current_correct += 1
                # orange is red, and green is not correct and not yellow
                elif self.cube["orange"][0][1] == "R" and not self.cube["green"][1][2] == "Y":
                    # red-blue edge
                    if self.cube["green"][1][2] == "B":
                        self.execute_moves(["R", "b", "r", "b", "u", "B", "U", "2B", "d", "B", "D", "B", "L", "b", "l"])
                        orange_green_edge = True
                        current_correct += 1
                    # red-green edge
                    elif self.cube["green"][1][2] == "G":
                        self.execute_moves(["R", "b", "r", "b", "u", "B", "U", "U", "b", "u", "b", "l", "B", "L"])
                        red_green_edge = True
                        current_correct += 1
            
            # old_correct < current_correct -> in latest iteration one edge has been solved 
            if old_correct < current_correct:
                old_correct = current_correct
            # old_correct == current_correct -> in latest iteration no edge has been solved further. Must break out of loop, else infinite loop
            elif old_correct == current_correct:
                break
        
        # iteration checks for edge pieces located at the color|yellow edge
        while not self.finished_second_layer():
            # non yellow edge piece located at red-yellow edge
            if not self.cube["red"][1][0] == "Y" and not self.cube["yellow"][1][0] == "Y":
                # part red edge
                if self.cube["red"][1][0] == "R":
                    # red-blue edge
                    if self.cube["yellow"][1][0] == "B":
                        self.execute_moves(["b", "d", "B", "D", "B", "L", "b", "l"])
                    # red-green edge
                    elif self.cube["yellow"][1][0] == "G":
                        self.execute_moves(["B", "U", "b", "u", "b", "l", "B", "L"])
                # part blue edge
                elif self.cube["red"][1][0] == "B":
                    # blue-red edge
                    if self.cube["yellow"][1][0] == "R":
                        self.execute_moves(["2B" , "L", "b", "l", "b", "d", "B", "D"])
                    # blue-orange edge
                    elif self.cube["yellow"][1][0] == "O":
                        self.execute_moves(["r", "B", "R", "B", "D", "b", "d"])
                # part green edge
                elif self.cube["red"][1][0] == "G":
                    # green-red edge
                    if self.cube["yellow"][1][0] == "R":
                        self.execute_moves(["2B", "l", "B", "L", "B", "U", "b", "u"])
                    # green-orange edge
                    elif self.cube["yellow"][1][0] == "O":
                        self.execute_moves(["R", "b", "r", "b", "u", "B", "U"])
                # part orange edge
                elif self.cube["red"][1][0] == "O":
                    # orange-green edge
                    if self.cube["yellow"][1][0] == "G":
                        self.execute_moves(["B", "u", "B", "U", "B", "R", "b", "r"])
                    # orange-blue edge
                    elif self.cube["yellow"][1][0] == "B":
                        self.execute_moves(["b", "D", "b", "d", "b", "r", "B", "R"])
            else:
                # rotate back and check for edges again
                self.execute_moves(["B"])
            
    def solve_yellow_edges(self) -> None:
        """ executes moves to solve yellow edges """

        # orientate one edge, so a atleast red-yellow edge is correct
        while not self.cube["red"][1][0] == "R":
            self.execute_moves(["B"])
        
        # blue-yellow edge correct, orange-yellow edge is green-yellow
        if self.cube["blue"][2][1] == "B" and self.cube["orange"][1][2] == "G":
            self.execute_moves(["D", "B", "d" ,"B" ,"D" ,"2B" ,"d" ,"B"])
        # blue-yellow edge is orange-yellow edge, orange-yellow edge is blue-yellow
        elif self.cube["blue"][2][1] == "O" and self.cube["orange"][1][2] == "B":
            self.execute_moves(["L", "B", "l", "B", "L", "B", "B", "l", "B"])
        # blue-yellow edge is green-yellow edge, orange-yellow edge is blue-yellow
        elif self.cube["blue"][2][1] == "G" and self.cube["orange"][1][2] == "B":
            self.execute_moves(["L", "B", "l", "B", "L", "B", "B", "l", "B", "D", "B", "d" ,"B" ,"D" ,"2B" ,"d" ,"B"])
        # blue-yellow edge is green-yellow edge, orange-yellow edge is correct
        elif self.cube["blue"][2][1] == "G" and self.cube["orange"][1][2] == "O":
            self.execute_moves(["L", "B", "l", "B", "L", "B", "B", "l", "B", "D", "B", "d" ,"B" ,"D" ,"2B" ,"d" ,"B", "L", "B", "l", "B", "L", "B", "B", "l", "B"])
        # blue-yellow edge is orange-yellow and orange-yellow edge is green-yellow
        elif self.cube["blue"][2][1] == "O" and self.cube["orange"][1][2] == "G":
            self.execute_moves(["D", "B", "d" ,"B" ,"D" ,"2B" ,"d" ,"B", "L", "B", "l", "B", "L", "B", "B", "l", "B"])

    def solve_yellow_corners(self) -> None:
        """ permutes the current cube, so that yellow corners are solved """

        red_blue, red_green, orange_blue, orange_green = False, False, False, False
        
        # while not a single corner is solved
        while not (red_blue or red_green or orange_blue or orange_green): 
            # is green-orange-yellow corner correct? (orientation not important, but corner piece should be correct)
            if (self.cube["green"][0][2] == "G" or self.cube["green"][0][2] == "O" or self.cube["green"][0][2] == "Y") and \
                (self.cube["orange"][0][2] == "G" or self.cube["orange"][0][2] == "O" or self.cube["orange"][0][2] == "Y") and \
                    (self.cube["yellow"][2][2] == "G" or self.cube["yellow"][2][2] == "O" or self.cube["yellow"][2][2] == "Y"):
                    # perform algorithm as long as green-red-yellow corner is not correct
                    while not ((self.cube["green"][0][0] == "G" or self.cube["green"][0][0] == "R" or self.cube["green"][0][0] == "Y") and \
                                (self.cube["red"][0][0] == "G" or self.cube["red"][0][0] == "R" or self.cube["red"][0][0] == "Y") and \
                                (self.cube["yellow"][2][0] == "G" or self.cube["yellow"][2][0] == "R" or self.cube["yellow"][2][0] == "Y")):
                        self.execute_moves(["B", "R", "b", "l", "B", "r", "b", "L"])
                    orange_green = True
            # is green-red-yellow corner correct? (orientation not important, but corner piece should be correct)
            elif (self.cube["green"][0][0] == "G" or self.cube["green"][0][0] == "R" or self.cube["green"][0][0] == "Y") and \
                (self.cube["red"][0][0] == "G" or self.cube["red"][0][0] == "R" or self.cube["red"][0][0] == "Y") and \
                    (self.cube["yellow"][2][0] == "G" or self.cube["yellow"][2][0] == "R" or self.cube["yellow"][2][0] == "Y"):
                    # perform algorithm as long as blue-red-yellow corner is not correct
                    while not ((self.cube["blue"][2][0] == "B" or self.cube["blue"][2][0] == "R" or self.cube["blue"][2][0] == "Y") and \
                                (self.cube["red"][2][0] == "B" or self.cube["red"][2][0] == "R" or self.cube["red"][2][0] == "Y") and \
                                (self.cube["yellow"][0][0] == "B" or self.cube["yellow"][0][0] == "R" or self.cube["yellow"][0][0] == "Y")):
                        self.execute_moves(["B", "U", "b", "d", "B", "u", "b", "D"]) 
                    red_green = True
            # is blue-red-yellow corner correct? (orientation not important, but corner piece should be correct)
            elif (self.cube["blue"][2][0] == "B" or self.cube["blue"][2][0] == "R" or self.cube["blue"][2][0] == "Y") and \
                (self.cube["red"][2][0] == "B" or self.cube["red"][2][0] == "R" or self.cube["red"][2][0] == "Y") and \
                    (self.cube["yellow"][0][0] == "B" or self.cube["yellow"][0][0] == "R" or self.cube["yellow"][0][0] == "Y"):
                    # perform algorithm as long as blue-orange-yellow corner is not correct
                    while not ((self.cube["blue"][2][2] == "B" or self.cube["blue"][2][2] == "O" or self.cube["blue"][2][2] == "Y") and \
                (self.cube["orange"][2][2] == "B" or self.cube["orange"][2][2] == "O" or self.cube["orange"][2][2] == "Y") and \
                    (self.cube["yellow"][0][2] == "B" or self.cube["yellow"][0][2] == "O" or self.cube["yellow"][0][2] == "Y")):
                        self.execute_moves(["B", "L", "b", "r", "B", "l", "b", "R"])
                    red_blue = True
            # is blue-orange-yellow corner correct? (orientation not important, but corner piece should be correct)
            elif ((self.cube["blue"][2][2] == "B" or self.cube["blue"][2][2] == "O" or self.cube["blue"][2][2] == "Y") and \
                (self.cube["orange"][2][2] == "B" or self.cube["orange"][2][2] == "O" or self.cube["orange"][2][2] == "Y") and \
                    (self.cube["yellow"][0][2] == "B" or self.cube["yellow"][0][2] == "O" or self.cube["yellow"][0][2] == "Y")):
                    # perform algorithm as long as green-orange-yellow corner is not correct
                    while not ((self.cube["green"][0][2] == "G" or self.cube["green"][0][2] == "O" or self.cube["green"][0][2] == "Y") and \
                (self.cube["orange"][0][2] == "G" or self.cube["orange"][0][2] == "O" or self.cube["orange"][0][2] == "Y") and \
                    (self.cube["yellow"][2][2] == "G" or self.cube["yellow"][2][2] == "O" or self.cube["yellow"][2][2] == "Y")):
                        self.execute_moves(["B", "D", "b", "u", "B", "d", "b", "U"])
                    orange_blue = True
            # no corner is correctly placed. Just execute algorithm and hope it orientates atleast one corner correctly
            else:
                self.execute_moves(["B", "R", "b", "l", "B", "r", "b", "L"])
        
        # execute algorithm for each corner until yellow is correctly located
        for i in range(4):
            while not self.cube["yellow"][2][2] == "Y":
                self.execute_moves(["r", "f", "R", "F"])
            self.execute_moves(["b"])

    def get_solve_strings(self) -> list:
        """ receive a list of move strings """
        return [self.movesToSolveWhiteFace, self.movesToSolveSecondLayer, self.movesToSolveYellowCross, self.movesToSolveYellowEdges, self.movesToSolveYellowCorners, self.moveString]

    def start_solve(self) -> None:
        """ call needed functions to simulate the process of solving the cube """
        self.solve_white_side()
        self.movesToSolveWhiteFace = self.moveString
        self.moveString = ""
        self.solve_second_layer()
        self.movesToSolveSecondLayer = self.moveString
        self.moveString = ""
        self.create_yellow_cross()
        self.movesToSolveYellowCross = self.moveString
        self.moveString = ""
        self.solve_yellow_edges()
        self.movesToSolveYellowEdges = self.moveString
        self.moveString = ""
        self.solve_yellow_corners()
        self.movesToSolveYellowCorners = self.moveString
        self.moveString = self.movesToSolveWhiteFace + self.movesToSolveSecondLayer + self.movesToSolveYellowCross + self.movesToSolveYellowEdges + self.movesToSolveYellowCorners 
        return
    
    def executeMove(self, move: str) -> None:
        """ sort MoveString to according method call """
        # Right
        if move == "R":
            return self.mover.make_right(self.cube)
        # Right Prime
        elif move == "r":
            return self.mover.make_right(self.cube, inverted = True)
        # Double Right
        elif move == "2R":
            return self.mover.make_right(self.mover.make_right(self.cube))
        # Left
        elif move == "L":
            return self.mover.make_left(self.cube)
        # Left Prime
        elif move == "l":
            return self.mover.make_left(self.cube, inverted = True)
        # Double Left
        elif move == "2L":
            return self.mover.make_left(self.mover.make_left(self.cube))
        # Up
        elif move == "U":
            return self.mover.make_up(self.cube)
        # Up Prime
        elif move == "u":
            return self.mover.make_up(self.cube, inverted = True)
        # Double Up
        elif move == "2U":
            return self.mover.make_up(self.mover.make_up(self.cube))
        # Back
        elif move == "B":
            return self.mover.make_back(self.cube)
        # Back Prime
        elif move == "b":
            return self.mover.make_back(self.cube, inverted = True)
        # Double Back
        elif move == "2B":
            return self.mover.make_back(self.mover.make_back(self.cube))
        # Down
        elif move == "D":
            return self.mover.make_down(self.cube)
        # Down Prime
        elif move == "d":
            return self.mover.make_down(self.cube, inverted = True)
        # Double Down
        elif move == "2D":
            return self.mover.make_down(self.mover.make_down(self.cube))
        # Front
        elif move == "F":
            return self.mover.make_front(self.cube)
        # Front Prime
        elif move == "f":
            return self.mover.make_front(self.cube, inverted = True)
        # Double Front
        elif move == "2F":
            return self.mover.make_front(self.mover.make_front(self.cube))
    
    def is_edge_piece(self, indices: tuple) -> bool:
        """
            checks if the index of the current piece indicates if its an edge piece or not
        """
        return ((indices[0] == 0 or indices[0] == 2) and indices[1] == 1) or (indices[0] == 1 and (indices[1] == 0 or indices[1] == 2))

    def has_white_in_face(self, face: list) -> list:
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
        self.current_scramble = ""
        self.permutation = ""
        self.create_move_buttons()    
        self.print_cube(self.cube)
        self.color_cycle = ['G', 'W', 'R', 'O', 'B', 'Y']

    def generate_scramble(self):
        """ calls scramble generation form helper and shows it """
        helper = RubiksHelper()
        move_list = helper.get_scramble()
        temp = RubiksCubeSolver(self.mover, self.cube)
        for move in move_list:
            self.current_scramble += move + " "
        self.current_scramble += "\n"
        temp.execute_moves(move_list)
        self.cube = temp.get_cube()
        self.print_cube(self.cube)

    def show_scramble_win(self):
        win = tk.Toplevel(self.root)
        tk.Label(win, text=self.current_scramble).pack(padx=30, pady=30)

    def create_move_buttons(self):
        """ Initializes Buttons for permuting the cube """
        # Left
        self.L_button = tk.Button(self.root, text="  L  ", command=lambda: self.moveButtonHandler('L'))
        self.L_button.place(x=25, y=450)
        # Left Prime
        self.l_button = tk.Button(self.root, text="  l  ", command=lambda: self.moveButtonHandler('l'))
        self.l_button.place(x=25, y=475)
        # Right
        self.R_button = tk.Button(self.root, text="  R  ", command=lambda: self.moveButtonHandler('R'))
        self.R_button.place(x=60, y=450)
        # Right Prime
        self.r_button = tk.Button(self.root, text="  r  ", command=lambda: self.moveButtonHandler('r'))
        self.r_button.place(x=60, y=475)
        # Up
        self.U_button = tk.Button(self.root, text="  U  ", command=lambda: self.moveButtonHandler('U'))
        self.U_button.place(x=95, y=450)
        # Up Prime
        self.u_button = tk.Button(self.root, text="  u  ", command=lambda: self.moveButtonHandler('u'))
        self.u_button.place(x=95, y=475) 
        # Front
        self.F_button = tk.Button(self.root, text="  F  ", command=lambda: self.moveButtonHandler('F'))
        self.F_button.place(x=130, y=450)
        # Front Prime
        self.f_button = tk.Button(self.root, text="  f  ", command=lambda: self.moveButtonHandler('f'))
        self.f_button.place(x=130, y=475)
        # Down
        self.D_button = tk.Button(self.root, text="  D  ", command=lambda: self.moveButtonHandler('D'))
        self.D_button.place(x=165, y=450)
        # Down Prime
        self.d_button = tk.Button(self.root, text="  d  ", command=lambda: self.moveButtonHandler('d'))
        self.d_button.place(x=165, y=475)
        # Back
        self.B_button = tk.Button(self.root, text="  B  ", command=lambda: self.moveButtonHandler('B'))
        self.B_button.place(x=200, y=450)
        # Back Prime
        self.b_button = tk.Button(self.root, text="  b  ", command=lambda: self.moveButtonHandler('b'))
        self.b_button.place(x=200, y=475)
        # Solve Button
        self.solve_button = tk.Button(self.root, text= "Solve", command=lambda: self.solveCube())
        self.solve_button.place(x=60, y= 525)
        # generate mix
        self.generate_mix = tk.Button(self.root, text= "Generate Scramble", command=lambda: self.generate_scramble())
        self.generate_mix.place(x = 60, y= 560)
        # show scramble mix 
        self.show_scramble = tk.Button(self.root, text = "Show generated scramble", command=lambda: self.show_scramble_win())
        self.show_scramble.place(x=60, y=590)
        # add Instruction Label
        self.instruction_label = tk.Label(self.root, text= "Please keep the white side in the front \n(shows to you) and the green side at the \ntop (points up) at all times!")
        self.instruction_label.place(x=30, y=380)

    def solveCube(self):
        """ calls solve function from RubiksCubeSolver """
        solver = RubiksCubeSolver(self.mover, self.cube)
        solver.start_solve()
        self.cube = solver.get_cube()
        self.print_cube(self.cube)
        move_strings = solver.get_solve_strings()
        self.show_solution_popup(move_strings)
        self.current_scramble = ""
    
    def show_solution_popup(self, moveStrings):
        """ shows a movement string to solve the cube """
        win = tk.Toplevel(self.root)
        tk.Label(win, text= "Cube-perm: " + self.permutation + 
                            "\n\n" + moveStrings[0] + "\n\n" + 
                            "White Face Solved\n\n" + 
                            moveStrings[1] + "\n\n" + 
                            "Second Layer solved\n\n" +
                            moveStrings[2] + "\n\n" + 
                            "Yellow Cross solved\n\n" +
                            moveStrings[3] + "\n\n" + 
                            "Yellow Edges solved\n\n" +
                            moveStrings[4]).pack(padx=30, pady=30)

    def get_color(self, color):
        """ gets color string according to given Characters (W, R, B, G, Y, O) """
        return 'white' if color == "W" else 'red' if color == "R" else 'blue' if color == "B" else 'yellow' if color == "Y" else 'green' if color == "G" else 'orange'

    def changeColor(self, currentColor, currentSide, x, y):
        """ changes color of tiles on click, according to pre-defined cycle """
        currentIndex = self.color_cycle.index(currentColor)
        nextIndex = currentIndex+1
        if nextIndex == len(self.color_cycle):
            nextIndex = 0
        self.cube[currentSide][x][y] = self.color_cycle[nextIndex]
        self.print_cube(self.cube)
        
    def print_cube(self, cube):
        """ calls prints every cube side on User Interface with Positional Arguments for the UI """
        self.print_face(cube["green"], 120, 15, "green")
        self.print_face(cube["red"], 73, 90, "red")
        self.print_face(cube["white"], 120, 90, "white")
        self.print_face(cube["orange"], 166, 90, "orange")
        self.print_face(cube["blue"], 120, 165, "blue")
        self.print_face(cube["yellow"], 120, 240, "yellow")

    def print_face(self, colors, gridX, gridY, side):
        """ prints face (UI) according to given color and position data """
        # top Left
        tL = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][0]), command=lambda: self.changeColor(colors[0][0], side, 0, 0))
        tL.place(x=gridX, y=gridY)

        # top Mid
        tM = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][1]), command=lambda: self.changeColor(colors[0][1], side, 0, 1))
        tM.place(x=gridX+15, y=gridY)

        # top Right
        tR = tk.Button(self.root, text="  ", bg= self.get_color(colors[0][2]), command=lambda: self.changeColor(colors[0][2], side, 0, 2))
        tR.place(x=gridX+30, y=gridY)

        # mid Left
        mL = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][0]), command=lambda: self.changeColor(colors[1][0], side, 1, 0))
        mL.place(x=gridX, y=gridY+25)

        # mid Mid
        if side == "white":
            mM = tk.Button(self.root, text="F ", bg = self.get_color(colors[1][1]))
        elif side == "green":
            mM = tk.Button(self.root, text="T ", bg= self.get_color(colors[1][1]))
        else:
            mM = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][1]))
        
        mM.place(x=gridX+15, y=gridY+25)

        # mid Right
        mR = tk.Button(self.root, text="  ", bg= self.get_color(colors[1][2]), command=lambda: self.changeColor(colors[1][2], side, 1, 2))
        mR.place(x=gridX+30, y=gridY+25)

        # bottom Left
        bL = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][0]), command=lambda: self.changeColor(colors[2][0], side, 2, 0))
        bL.place(x=gridX, y=gridY+50)

        # bottom Right
        bM = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][1]), command=lambda: self.changeColor(colors[2][1], side, 2, 1))
        bM.place(x=gridX+15, y=gridY+50)

        # bottom Left
        bR = tk.Button(self.root, text="  ", bg= self.get_color(colors[2][2]), command=lambda: self.changeColor(colors[2][2], side, 2, 2))
        bR.place(x=gridX+30, y=gridY+50)
        
    def moveButtonHandler(self, move):
        """ handler for permutation buttons """
        self.permutation += move + " "
        self.cube = self.mover.sort_move(move, self.cube)
        self.print_cube(self.cube)

def main():
    """ Initializes needed Elements for the Project """
    cube = {
        'white': [
            ["W" for row in range(3)] for line in range(3)
        ],
        'red': [
            ["R" for row in range(3)] for line in range(3)
        ],
        'blue': [
            ["B" for row in range(3)] for line in range(3)
        ],
        'green': [
           ["G" for row in range(3)] for line in range(3)
        ],
        'yellow': [
            ["Y" for row in range(3)] for line in range(3)
        ],
        'orange': [
            ["O" for row in range(3)] for line in range(3)
        ]
    }

    root = tk.Tk()
    root.geometry('280x650')
    interface = UserInterface(root, Movemaker(), cube)
    root.mainloop()

if __name__ == "__main__":
    main()

