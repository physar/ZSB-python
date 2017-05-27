from __future__ import print_function
from copy import deepcopy
import sys

## Helper functions

# Translate a position in chess notation to x,y-coordinates
# Example: c3 corresponds to (2,5)
def to_coordinate(notation):
    x = ord(notation[0]) - ord('a')
    y = 8 - int(notation[1])
    return (x, y)

# Translate a position in x,y-coordinates to chess notation
# Example: (2,5) corresponds to c3
def to_notation(coordinates):
    (x,y) = coordinates
    letter = chr(ord('a') + x)
    number = 8 - y
    return letter + str(number)

# Translates two x,y-coordinates into a chess move notation
# Example: (1,4) and (2,3) will become b4c5
def to_move(from_coord, to_coord):
    return to_notation(from_coord) + to_notation(to_coord)

## Defining board states

# These Static classes are used as enums for:
# - Material.Rook
# - Material.King
# - Material.Pawn
# - Side.White
# - Side.Black
class Material:
    Rook, King, Pawn = ['r','k','p']
class Side:
    White, Black = range(0,2)

# A chesspiece on the board is specified by the side it belongs to and the type
# of the chesspiece
class Piece:
    def __init__(self, side, material):
        self.side = side
        self.material = material


# A chess configuration is specified by whose turn it is and a 2d array
# with all the pieces on the board
class ChessBoard:
    
    def __init__(self, turn):
        # This variable is either equal to Side.White or Side.Black
        self.turn = turn
        self.board_matrix = None


    ## Getter and setter methods 
    def set_board_matrix(self,board_matrix):
        self.board_matrix = board_matrix

    # Note: assumes the position is valid
    def get_boardpiece(self,position):
        (x,y) = position
        if(x > 7 or x < 0 or y > 7 or y < 0):
            return None
        return self.board_matrix[y][x]

    # Note: assumes the position is valid
    def set_boardpiece(self,position,piece):
        (x,y) = position
        self.board_matrix[y][x] = piece
    
    # Read in the board_matrix using an input string
    def load_from_input(self,input_str):
        self.board_matrix = [[None for _ in range(8)] for _ in range(8)]
        x = 0
        y = 0
        for char in input_str:
            print(char)
            if char == '\r':
                continue
            if char == '.':
                x += 1
                continue
            if char == '\n':
                x = 0
                y += 1
                continue 
            
            if char.isupper():
                side = Side.White
            else:
                side = Side.Black
            material = char.lower()

            piece = Piece(side, material)
            self.set_boardpiece((x,y),piece)
            x += 1

    # Print the current board state
    def __str__(self):
        return_str = ""

        return_str += "   abcdefgh\n\n"
        y = 8
        for board_row in self.board_matrix:
            return_str += str(y) + "  " 
            for piece in board_row:
                if piece == None:
                    return_str += "."
                else:
                    char = piece.material
                    if piece.side == Side.White:
                        char = char.upper()
                    return_str += char
            return_str += '\n'
            y -= 1
        
        turn_name = ("White" if self.turn == Side.White else "Black") 
        return_str += "It is " + turn_name + "'s turn\n"

        return return_str

    # Given a move string in chess notation, return a new ChessBoard object
    # with the new board situation
    # Note: this method assumes the move suggested is a valid, legal move
    def make_move(self, move_str):
        
        (start_x, start_y) = to_coordinate(move_str[0:2])
        (end_x, end_y) = to_coordinate(move_str[2:4])

        if self.turn == Side.White:
            turn = Side.Black
        else:
            turn = Side.White
            
        # Duplicate the current board_matrix and apply the move
        new_matrix = [row[:] for row in self.board_matrix]
        piece = new_matrix[start_y][start_x] 
        new_matrix[end_y][end_x] = piece
        new_matrix[start_y][start_x] = None
        
        # Create a new chessboard object
        new_board = ChessBoard(turn)
        new_board.set_board_matrix(new_matrix)

        return new_board

    
    ### BEGIN OF CODE TO IMPLEMENT BY STUDENT ###
    def legal_moves(self):
        
        moves = []
        for x in range(8):
            for y in range(8):
                piece = self.get_boardpiece((x,y))
                if piece != None and piece.side == self.turn:
                    pos = []
                    if piece.material == Material.Rook:
                        pos = self.legal_rook_moves(x,y)
                    if piece.material == Material.Pawn:
                        pos = self.legal_pawn_moves(x,y)
                    if piece.material == Material.King:
                        pos = self.legal_king_moves(x,y)

                    moves += map(lambda l: to_move((x,y),l), pos)
        
        return moves

    def is_legal_move(self,move):
        return move in self.legal_moves()

    def legal_king_moves(self, king_x, king_y):

        positions = []
        possible = [
                (king_x, king_y - 1), (king_x, king_y + 1), \
                (king_x - 1, king_y - 1), (king_x - 1, king_y), \
                (king_x -1, king_y + 1), (king_x + 1, king_y - 1), \
                (king_x + 1, king_y), (king_x +1, king_y + 1)]

        for pos in possible:
            (x,y) = pos
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            piece = self.get_boardpiece(pos)
            if piece != None and piece.side == self.turn:
                continue
            positions.append(pos)
        return positions

    def legal_pawn_moves(self, pawn_x, pawn_y):

        positions = []

        if pawn_y == 0 and self.turn == Side.White:
            return []
        if pawn_y >= 7 and self.turn == Side.Black:
            return []

        new_y = pawn_y
        if self.turn == Side.White:
            new_y -= 1
        if self.turn == Side.Black:
            new_y += 1
        
        pos = (pawn_x, new_y)
        if self.get_boardpiece(pos) == None:
            positions.append(pos)
        
        cross_pos1 = (pawn_x + 1, new_y)
        piece = self.get_boardpiece(cross_pos1)
        if piece != None and self.turn != piece.side:
            positions.append(cross_pos1)

        cross_pos2 = (pawn_x - 1, new_y)
        piece = self.get_boardpiece(cross_pos2)
        if piece != None and self.turn != piece.side:
            positions.append(cross_pos2)

        return positions

    def legal_rook_moves(self,rook_x,rook_y):
        
        positions = []
        cur_pos_x = rook_x + 1
        while(True):
            if(cur_pos_x > 7):
                break
            board_pos = self.board_matrix[rook_y][cur_pos_x]
            if board_pos == None:
                positions.append((cur_pos_x, rook_y))
                cur_pos_x += 1
                continue
            elif board_pos.side != self.turn:

                positions.append((cur_pos_x, rook_y))
                break
            else:
                break

        cur_pos_y = rook_y + 1
        while(True):
            if(cur_pos_y > 7):
                break
            board_pos = self.board_matrix[cur_pos_y][rook_x]
            if board_pos == None:
                positions.append((rook_x, cur_pos_y))
                cur_pos_y += 1
                continue
            elif board_pos.side != self.turn:

                positions.append((rook_x, cur_pos_y))
                break
            else:
                break


        cur_pos_y = rook_y - 1
        while(True):
            if(cur_pos_y < 0):
                break
            board_pos = self.board_matrix[cur_pos_y][rook_x]
            if board_pos == None:
                positions.append((rook_x, cur_pos_y))
                cur_pos_y -= 1
                continue
            elif board_pos.side != self.turn:

                positions.append((rook_x, cur_pos_y))
                break
            else:
                break

        cur_pos_x = rook_x - 1
        while(True):
            if(cur_pos_x < 0):
                break
            board_pos = self.board_matrix[rook_y][cur_pos_x]
            if board_pos == None:
                positions.append((cur_pos_x, rook_y))
                cur_pos_x -= 1
                continue
            elif board_pos.side != self.turn:
                positions.append((cur_pos_x, rook_y))
                break
            else:
                break

        return positions
    ### END OF CODE TO IMPLEMENT BY STUDENT

