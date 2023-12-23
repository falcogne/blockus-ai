creating blockus and then once the ai learns the game I want to see what kinds of strategies it uses.

I'm putting a lot of heavy lifting into the Piece class. It's given a shape like:

(TODO: I want this to be verbatim idk how tho)
x .
x x
. x

it then extends a border around it to work with:

. . . .
. x . .
. x x .
. . x .
. . . .

and then it populates the adjacent pieces (helpful to determine corners)

. a . .
a x a .
a x x a
. a x a
. . a .

and finally finds the corners:

c a c .
a x a c
a x x a
c a x a
. c a c

at any point here, it can flip or rotate the piece (which will be necessary for trying to find available moves)

---

used this to figure out how to do rotation:

0,0 0,1 0,2 0,3
1,0 1,1 1,2 1,3
2,0 2,1 2,2 2,3

row 0 is column 2
row 1 is column 1
row 2 is column 0

column 0 is flipped row 0
column 1 is flipped row 1

2,0 1,0 0,0
2,1 1,1 0,1
2,2 1,2 0,2
2,3 1,3 0,3

0,0 0,1 0,2
1,0 1,1 1,2
2,0 2,1 2,2
3,0 3,1 3,2

it was kinda helpful

---

That lets me put each piece in every possible orientation and then try to match up the corners from the piece with the corneers available on the board. The loop would be something like:

```
get available moves: 

for each corner on board
    for each piece in player's hand
        for each orientation # 8 total: 4 rotations for 2 flips
            # now we have piece in oreintation
            for each corner on piece
                get a translation to move corner to match
                for each translation
                    for each square in the piece
                        if square is a adjacent, is it overlapping one of your own pieces?
                            if yes invalid
                        if square is a filled, is it overlapping any piece (including out of bounds)?
                            if yes invalid
                        reaching here means valid - add it to possible moves
```

the optimization I could do is to track whether a space on the board was affected (adjacent or corner was modified) and keep the prior possible moves that were not affected since the last turn. I'm worried that the "checking moves" part will be way too long, so this may be necessary. 

