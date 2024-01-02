import constants

class Piece():
    def __init__(self, c, s=None):
        self.string_shape = s # keep it just for copying purposes
        self.shape = None
        self.adjacents = None
        self.corners = None
        self.color = c
        self.num_filled = 0
        if s is not None:
            self.set_shape(s)
    
    def set_shape(self, s):
        self.num_filled = 0
        self.shape = [[Square(constants.EMPTY, '') for _ in range(len(s[0])+2)] for _ in range(len(s)+2)]
        width = len(s[0])
        for row in range(len(s)):
            assert len(s[row]) == width
            for col in range(len(s[row])):
                if s[row][col] == constants.FILLED:
                    self.num_filled += 1
                    self.shape[row+1][col+1] = Square(constants.FILLED, self.color)
        self.set_adjacents()
        self.set_corners()


    def copy(self):
        c = Piece(self.color, self.string_shape)
        for _ in range(2):
            for _ in range(4):
                if c == self:
                    return c
                c.rotate()
            c.flip()

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def same_shape(self, other) -> bool:
        return self.string_shape == other.string_shape

    def change_color(self, c):
        self.color = c


    def set_adjacents(self):
        self.adjacents = []
        for row, arr in enumerate(self.shape):
            for col, val in enumerate(arr):
                # go through all spaces, only care about where the shape has a piece
                if val.is_filled():
                    # go to each adjacent spot and mark it
                    for d in [(1,0), (-1,0), (0,-1), (0,1)]:
                        self.adjacents.append((row+d[0], col+d[1]))
        for spot in self.adjacents:
            if not self.shape[spot[0]][spot[1]].is_filled():
                self.shape[spot[0]][spot[1]] = Square(constants.ADJACENT, self.color)


    def set_corners(self):
        assert self.adjacents is not None and len(self.adjacents) > 0
        self.corners = []
        for row, arr in enumerate(self.shape):
            for col, val in enumerate(arr):
                # go through all spaces, only care about where the shape has a piece
                if val.is_filled():
                    # go to each diagonal point
                    for d in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        # only mark it if the spot isn't already adjacent to another place in the piece
                        spot = (row+d[0], col+d[1])
                        if spot not in self.adjacents:
                            self.corners.append(spot)
        for spot in self.corners:
            if not self.shape[spot[0]][spot[1]].is_filled():
                self.shape[spot[0]][spot[1]] = Square(constants.CORNER, self.color)


    def flip(self):
        """flips the piece over vertically"""
        top_row = 0
        bottom_row = len(self.shape)-1
        while bottom_row > top_row:
            for col, _ in enumerate(self.shape[top_row]):
                self.shape[top_row][col], self.shape[bottom_row][col] = self.shape[bottom_row][col], self.shape[top_row][col]
            top_row += 1
            bottom_row -= 1
    

    def rotate(self):
        """rotates the shape 90 degrees counter-clockwise. the important part is the 90 degrees part"""
        flipped = [[constants.EMPTY for _ in range(len(self.shape))] for _ in range(len(self.shape[0]))]
        # num_rows = len(self.shape)-1
        num_cols = len(self.shape[0])-1
        for row, arr in enumerate(self.shape):
            for col, ele in enumerate(arr):
                flipped[num_cols - col][row] = ele
        self.shape = flipped


    def __str__(self):
        s = ""
        for arr in self.shape:
            for ele in arr:
                s += str(ele) + " "
            s += "\n"
        return s    


class Square():
    def __init__(self, t, c):
        self.type = t
        self.color = c
    

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Square) and self.type == __value.type and self.color == __value.color
    

    def copy(self):
        return Square(self.type, self.color)


    def is_filled(self) -> bool:
        return self.type == constants.FILLED
    

    def is_empty(self) -> bool:
        return self.type == constants.EMPTY
    

    def __str__(self) -> str:
        if self.is_filled():
            return self.color
        else:
            return self.type

if __name__ == "__main__":
    p = Piece('y', 
    [
        ['x','.','.'],
        ['x','x','x'],
        ['.','x','.'],
    ])
    print(p)
    p.rotate()
    print(p)
    p.rotate()
    print(p)
    p.rotate()
    print(p)