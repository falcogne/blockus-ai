import piece
import board
import constants
import random

class Player():
    def __init__(self, color, piece_strings, board):
        self.color = color
        self.board = board
        self.piece_strings_backup = piece_strings
        self.pieces = None
        self.reset()
    
    
    def reset(self):
        self.pieces = [piece.Piece(self.color, s) for s in self.piece_strings_backup]

    
    def choose_move(self, availables):
        choice = random.choice(availables)
        return choice
    
    def remove_piece_taken(self, choice):
        for p in self.pieces:
            if choice[0].same_shape(p):
                self.pieces.remove(p)
                return choice
        raise ValueError("removing a piece that's not in your hand???")

    def take_turn(self):

        possible_moves = self.board.find_available_moves(self.pieces)

        if len(possible_moves) == 0:
            return False
        
        move = self.choose_move(possible_moves)
        self.remove_piece_taken(move)
        self.board.place_piece(move[0], move[1])

        # print(self.board.str_for_player(self.color))
        # print("turn over")
        # print("-"*30)
        # print()
        
        return True
    

class FastPlayer(Player):
    def take_turn(self):

        biggest_piece = len(self.pieces) - 1

        while biggest_piece != -1:

            possible_moves = self.board.find_available_moves([self.pieces[biggest_piece]])

            if len(possible_moves) == 0:
                biggest_piece -= 1
            else:
                move = self.choose_move(possible_moves)
                self.remove_piece_taken(move)
                self.board.place_piece(move[0], move[1])
                return True
        return False
    
class SlowDecisive(Player):
    def choose_move(self, availables):
        
        best_score = -10_000_000
        best_move = []
        for p in availables:
            test_b = self.board.test_move(p[0], p[1])
            count_my_corners = 0
            count_other_corners = 0
            # count_other_corners = [0]*(len(constants.PLAYER_COLORS)-1)
            for arr in test_b.board:
                for square_list in arr:
                    for sq in square_list:
                        if sq.type == constants.CORNER:
                            if sq.color == self.color:
                                count_my_corners += 1
                            else:
                                count_other_corners += 1
            
            score = 1.2 * count_my_corners + -3 * count_other_corners + 1.5 * p[0].num_filled
            
            if score == best_score:
                best_move.append(p)
            elif score > best_score:
                best_score = score
                best_move = [p]

        return random.choice(best_move)