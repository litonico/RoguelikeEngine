class Pos(object):
    ''' Positions of actors on the map '''
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        '''Pretty-printing for tests'''
        return 'Pos({0} {1} {2})'.format(self.x, self.y, self.z)

    def __add__(self, otherpos):
        # + operator for positons
        return Pos(
                self.x + otherpos.x, 
                self.y + otherpos.y, 
                self.z + otherpos.z)
    def __iadd__(self, otherpos):
        # += operator for positons
        self.x += otherpos.x
        self.y += otherpos.y
        self.z += otherpos.z

    def __mod__(self, otherpos):
        return Pos(
                self.x % otherpos.x, 
                self.y % otherpos.y, 
                self.z % otherpos.z)

N = Pos(0, -1, 0)
S = Pos(0, 1, 0)
W = Pos(1, 0, 0)
E = Pos(-1, 0, 0)
UP = Pos(0, 0, 1)
DN = Pos(0, 0, -1)
NONE = Pos(0, 0, 0)
