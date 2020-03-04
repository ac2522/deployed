from django.db import models
from django.contrib.auth.models import User
import random

class Chess_board(object): 
    def __init__(self):
        
        self.free = [str(i) + j for i in range(8) for j in 'abcdefgh']
        self.rep = {}
        for i in self.free:
            self.rep[i] = 0
        self.rep_copy = self.rep.copy()
        self.free_copy = self.free.copy()
        self.king1 = 0
        self.moves = {}
        self.mate_moves = {}
        self.generate()


    def generate(self):
        # loading icon
        possible_mate = False
        pieces = 'PPPPPPPPNNRRBBQ'
        i=1
        while possible_mate == False:
            self.rep = self.rep_copy.copy()
            self.free = self.free_copy.copy()
            king0 = self.place('K0', ret=True)
            percentage = random.choice([0.1,0.5,0.9])
            for piece in pieces:
                if random.random() < percentage:
                    self.place(piece + '0')
            percentage *= 0.8
            for piece in pieces:
                if random.random() < percentage:
                    if self.place2(piece + '1', king0) == False:
                        break
            if self.placeK(king0) == True:
                possible_mate = True


    def place(self, piece, ret=False):
        spaces = self.free.copy()
        if 'P' in piece:
            spaces = [i for i in spaces if not i[0] in ['0','7']]
        if ('B' in piece) and ('B0' in self.rep.values()):
            square_col = next((pos for pos, piece in self.rep.items() if piece == 'B0'), None)
            square_col = (int(square_col[0]) + ord(square_col[1]))%2
            for i in self.free:
                if square_col == (int(i[0]) + ord(i[1]))%2:
                    spaces.remove(i)
        position = random.choice(spaces)
        self.rep[position] = piece 
        self.free.remove(position)
        if ret == True:
            return position
        
        
    def place2(self, piece, k_position):
        spaces = self.free.copy()
        if 'P' in piece:
            spaces = [i for i in spaces if not i[0] in ['0','7']]
        if ('B' in piece) and ('B1' in self.rep.values()):
            square_col = next((pos for pos, piece in self.rep.items() if piece == 'B1'), None)
            square_col = (int(square_col[0]) + ord(square_col[1]))%2
            for i in self.free:
                if square_col == (int(i[0]) + ord(i[1]))%2:
                    spaces.remove(i)
        position = random.choice(spaces)
        while self.check_single(k_position, position, piece) == True:
            if len(spaces) == 1: 
                return False
            else: 
                spaces.remove(position)
                position = random.choice(spaces)
        self.rep[position] = piece 
        self.free.remove(position)
        if len(self.free) == 0:
            return False
        return True
    
    
    
    def placeK(self, king0):
        spaces = self.free.copy()
        free__copy = self.free.copy()
        free__rep = self.rep.copy()
        not_found = True
        while not_found == True:
            self.free = free__copy.copy()
            self.rep = free__rep.copy()
            if len(spaces) == 0:
                return False
            position = random.choice(spaces)
            spaces.remove(position)
            self.free.remove(position)
            self.rep[position] = 'K1'
            self.king1 = position
            if self.check(position, '0') == True:
                continue
            if self.mate(king0, '0') == False:
                continue
            self.mate(king0, '0', analyse=True)
            return True
        

    
    def check(self, k_position, col):
        for piece in 'KQRBNP':
            piec = piece + col
            for p_position in [key  for (key, value) in self.rep.items() if value == piec]:
                if self.check_single(k_position, p_position, piec) == True:
                    return True
        return False                


    def check_single(self, k_position, p_position, piece):
        if 'K' in piece:
            if (abs(int(k_position[0]) - int(p_position[0]))) <= 1 and (abs(ord(k_position[1]) - ord(p_position[1])) <= 1):
                return True
        
        elif ('R' in piece) or ('Q' in piece):
            in_check = True
            if k_position[0] == p_position[0]:
                min_ = min(ord(k_position[1]), ord(p_position[1]))
                max_ = max(ord(k_position[1]), ord(p_position[1]))
                for pos in range(min_ + 1, max_):
                    if k_position[0] + chr(pos) not in self.free:
                        in_check = False
                if in_check == True:
                    return True
            if k_position[1] == p_position[1]:
                min_ = min(int(k_position[0]), int(p_position[0]))
                max_ = max(int(k_position[0]), int(p_position[0]))
                for pos in range(min_ + 1, max_):
                    if str(pos) + k_position[1] not in self.free:
                        in_check = False
                if in_check == True:
                    return True
        
        elif 'N' in piece:
            if (abs(int(k_position[0]) - int(p_position[0]))) == 1 and (abs(ord(k_position[1]) - ord(p_position[1])) == 2):
                return True
            if (abs(int(k_position[0]) - int(p_position[0]))) == 2 and (abs(ord(k_position[1]) - ord(p_position[1])) == 1):
                return True
        
        elif piece == 'P0':
            if int(k_position[0]) - int(p_position[0]) == 1 and abs(ord(k_position[1]) - ord(p_position[1])) == 1:
                return True
            elif int(p_position[0]) == 7:
                for promoted in ['Q0','N0']:
                    if self.check_single(k_position, p_position, promoted):
                        return True
        elif piece == 'P1':
            if int(p_position[0]) - int(k_position[0]) == 1 and abs(ord(k_position[1]) - ord(p_position[1])) == 1:
                return True
            elif int(p_position[0]) == 0:
                for promoted in ['Q1','N1']:
                    if self.check_single(k_position, p_position, promoted): 
                        return True
            
        if 'B' in piece or 'Q' in piece:
            in_check = True; enumerat = 0
            if abs(int(k_position[0]) - int(p_position[0])) == abs(ord(k_position[1]) - ord(p_position[1])):
                if int(k_position[0]) > int(p_position[0]) and ord(k_position[1]) > ord(p_position[1]):
                    for pos in range(int(p_position[0]) + 1, int(k_position[0])):
                        enumerat += 1
                        if str(pos) + chr(ord(p_position[1]) + enumerat) not in self.free:
                            in_check = False
                    if in_check == True:
                        return True
                elif int(k_position[0]) < int(p_position[0]) and ord(k_position[1]) > ord(p_position[1]):
                    for pos in range(int(k_position[0]) + 1, int(p_position[0])):
                        enumerat += 1
                        if str(pos) + chr(ord(k_position[1]) - enumerat) not in self.free:
                            in_check = False
                    if in_check == True:
                        return True
                elif int(k_position[0]) > int(p_position[0]) and ord(k_position[1]) < ord(p_position[1]):
                    for pos in range(int(p_position[0]) + 1, int(k_position[0])):
                        enumerat += 1
                        if str(pos) + chr(ord(p_position[1]) - enumerat) not in self.free:
                            in_check = False
                    if in_check == True:
                        return True
                else:
                    for pos in range(int(k_position[0]) + 1, int(p_position[0])):
                        enumerat += 1
                        if str(pos) + chr(ord(k_position[1]) + enumerat) not in self.free:
                            in_check = False
                    if in_check == True:
                        return True
        return False

    def mate(self, king0, col, analyse=False):
        for piece in 'QRBNPK':
            piec = piece + col
            for p_position in [key  for (key, value) in self.rep.items() if value == piec]:
                if self.move_mate(piec, p_position, king0, col, analysis=analyse) == False:
                    continue
                else:
                    return True
        return False


    def move_mate(self, piece, p_position, king0, col, analysis=False):
        
        if col == '0':
            col1 = '1'
        else: 
            col1 ='0'
        moves = []

        if 'K' in piece:
            for x in range(-1,2):
                for y in range(-1,2):
                    moves.append(str(int(p_position[0]) + x) + chr(ord(p_position[1]) + y))
            for i in moves.copy():
                if i not in self.rep:
                    moves.remove(i)
                elif (self.rep[i] != 0) and (col in self.rep[i]):
                    moves.remove(i)
                elif piece == 'K0':
                    if (abs(int(self.king1[0]) - int(i[0]))) <= 1 and (abs(ord(self.king1[1]) - ord(i[1])) <= 1):
                        moves.remove(i)
                    #[moves.remove(i) for i in moves if i not in self.rep]
                    #[moves.remove(i) for i in moves if 0 == self.rep[i]]
                    #[moves.remove(i) for i in moves if col1 in self.rep[i]]          <- int error

        if ('R' in piece) or ('Q' in piece):
            for arb in [1,-1]:
                for row in range(1,8):
                    taken = str(int(p_position[0]) + row * arb) + p_position[1]
                    if taken not in self.rep:
                        break
                    if self.rep[taken] == 0:
                        moves.append(taken)
                    elif col in self.rep[taken]:
                        break
                    elif col1 in self.rep[taken]:
                        moves.append(taken)
                        break
                for column in range(1,8):
                    taken = p_position[0] + chr(ord(p_position[1]) + column * arb)
                    if taken not in self.rep:
                        break
                    if self.rep[taken] == 0:
                        moves.append(taken)
                    elif col in self.rep[taken]:
                        break
                    elif col1 in self.rep[taken]:
                        moves.append(taken)
                        break

        if ('B' in piece) or ('Q' in piece):
            for column in [1,-1]:
                for row in [1,-1]:
                    for arb in range(1,8):
                        taken = str(int(p_position[0]) + arb * row) + chr(ord(p_position[1]) + arb * column)
                        if taken not in self.rep:
                            break
                        if self.rep[taken] == 0:
                            moves.append(taken)
                        elif col in self.rep[taken]:
                            break
                        elif col1 in self.rep[taken]:
                            moves.append(taken)
                            break
            
        if 'N' in piece:
            for x in [2,-2]:
                for y in [1,-1]:                    
                    moves.append(str(int(p_position[0]) + x) + chr(ord(p_position[1]) + y))
                    moves.append(str(int(p_position[0]) + y) + chr(ord(p_position[1]) + x))
            for i in moves.copy():
                if i not in self.rep:
                    moves.remove(i)
                elif (self.rep[i] != 0) and (col in self.rep[i]):
                    moves.remove(i)

        if 'P' in piece:
            direction = 1 - 2 * int(col)
            if (str(int(p_position[0]) + direction) + p_position[1]) in self.free:
                moves.append(str(int(p_position[0]) + direction) + p_position[1])
                if (col == '0') and ('1' in p_position) and (('3' + p_position[1]) in self.free):
                    moves.append('3' + p_position[1])
                if (col == '1') and ('6' in p_position) and (('4' + p_position[1]) in self.free):
                    moves.append('4' + p_position[1])
            for y in [1,-1]:
                diagonal = str(int(p_position[0]) + direction) + chr(ord(p_position[1]) + y)
                if diagonal in self.rep:
                    if (self.rep[diagonal] != 0) and (col1 in self.rep[diagonal]):
                        moves.append(str(int(p_position[0]) + direction) + chr(ord(p_position[1]) + y))
            for move in moves.copy():  # for knight and queen
                if '7' in move:
                    moves.append(move)

        possible_rep = self.rep.copy()
        possible_free = self.free.copy()
        already_seen = []
        for move in moves.copy():
            self.rep[move] = piece
            self.rep[p_position] = 0
            if move in self.free:
                self.free.remove(move)
            self.free.append(p_position)
            if col == '1' and piece == 'K1':
                king0 = move
            if self.check(king0, col1) == True:  # is player 1 in check
                moves.remove(move)
            self.rep = possible_rep.copy()
            self.free = possible_free.copy()
        if col == '1':
            if len(moves) >= 1:
                return True
            else: 
                return False

        if analysis == True: self.moves[p_position] = moves
        king1 = self.king1
        possible_rep = self.rep.copy()
        possible_free = self.free.copy()
        for pos_move in moves:  # for each move that can be made
            if piece == 'P0' and '7' in pos_move: # needs work
                if pos_move in already_seen:
                    self.rep[pos_move] = 'N0'
                else:
                    self.rep[pos_move] = 'Q0'
                    already_seen.append(pos_move)
            else:
                self.rep[pos_move] = piece
            self.rep[p_position] = 0
            if pos_move in self.free:
                self.free.remove(pos_move)
            self.free.append(p_position)
            if self.check(king1, '0') == True:  # does the move put other player in check
                if self.mate(king1, '1') == False:  # can they make move that stops check
                    self.rep = possible_rep.copy()
                    self.free = possible_free.copy()
                    if analysis == True: 
                        if p_position in self.mate_moves:
                            self.mate_moves[p_position].append(pos_move)
                        else:
                            self.mate_moves[p_position] = [pos_move]
                    else:
                        return True
            self.rep = possible_rep.copy()
            self.free = possible_free.copy()
        return False