# This static class is responsible for providing functions that can calculate
# the optimal move using minimax
class ChessComputer:

    # This method uses either alphabeta or minimax to calculate the best move
    # possible. The input needed is a chessboard configuration and the max
    # depth of the search algorithm. It returns a tuple of (score, chessboard)
    # with score the maximum score attainable and chessboardmove that is needed
    #to achieve this score.
    @staticmethod
    def computer_move(chessboard, depth, alphabeta=False):
        if alphabeta:
            inf = 99999999
            min_inf = -inf
            return ChessComputer.alphabeta(chessboard, depth, min_inf, inf)
        else:
            return ChessComputer.minimax(chessboard, depth)


    # This function uses minimax to calculate the next move. Given the current
    # chessboard and max depth, this function should return a tuple of the
    # the score and the move that should be executed
    # NOTE: use ChessComputer.evaluate_board(chessboard) to calculate the score
    # of a specific board configuration after the max depth is reached
    @staticmethod
    def minimax(chessboard, depth):
        ### BEGIN OF CODE TO IMPLEMENT BY STUDENT
        if depth == 0:
            return ChessComputer.evaluate_board(chessboard), "----"

        moves = chessboard.legal_moves()

        scores = {}
        for move in moves:
            new_board = chessboard.make_move(move)
            score, _ = ChessComputer.minimax(new_board, depth - 1)
            scores[move] = score
        if len(moves) == 0:
            return ChessComputer.evaluate_board(chessboard) + depth*10, "----"
        
        if chessboard.turn == Side.White:
            best_board = max(scores, key=scores.get)
            return (scores[best_board], best_board)
        else:
            best_board = min(scores, key=scores.get)
            return (scores[best_board], best_board)
        ### END OF CODE TO IMPLEMENT BY STUDENT

    # This function uses alphabeta to calculate the next move. Given the
    # chessboard and max depth, this function should return a tuple of the
    # the score and the move that should be executed.
    # It has alpha and beta as extra pruning parameters
    # NOTE: use ChessComputer.evaluate_board(chessboard) to calculate the score
    # of a specific board configuration after the max depth is reached
    @staticmethod
    def alphabeta(chessboard, depth, alpha, beta):
        ### BEGIN OF CODE TO IMPLEMENT BY STUDENT
        inf = 99999999
        min_inf = -inf
        if depth == 0:
            return ChessComputer.evaluate_board(chessboard), "----"

        moves = chessboard.legal_moves()

        if len(moves) == 0:
            return ChessComputer.evaluate_board(chessboard) + depth*10, "----"

        move_for_v = ""
        if chessboard.turn == Side.White:
            v = min_inf
        else:
            v = inf
        for move in moves:
            new_board = chessboard.make_move(move)
            score, _ = ChessComputer.alphabeta(new_board, depth-1, alpha, beta)
            if chessboard.turn == Side.White:
                if score > v:
                    v = score
                    move_for_v = move
                alpha = max(alpha, v)
            else:
                if score < v:
                    v = score
                    move_for_v = move
                beta = min(beta, v)
            
            if beta <= alpha:
                break
        
        return v, move_for_v
        ### END OF CODE TO IMPLEMENT BY STUDENT
    
    # Calculates the score of a given board configuration based on the 
    # material left on the board. Returns a score number, in which positive
    # means white is better off, while negative means black is better of
    @staticmethod
    def evaluate_board(chessboard):
        ### BEGIN OF CODE TO IMPLEMENT BY STUDENT
        board_values = {}
        board_values[Material.Pawn] = 100
        board_values[Material.King] = 1000
        board_values[Material.Rook] = 500

        
        score = 0
        
        for x in range(8):
            for y in range(8):
                piece = chessboard.get_boardpiece((x,y))
                
                if piece == None:
                    continue

                if piece.side == Side.White:
                    multiplier = 1
                else:
                    multiplier = -1
                
                score += multiplier * board_values[piece.material]

        return score
        ### END OF CODE TO IMPLEMENT BY STUDENT
        
