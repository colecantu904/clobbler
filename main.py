import copy
from pathlib import Path
import json
from parts import Board, Piece

# pieces will be made from a nxn matrix of the 
# Each matrix represents a unique piece type found in the set.
# 1 represents a ball, 0 represents empty space.

kanoodle_pieces = [
    # 1. Square (4 spheres) - 2x2 matrix
    # Light Green in the image
    [[1, 1],
     [1, 1]],

    # 2. L-tromino (3 spheres) - 2x2 matrix
    # Dark Green in the image (small L)
    [[1, 1],
     [1, 0]],

    # 3. L-tetromino (4 spheres) - 3x3 matrix
    # Orange in the image
    [[1, 0],
     [1, 0],
     [1, 1]],

    # 4. Z-tetromino / Skew (4 spheres) - 3x3 matrix
    # Light Blue in the image
    [[1, 1, 0, 0],
     [0, 1, 1, 1]],

    # 5. P-pentomino (5 spheres) - 3x3 matrix
    # Yellow in the image
    [[1, 1],
     [1, 1],
     [1, 0]],

    # 6. Cross-pentomino (5 spheres) - 3x3 matrix
    # White in the image
    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]],

    # 7. V-pentomino (5 spheres) - 3x3 matrix
    # Dark Blue in the image
    [[1, 0, 0],
     [1, 0, 0],
     [1, 1, 1]],

    # 8. U-pentomino (5 spheres) - 3x3 matrix
    # Magenta/Pink in the image
    [[1, 0, 1],
     [1, 1, 1]],

    # 9. W-pentomino (5 spheres) - 3x3 matrix
    # Red in the image
    [[1, 0, 0],
     [1, 1, 0],
     [0, 1, 1]],

    # 10. Z-pentomino (5 spheres) - 3x3 matrix
    # Cyan in the image
    [[1, 1, 1, 1]],

    # 11. Y-pentomino (5 spheres) - 4x4 matrix
    # Peach in the image
    [[1, 0],
     [1, 1],
     [1, 0],
     [1, 0]],

    # 12. L-pentomino (5 spheres) - 4x4 matrix
    # Purple in the image
    [[1, 0],
     [1, 0],
     [1, 0],
     [1, 1]]
]


# ======================= #
#       Search Algo
# ======================= #

answers = []
        
# this works?
def find_solutions( board : Board, pieces : list[Piece], depth=0) -> list:
    global answers
    if depth > 10:
        print_board(board.board)
        print()
    if len(answers) >= 1:
        return
    if board.is_board_complete():
        #return [{"board" : copy.deepcopy(board.board), "moves" : copy.deepcopy(board.moves)}]
        answers.append({"board" : copy.deepcopy(board.board), "moves" : copy.deepcopy(board.moves)})
        print('answer found')
        print_board(board.board)
        return
    # if len(board.played_pieces) > 3:
    #     return [{"board" : copy.deepcopy(board.board), "moves" : copy.deepcopy(board.moves)}]
    if len(board.played_pieces) >= len(pieces):
        #return []
        return
    else:
        #local_answers = []
        
        for p in pieces:
            for rot in range(len(p.apr)):
                for dir in range(2):
                    move = board.play_piece(p, rot, dir)
                    
                    if move:
                        #branch_answers = find_solutions(board, pieces, depth+1)
                        find_solutions(board, pieces, depth+1)
                        
                        # for sol in branch_answers:
                        #     if sol not in local_answers:
                        #         local_answers.append(sol)
                    
                        board.unplay_last_piece()
                    
                        if len(answers) >= 1:
                            return
        
        #return local_answers
        return

# ======================= #
#       Data Saving
# ======================= #

def save_test_data( answers, pieces : list[Piece] ):
    tests_folder = Path('./tests')
    
    current_test = sum([1 for item in tests_folder.iterdir()])
    
    data = {
        "pieces" : [ { "id" : p.id, "schema" : p.s.tolist() } for p in pieces ],
        "tests" : answers
    }
    
    with open(f'./tests/{current_test}_test.json', 'w') as f:
        json.dump(data, f)
        

def read_test_data( path ) -> list:
    test_path = Path(path)
    
    with open(test_path, 'r') as file:
        data = json.load(file)
        
        return data

def print_board( board ):
    # 1. Find the maximum length of any item in the matrix
    # We convert items to strings first so we can measure their character length
    max_width = 0
    for row in board:
        for item in row:
            max_width = max(max_width, len(str(item)))

    # 2. Add a little extra buffer if you want space between columns
    padding = max_width + 2

    # 3. Print the grid using f-string padding
    # :>{padding} means "right-align this string, padding it to {padding} width"
    for row in board:
        print("".join(f"{str(item):>{padding}}" for item in row))

if __name__ == "__main__":
    b = Board(11, 5)
    
    pieces =[]
    for i in range(len(kanoodle_pieces)):
        pieces.append(Piece(kanoodle_pieces[i], i+1))
    
    # should not work... its causing way more game trees
    # b.play_piece(pieces[11], 3, 0)
    # print_board(b.board)
    
    
    
    # b.place = (4, 0)
    # b.play_piece(pieces[11], 3, 0)
    # print_board(b.board)
    
    # playing with fire...
    #find_solutions(b, pieces)
    
    #print(answers)
    
    #save_test_data( answers, pieces )
    
    #data = read_test_data('./tests/0_test.json')
    
    #b.load_board(data['tests'][0]['board'], data['tests'][0]['moves'])
    
    