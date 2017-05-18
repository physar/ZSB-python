from __future__ import print_function
from copy import deepcopy


def to_coordinate(notation):
    x = ord(notation[0]) - ord('a')
    y = 8 - int(notation[1])
    return (x, y)

def to_notation(coordinates):
    (x,y) = coordinates
    letter = chr(ord('a') + x)
    number = 8 - y
    return letter + str(number)

def to_move(from_coord, to_coord):
    return to_notation(from_coord) + to_notation(to_coord)

class Material:
    Rook, King, Pawn = ['r','k','p']

class Side:
    White, Black = range(0,2)

class Piece:
    def __init__(self, side, material):
        self.side = side
        self.material = material


class ChessBoard:
    
    def __init__(self, turn, board_str):
        self.turn = turn
        self.board_matrix = None
        if board_str != "":
            self.load_from_input(board_str)


    def set_board_matrix(self,board_matrix):
        self.board_matrix = board_matrix

    def __str__(self):
        return_str = ""

        #return_str += "     01234567\n"
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
        
        return_str +="It is " + ("White" if self.turn == Side.White else "Black" ) + "'s turn\n"
        return return_str

    def make_move(self, move_str):
        (start_x, start_y) = to_coordinate(move_str[0:2])
        (end_x, end_y) = to_coordinate(move_str[2:4])

        #print("x: " + str(start_x) + " y: " + str(start_y))
        #print("x: " + str(end_x) + " y: " + str(end_y))

        #new_board = deepcopy(self)

        if self.turn == Side.White:
            turn = Side.Black
        else:
            turn = Side.White
            
        new_matrix = [row[:] for row in self.board_matrix]
        new_board = ChessBoard(turn,"")
        new_board.set_board_matrix(new_matrix)

        piece = new_board.board_matrix[start_y][start_x] 
        new_board.board_matrix[end_y][end_x] = piece
        new_board.board_matrix[start_y][start_x] = None

        

        return new_board

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
            
            
            
                    
    def is_legal_move(self,move):
        return move in self.legal_moves()


    def legal_king_moves(self, king_x, king_y):

        positions = []
        possible = [
                (king_x, king_y - 1), (king_x, king_y + 1), \
                (king_x - 1, king_y - 1), (king_x - 1, king_y), (king_x -1, king_y + 1), \
                (king_x + 1, king_y - 1), (king_x + 1, king_y), (king_x +1, king_y + 1)]

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


    def get_boardpiece(self,position):
        (x,y) = position
        if(x > 7 or x < 0 or y > 7 or y < 0):
            return None
        return self.board_matrix[y][x]

    def set_boardpiece(self,position,piece):
        (x,y) = position
        
        self.board_matrix[y][x] = piece

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
        #return list(map(to_notation,positions))


class ChessComputer:
    @staticmethod
    def minimax(chessboard, depth):
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
            

    @staticmethod
    def alphabeta(chessboard, depth, alpha, beta):
        if depth == 0:
            return ChessComputer.evaluate_board(chessboard), "----"

        moves = chessboard.legal_moves()

        if len(moves) == 0:
            return ChessComputer.evaluate_board(chessboard) + depth*10, "----"

        move_for_v = ""
        if chessboard.turn == Side.White:
            v = -999999
        else:
            v = 999999
        for move in moves:
            new_board = chessboard.make_move(move)
            score, _ = ChessComputer.alphabeta(new_board, depth - 1, alpha, beta)
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


    @staticmethod
    def evaluate_board(chessboard):
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
        

class ChessGame:
    def __init__(self, turn):
     
        board = "r..k...r\n" + \
                "pppppppp\n" + \
                "........\n" + \
                "........\n" + \
                "........\n" + \
                "........\n" + \
                "PPPPPPPP\n" + \
                "R..K...R\n"

        board = "...K...k\n" + \
                "........\n" + \
                "........\n" + \
                "........\n" + \
                ".....R..\n" + \
                "........\n" + \
                "........\n" + \
                "........\n"

        self.chessboard = ChessBoard(turn,board)


    def main(self):
        while True:
            print(self.chessboard)

            print("current score: " + str(ChessComputer.evaluate_board(self.chessboard)))
            score, board = self.make_computer_move()
            print("best score: " + str(score))
            print(board)
            self.make_human_move()


    def make_computer_move(self):
        return ChessComputer.alphabeta(self.chessboard, 7,-999999,999999)
        

    def make_human_move(self):
        while True:
            move = input("Indicate your move: ")
            if self.chessboard.is_legal_move(move):
                break
            print("Incorrect move!")

        self.chessboard = self.chessboard.make_move(move)


    def set_board_position(self, board_array):
        pass




chess_game = ChessGame(Side.White)
chess_game.main()


"""
    print(chess_board)
    moves = chess_board.legal_moves()
    for move in moves:
        print(chess_board.make_move(move))
"""
