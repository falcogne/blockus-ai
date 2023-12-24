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
        for p in self.pieces:
            if choice[0].same_shape(p):
                self.pieces.remove(p)
                return choice
        raise ValueError("chose a piece that's not in your hand???")
    

    def take_turn(self):

        possible_moves = self.board.find_available_moves(self.pieces)

        if len(possible_moves) == 0:
            return False
        
        move = self.choose_move(possible_moves)
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
                self.board.place_piece(move[0], move[1])
                return True
        return False
