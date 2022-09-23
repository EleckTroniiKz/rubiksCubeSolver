import random 


class RubiksHelper:
    def __init__(self):
        self.moves = ["R", "L", "B", "F", "U", "D", "r", "l", "b", "f", "u", "d"]

    def parse_moveString(self, moves):
        """ turns movestring into more compact form"""
        move_list = moves.split()

        # loop and check if doubles occur
        for index in range(0, len(move_list), 2):
            if index+1 >= len(move_list):
                break
            else:
                if move_list[index] == move_list[index+1]:
                    move_list.pop(index)
                    move_list[index] = "2" + move_list[index].capitalize()
                elif move_list[index] == move_list[index+1].casefold() or move_list[index].casefold() == move_list[index+1]:
                    move_list.pop(index)
                    move_list.pop(index)

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

    def is_edge_piece(self, indices):
        """ returns true, if indices belong to an edge piece """
        return ((indices[0] == 0 or indices[0] == 2) and indices[1] == 1) or (indices[0] == 1 and (indices[1] == 0 or indices[1] == 2))

    def start_timer(self):
        pass

    def end_timer(self):
        pass

    def get_time(self):
        pass

