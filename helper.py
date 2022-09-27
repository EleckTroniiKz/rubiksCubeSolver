import random 


class RubiksHelper:
    def __init__(self):
        self.moves = ["R", "L", "B", "F", "U", "D", "r", "l", "b", "f", "u", "d"]

    def parse_moveString(self, moves):
        """ turns movestring into more compact form"""

        #TBD diese Methode funktioniert noch nicht so wie sie soll.
        move_list = moves.split()
        nothing_changed = True
        index = 0

        while nothing_changed:
            nothing_changed = False
            if index <= len(moves)-1:
                if  ((move_list[index].isupper() and move_list[index+1].islower()) or \
                    (move_list[index].islower() and move_list[index+1].isupper())) and \
                    (move_list[index].casefold() == move_list[index+1].casefold()):
                    del move_list[index+1]
                    index = 0
                    nothing_changed = True
                    continue
                elif ((move_list[index] == move_list[index+1] and "2" in move_list[index])):
                    del move_list[index:index+2]
                    index = 0
                    nothing_changed = True
                    continue
                elif ((move_list[index] == move_list[index+1] and not "2" in move_list[index])):
                    del move_list[index+1]
                    move_list[index] = "2"+move_list[index].uppercase()
                    index = 0
                    nothing_changed = True
                    continue
                index += 1
            else:
                index = 0

        move_string = " ".join(move_list)
        return move_string

    def get_scramble(self, length = 20):
        """ generates random list of moves """
        random_moves = []
        lastMadeMove = ""
        while len(random_moves) < length:
            random_number = random.randint(0, len(self.moves)-1)
            if lastMadeMove.capitalize() == self.moves[random_number].capitalize():
                continue
            else:
                lastMadeMove = self.moves[random_number][0]
                random_moves.append(lastMadeMove)
        return random_moves

    def is_edge_piece(self, indices):
        """ returns true, if indices belong to an edge piece """
        return ((indices[0] == 0 or indices[0] == 2) and indices[1] == 1) or (indices[0] == 1 and (indices[1] == 0 or indices[1] == 2))

    def start_timer(self):
        # TBD: But this Method should be called, when the user wants to start a timer.
        pass

    def end_timer(self):
        # TBD: But this Method should be called, when the user wnats to end a timer.
        pass

    def get_time(self):
        # TBD: But this calculated the timedifference between start and end
        pass
