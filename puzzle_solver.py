import itertools
import collections

class Connection(object):
    POSITIVE = '+'
    NEGATIVE = '-'
    def __init__(self, shape=None, polarity=None):
        self.shape = shape
        self.polarity = polarity
        
    def __repr__(self):
        return 'Connection(%s, %s)' % (self.shape, self.polarity)
    
    def __eq__(self, other):
        return self.shape == other.shape and self.polarity == other.polarity
    
    def connects(self, other):
        return self.shape == other.shape and self.polarity != other.polarity
        
class Piece (object):
    def __init__(self, n, e, s, w):
        self.n = n
        self.e = e
        self.w = w
        self.s = s
        
    def __repr__(self):
        return 'Piece(n=%s, e=%s, s=%s, w=%s)' % (self.n, self.e, self.s, self.w)
    
    def __eq__(self, other):
        return (self.n, self.e, self.w, self.s) == (other.n, other.e, other.w, other.s)
        
    def rotated(self):
        ''' Return a new piece that has the same connections as the current piece, but rotated 90deg counterclockwise'''
        return Piece(self.e, self.s, self.w, self.n)
    
    def all_rotations(self):
        '''Return an iterator over all four rotations of this piece'''
        piece = self
        yield piece
        for _ in xrange(3):
            piece = piece.rotated()
            yield piece
            
    def is_rotation_of(self, other):
        for rotation in self.all_rotations():
            if rotation == other:
                return True
        return False
        
def valid_pieces(board, open_list, pos):
    '''Yield tuple of (piece, rotation_that_fits) for each piece in the open_list that fits'''
    top_neighbor = board[pos - 3] if pos >= 3 else None
    left_neighbor = board[pos - 1] if pos % 3 > 0 else None
    
    for piece in open_list:
        # Test all rotations of each piece.
        for rotation in piece.all_rotations():
            if top_neighbor is not None and not top_neighbor.s.connects(rotation.n):
                continue
            if left_neighbor is not None and not left_neighbor.e.connects(rotation.w):
                continue
            yield piece, rotation
            break
    
def search(board, open_list, pos):
    if pos > 8:
        # Solution found.
        return board
    
    for piece, rotation in valid_pieces(board, open_list, pos):
        print piece, rotation
        next_board = board[:]
        next_board[pos] = rotation
        next_open_list = open_list[:]
        next_open_list.remove(piece)
        
        print next_board
        
        result = search(next_board, next_open_list, pos + 1)
        if result is not None:
            return result
    return None

def find_solution(pieces):
    board = [None] * 9
    return search(board, pieces, 0)
    
        
if __name__ == '__main__':
    si = Connection('spade',   Connection.NEGATIVE)
    hi = Connection('heart',   Connection.NEGATIVE)
    di = Connection('diamond', Connection.NEGATIVE)
    ci = Connection('club',    Connection.NEGATIVE)
    
    so = Connection('spade',   Connection.POSITIVE)
    ho = Connection('heart',   Connection.POSITIVE)
    do = Connection('diamond', Connection.POSITIVE)
    co = Connection('club',    Connection.POSITIVE)
    
    pieces = [
        Piece(ho,ci,si,so),
        Piece(ho,ci,ci,do),
        Piece(so,ci,hi,so),
        Piece(so,di,hi,do),
        Piece(so,hi,si,do),
        Piece(ho,hi,di,do),
        Piece(do,di,ci,co),
        Piece(co,hi,si,ho),
        Piece(co,ci,di,ho),
    ]
    
    def print_board(board):
        fill = '|   |   |   |'
        ch = lambda c:c.shape[0]
        prv = lambda r:'+-' + '-+-'.join((ch(p.n) if p else '-') for p in r) + '-+'
        prh = lambda r: '   '.join(ch(p.w) if p else '|' for p in r) + '   ' + (ch(r[-1].e) if r[-1] else '|')
        for i in xrange(0, 7, 3):
            print prv(board[i:i+3])
            print fill
            print prh(board[i:i+3])
            print fill
        print '+-' + '-+-'.join((ch(p.s) if p else '-') for p in board[-3:]) + '-+'
    
   
    solution = find_solution(pieces)
    if solution:
        print_board(solution)
    else:
        print 'No solution found'