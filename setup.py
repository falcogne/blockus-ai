import piece
import board
import players
import constants
import random

class Setup():
    def __init__(self):
        self.reset()

    def reset(self):
        self.b = board.Board()
        self.piece_strings = [
            [
                ['x'],
            ],
            [
                ['x', 'x'],
            ],
            [
                ['x', 'x', 'x'],
            ],
            [
                ['x','x'],
                ['x','.'],
            ],
            [
                ['x', 'x', 'x', 'x'],
            ],
            [
                ['x','.','.'],
                ['x','x','x'],
            ],
            [
                ['.','x','.'],
                ['x','x','x'],
            ],
            [
                ['x','x'],
                ['x','x'],
            ],
            [
                ['.','x','x'],
                ['x','x','.'],
            ],
            [
                ['x', 'x', 'x', 'x', 'x'],
            ],
            [
                ['x','x','x','x'],
                ['x','.','.','.'],
            ],
            [
                ['x','x','x','.'],
                ['.','.','x','x'],
            ],
            [
                ['x','x','x'],
                ['x','x','.'],
            ],
            [
                ['x','x'],
                ['x','.'],
                ['x','x'],
            ],
            [
                ['x','x','x','x'],
                ['.','.','x','.'],
            ],
            [
                ['.','x','.'],
                ['.','x','.'],
                ['x','x','x'],
            ],
            [
                ['x','.','.'],
                ['x','.','.'],
                ['x','x','x'],
            ],
            [
                ['x','.','.'],
                ['x','x','.'],
                ['.','x','x'],
            ],
            [
                ['x','.','.'],
                ['x','x','x'],
                ['.','.','x'],
            ],
            [
                ['x','.','.'],
                ['x','x','x'],
                ['.','x','.'],
            ],
            [
                ['.','x','.'],
                ['x','x','x'],
                ['.','x','.'],
            ],
        ]

        self.players = [
            players.SlowDecisive(constants.PLAYER_COLORS[0], self.piece_strings, self.b),
            players.FastPlayer(constants.PLAYER_COLORS[1], self.piece_strings, self.b),
            players.Player(constants.PLAYER_COLORS[2], self.piece_strings, self.b),
            players.Player(constants.PLAYER_COLORS[3], self.piece_strings, self.b),
        ]
        self.turn = random.randrange(0,len(self.players))
        self.players_out = []


    def play(self):
        while len(self.players) > 0:
            self.turn = (self.turn + 1) % len(self.players)
            # take_turn returns True if player could successfully take their turn
            if not self.players[self.turn].take_turn():
                self.players_out.append(self.players[self.turn])
                self.players.remove(self.players[self.turn])
            print(self.b)
        
        best_score = 1_000_000
        winner = None
        for p in self.players_out:
            score = 0
            for piece in p.pieces:
                score += piece.num_filled
            print(f"{p.color}: {score}")
            if score < best_score:
                best_score = score
                winner = p
        print(f"winner is {winner.color} with {best_score} squares left in their hand")

if __name__ == "__main__":
    s = Setup()
    s.play()