# This class is responsible for starting the chess game, playing and user 
# feedback
class ChessGame:
    def __init__(self, turn):
     
        board = "...K...k\n" + \
                "........\n" + \
                "........\n" + \
                "........\n" + \
                ".....R..\n" + \
                "........\n" + \
                "........\n" + \
                "........\n"

        self.depth = 7
        self.chessboard = ChessBoard(turn)
        self.chessboard.load_from_input(board)


    def load_from_file(self, filename):

        with open(filename) as f:
            content = f.readlines()

        self.chessboard.load_from_input(content)

    def main(self):
        while True:
            print(self.chessboard)

            # Print the current score
            current_score = ChessComputer.evaluate_board(self.chessboard)
            print("Current score: " + str(current_score))
            
            # Calculate the best possible move
            new_score, best_move = self.make_computer_move()
            
            print("Best move: " + best_move)
            print("Score to achieve: " + str(new_score))
            self.make_human_move()


    def make_computer_move(self):
        return ChessComputer.computer_move(self.chessboard,
                self.depth, alphabeta=True)
        

    def make_human_move(self):
        while True:
            move = input("Indicate your move: ")
            if self.chessboard.is_legal_move(move):
                break
            print("Incorrect move!")

        self.chessboard = self.chessboard.make_move(move)

chess_game = ChessGame(Side.White)
chess_game.main()

