class Tester:
    def __init__(self, mover):
        self.mover = mover

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
