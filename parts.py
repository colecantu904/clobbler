import numpy as np

class Piece:
    def __init__(self, schema, id):
        self.s = np.array(schema)
        
        # its nxn
        self.size = len(schema)
        
        self.id = id
        
        self.find_part()
        
        # all possible rotations
        self.apr = []
        
        self.set_all_possible_rotations()
    
    def find_part(self, specific_piece=[]):
        # get the idx of the leftmost higmost part of piece
        board = self.s
        
        if len(specific_piece) > 0:
            board = specific_piece
            
        
        mins = []
        
        for i in range(len(board)):
            j = 0
            while j < len(board[0]) and board[i][j] != 1:
                j += 1
            
            mins.append([j, (i, j)])
        
        mi = float('inf')
        mi_idx = -1
        
        for i in range(len(mins) - 1, -1, -1):
            if mins[i][0] <= mi:
                mi_idx = i
                mi = mins[i][0]
            
            
        self.part = mins[mi_idx][1]
        
        return mins[mi_idx][1]
    
    # it needs all the rotations, and all of the reflections of certain pieces!
    # this means there is really 8 different 2d configurations of a piece
    # we also need to have it try and place the piece from the leftmost upmost position, out
    def set_all_possible_rotations( self ):
        rots_found = []
        
        copy = self.s.copy()
        
        for _ in range(2):
            for i in range(4):
                copy = np.rot90(copy)
                
                copy_tuple = tuple(map(tuple, copy))

                if copy_tuple not in rots_found:
                    self.apr.append({
                        'schema' : copy.copy(),
                        'dim' : (len(copy), len(copy[0])),
                    })
                    
                    rots_found.append(copy_tuple)
            
            # reflect the copy
            copy = copy[:, ::-1]
            
            
            
    # rotate 90 degress 
    def rotate(self):
        self.s = np.rot90(self.s)
        self.find_part()


class Board:
    def __init__(self, size_x, size_y):
        self.m = size_y
        self.n = size_x
        
        # make the board
        self.board = [ [0]*size_x for _ in range(size_y) ]
        
        self.place = (0, 0)
        
        self.moves = []
        
        self.played_pieces = set()
    
    def __str__(self):
        s = ""
        for r in self.board:
            s += f'{r}'+'\n'
        
        return s
    
    def is_board_complete(self):
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == 0:
                    return False
        
        return True
    
    def find_place( self ):
        # find the leftmost highmost place
        mins = []
        
        for i in range(self.m):
            j = 0
            while j < self.n and self.board[i][j] != 0:
                j += 1
            
            mins.append([j, (i, j)])
        
        mi = float('inf')
        mi_idx = -1
        
        for i in range(len(mins) - 1, -1, -1):
            if mins[i][0] <= mi:
                mi_idx = i
                mi = mins[i][0]
            
            
        self.place = mins[mi_idx][1]
        
    
    # automatically plays in the .place
    def play_piece(self, piece, rot, play_down):
        if piece.id in self.played_pieces:
            return False
        
        place = self.place
        
        board_cords_to_change = []
        
        # ok, we are just going to go through all rotations of piece, so for play move
        # we can just try and check to play the piece going up and going down
        
        # need to change to piece.apr[rot]['schema']
        
        if play_down:
            for i in range(piece.apr[rot]['dim'][0]):
                for j in range(piece.apr[rot]['dim'][1]):
                    # everything is resting on this
                    if ((place[0] + i) >= self.m or (place[1] + j) >= self.n or (self.board[place[0] + i][place[1] + j] != 0 and piece.apr[rot]['schema'][i][j] != 0)) and (piece.apr[rot]['schema'][i][j] != 0):
                            return False

                    if piece.apr[rot]['schema'][i][j] != 0:
                        board_cords_to_change.append((place[0] + i, place[1] + j))
        else:
            # THIS NEEDS TO BE FIXED TO COUNT 
            for i in range(piece.apr[rot]['dim'][0]):
                for j in range(piece.apr[rot]['dim'][1]):
                    if ((place[0] - i) < 0 or (place[1] + j) >= self.n or (self.board[place[0] - i][place[1] + j] != 0 and piece.apr[rot]['schema'][(piece.apr[rot]['dim'][0] - 1 ) - i][j] != 0)) and (piece.apr[rot]['schema'][(piece.apr[rot]['dim'][0] - 1 ) - i][j] != 0):
                            return False

                    if piece.apr[rot]['schema'][(piece.apr[rot]['dim'][0] - 1) - i][j] != 0:
                        board_cords_to_change.append((place[0] - i, place[1] + j))
        
        for c in board_cords_to_change:
            self.board[c[0]][c[1]] = piece.id
        
        self.moves.append(piece.id)
        self.played_pieces.add(piece.id)
        self.find_place()
        
        return True

    def unplay_last_piece( self ):
        # modify the board and remove the last move
        
        p_id = self.moves.pop()
        self.played_pieces.remove(p_id)
        
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == p_id:
                    self.board[i][j] = 0
        
        self.find_place()
    
    def load_board(self, board : list[list], moves ):
        self.board = board
        
        self.moves = moves
        
        self.played_pieces = set(moves)
        
        self.find_place()
        # need the history then the board