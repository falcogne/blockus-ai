import constants

class Piece():
    def __init__(self, shape=None):
        self.shape = None
        self.adjacents = None
        self.corners = None
        if shape is not None:
            self.set_shape(shape)
    
    def set_shape(self, s):
        self.shape = [[constants.EMPTY for _ in range(len(s[0])+2)] for _ in range(len(s)+2)]
        width = len(s[0])
        for row in range(len(s)):
            assert len(s[row]) == width
            for col in range(len(s[row])):
                self.shape[row+1][col+1] = s[row][col]
        self.set_adjacents()
        self.set_corners()


    def set_adjacents(self):
        self.adjacents = []
        for row, arr in enumerate(self.shape):
            for col, val in enumerate(arr):
                # go through all spaces, only care about where the shape has a piece
                if val == constants.FILLED:
                    # go to each adjacent spot and mark it
                    for d in [(1,0), (-1,0), (0,-1), (0,1)]:
                        self.adjacents.append((row+d[0], col+d[1]))
        for spot in self.adjacents:
            if self.shape[spot[0]][spot[1]] != constants.FILLED:
                self.shape[spot[0]][spot[1]] = constants.ADJACENT

    def set_corners(self):
        assert self.adjacents is not None and len(self.adjacents) > 0
        self.corners = []
        for row, arr in enumerate(self.shape):
            for col, val in enumerate(arr):
                # go through all spaces, only care about where the shape has a piece
                if val == constants.FILLED:
                    # go to each diagonal point
                    for d in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        # only mark it if the spot isn't already adjacent to another place in the piece
                        spot = (row+d[0], col+d[1])
                        if spot not in self.adjacents:
                            self.corners.append(spot)
        for spot in self.corners:
            if self.shape[spot[0]][spot[1]] != constants.FILLED:
                self.shape[spot[0]][spot[1]] = constants.CORNER

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
            s += " ".join(arr) + "\n"
        
        return s    
    
p = Piece([
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