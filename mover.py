class Movemaker:
    def __init__(self):
        self.lastMove = 0

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
        TopLeft, TopRight, BottomLeft, BottomRight = currentSide[0][0], currentSide[0][2], currentSide[2][0], currentSide[2][2]
        TopMid, MidLeft, MidRight, BottomMid = currentSide[0][1], currentSide[1][0], currentSide[1][2], currentSide[2][1]
        if not inverted:
            currentSide[0][0] = BottomLeft
            currentSide[0][1] = MidLeft
            currentSide[0][2] = TopLeft
            currentSide[1][0] = BottomMid
            currentSide[1][2] = TopMid
            currentSide[2][0] = BottomRight
            currentSide[2][1] = MidRight
            currentSide[2][2] = TopRight
        else:
            currentSide[0][0] = TopRight
            currentSide[0][1] = MidRight
            currentSide[0][2] = BottomRight
            currentSide[1][0] = TopMid
            currentSide[1][2] = BottomMid
            currentSide[2][0] = TopLeft
            currentSide[2][1] = MidLeft
            currentSide[2][2] = BottomLeft
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
            
            cube["orange"][0][0], cube["orange"][0][1], cube["orange"][0][2] = cube["yellow"][2][2], cube["yellow"][2][1], cube["yellow"][2][0]

            cube["yellow"][2][0], cube["yellow"][2][1], cube["yellow"][2][2] = cube["red"][0][2], cube["red"][0][1], cube["red"][0][0]

            cube["red"][0][0], cube["red"][0][1], cube["red"][0][2] = whiteA, whiteB, whiteC
            
            cube["green"] = self.twist(cube["green"])
        else:
            whiteA, whiteB, whiteC = cube["white"][0][0], cube["white"][0][1], cube["white"][0][2]
            cube["white"][0][0], cube["white"][0][1], cube["white"][0][2] = cube["red"][0][0], cube["red"][0][1], cube["red"][0][2]

            cube["red"][0][0], cube["red"][0][1], cube["red"][0][2] = cube["yellow"][2][2], cube["yellow"][2][1], cube["yellow"][2][0]

            cube["yellow"][2][0], cube["yellow"][2][1], cube["yellow"][2][2] = cube["orange"][0][2], cube["orange"][0][1], cube["orange"][0][0]

            cube["orange"][0][0], cube["orange"][0][1], cube["orange"][0][2] = whiteA, whiteB, whiteC
            
            cube["green"] = self.twist(cube["green"], True)
        return cube

    def make_down(self, cube, inverted = False):
        #transform the cube as if a down move was made
        if not inverted:
            whiteA, whiteB, whiteC = cube["white"][2][0], cube["white"][2][1], cube["white"][2][2]
            cube["white"][2][0], cube["white"][2][1], cube["white"][2][2] = cube["red"][2][0], cube["red"][2][1], cube["red"][2][2]
            
            cube["red"][2][0], cube["red"][2][1], cube["red"][2][2] = cube["yellow"][0][2], cube["yellow"][0][1], cube["yellow"][0][0]

            cube["yellow"][0][2], cube["yellow"][0][1], cube["yellow"][0][0] = cube["orange"][2][0], cube["orange"][2][1], cube["orange"][2][2]
            
            cube["orange"][2][0], cube["orange"][2][1], cube["orange"][2][2] = whiteA, whiteB, whiteC

            cube["blue"] = self.twist(cube["blue"])
            
        else:
            whiteA, whiteB, whiteC = cube["white"][2][0], cube["white"][2][1], cube["white"][2][2]
            cube["white"][2][0], cube["white"][2][1], cube["white"][2][2] = cube["orange"][2][0], cube["orange"][2][1], cube["orange"][2][2]
            
            cube["orange"][2][0], cube["orange"][2][1], cube["orange"][2][2] = cube["yellow"][0][2], cube["yellow"][0][1], cube["yellow"][0][0]

            cube["yellow"][0][2], cube["yellow"][0][1], cube["yellow"][0][0] = cube["red"][2][0], cube["red"][2][1], cube["red"][2][2]

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

            cube["red"][2][0], cube["red"][1][0], cube["red"][0][0] = greenA, greenB, greenC
            
            cube["yellow"] = self.twist(cube["yellow"])
            
        else:
            greenA, greenB, greenC = cube["green"][0][0], cube["green"][0][1], cube["green"][0][2]
            cube["green"][0][0], cube["green"][0][1], cube["green"][0][2] = cube["red"][2][0], cube["red"][1][0], cube["red"][0][0]
            
            cube["red"][2][0], cube["red"][1][0], cube["red"][0][0] = cube["blue"][2][2], cube["blue"][2][1], cube["blue"][2][0]

            cube["blue"][2][0], cube["blue"][2][1], cube["blue"][2][2] = cube["orange"][2][2], cube["orange"][1][2], cube["orange"][0][2]

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
            greenA, greenB, greenC = cube["green"][2][2], cube["green"][2][1], cube["green"][2][0]
            cube["green"][2][0], cube["green"][2][1], cube["green"][2][2] = cube["orange"][0][0], cube["orange"][1][0], cube["orange"][2][0]
            
            cube["orange"][0][0], cube["orange"][1][0], cube["orange"][2][0] = cube["blue"][0][2], cube["blue"][0][1], cube["blue"][0][0]

            cube["blue"][0][0], cube["blue"][0][1], cube["blue"][0][2] = cube["red"][0][2], cube["red"][1][2], cube["red"][2][2]

            cube["red"][0][2], cube["red"][1][2], cube["red"][2][2] = greenA, greenB, greenC
            
            cube["white"] = self.twist(cube["white"], inverted=True)
        return 