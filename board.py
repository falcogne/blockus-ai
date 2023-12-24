import constants
import piece

class Board():
    def __init__(self, size=(20,20)):
        self.size = size
        self.corners = []
        self.available_moves = []
        self.reset()
    

    def reset(self):
        self.available_moves = []
        self.corners = []
        self.board = [[[piece.Square(constants.EMPTY, ' ')] for _ in range(self.size[1])] for _ in range(self.size[0])]
        row_edges = (0, len(self.board)-1)
        col_edges = (0, len(self.board[0])-1)
        # set the out of bounds edge
        for i in range(row_edges[0], row_edges[1]+1):
            self.board[i][col_edges[1]] = [piece.Square(constants.OUT_OF_BOUNDS, " ")]
            self.board[i][col_edges[0]] = [piece.Square(constants.OUT_OF_BOUNDS, " ")]
        
        for i in range(col_edges[0], col_edges[1]+1):
            self.board[row_edges[0]][i] = [piece.Square(constants.OUT_OF_BOUNDS, " ")]
            self.board[row_edges[1]][i] = [piece.Square(constants.OUT_OF_BOUNDS, " ")]

        # set the initial corners you can work with
        color_i = 0
        for r in (1, len(self.board)-2):
            for c in (1, len(self.board[0])-2):
                if color_i >= len(constants.PLAYER_COLORS):
                    break
                self.board[r][c] = [piece.Square(constants.CORNER, constants.PLAYER_COLORS[color_i])]
                self.corners.append((r, c))
                color_i += 1
    
    def place_piece(self, piece : piece.Piece, translation : tuple[int, int]):
        for row, arr in enumerate(piece.shape):
            for col, ele in enumerate(arr):
                this_l = self.board[row+translation[0]][col+translation[1]]
                if ele.type == constants.CORNER:
                    self.corners.append((row+translation[0], col+translation[1]))
                # set up the list at this location
                for v in this_l:
                    if ele.is_filled() or v.is_empty():
                        this_l.remove(v)
                    elif v.type == constants.OUT_OF_BOUNDS or v.is_filled():
                        assert not ele.is_filled() # can't put a piece out of bounds

                # add the piece to the location
                this_l.append(ele)                
                # TODO: this is where you can mark that a piece was "impacted" by a placement

    def can_place_here(self, piece, translation):
        corner_matching = False
        for row, arr in enumerate(piece.shape):
            for col, ele in enumerate(arr):
                
                # check if index is in bounds
                if row+translation[0] < 0 or col+translation[1] < 0:
                    return False
                try:
                    this_l = self.board[row+translation[0]][col+translation[1]]
                except IndexError:
                    return False
                
                # check this spot for anything problematic
                for v in this_l:
                    # ele is piece we want to place, v is what's currently at this location
                    if ele.is_filled() and (v.is_filled() or v.type == constants.OUT_OF_BOUNDS):
                        return False
                    if ele.is_filled() and v.type == constants.ADJACENT and v.color == ele.color:
                        return False
                    if ele.type == constants.FILLED and v.type == constants.CORNER and v.color == ele.color:
                        corner_matching = True
        
        return corner_matching

    
    def find_available_moves(self, pieces : piece.Piece):
        """
        for each corner on board
            for each piece in player's hand
                for each orientation # 8 total: 4 rotations for 2 flips
                    # now we have piece in oreintation
                    for each filled square on piece
                        get a translation to move corner to match
                        check if can place here
        """
        for p in pieces:
            assert p.color == pieces[0].color
        
        possibilities = []
        # for each board corner
        for board_corner_loc in self.corners:             
            for square_at_loc in self.board[board_corner_loc[0]][board_corner_loc[1]]:
                # corner color doesn't match piece color, invalid placement already
                if square_at_loc.type != constants.CORNER or square_at_loc.color != pieces[0].color:
                    continue # skip this square
                # for each piece available
                for piece in pieces:
                    # do each orientation (2 for each flip side, 4 for each rotation possibility)
                    for _ in range(2):
                        for _ in range(4):
                            # for each filled square on piece
                            p = piece.copy()
                            for row, arr in enumerate(piece.shape):
                                for col, sq in enumerate(arr):
                                    if sq.type == constants.FILLED:
                                        translation = (board_corner_loc[0] - row, board_corner_loc[1] - col)
                                        if self.can_place_here(piece, translation):
                                            p = piece.copy()
                                            possibilities.append((p, translation))
                            piece.rotate()
                        piece.flip()
        # print(f"num board corners: {len(self.corners)} | num pieces in hand: {len(pieces)} | {len(possibilities)}")
        return possibilities


    def str_for_player(self, c):
        s = ""
        for arr in self.board:
            for square_list in arr:
                for sq in square_list:
                    if sq.is_filled() or sq.color == c:
                        s += str(sq) + " "
                        break
                else:
                    s += str(sq) + " "
            s += "\n"

        return s
        
    def __str__(self) -> str:
        s = ""
        for arr in self.board:
            for square_list in arr:
                is_oob = False
                for sq in square_list:
                    if sq.is_filled():
                        s += str(sq) + " "
                        break
                    # if sq.is_empty():
                    #     has_empty = True
                    if sq.type == constants.OUT_OF_BOUNDS:
                        s += str(sq) + " "
                        break
                else:
                    s += constants.EMPTY + " "
            s += "\n"

        return s
    