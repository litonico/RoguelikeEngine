class Tile(object):
    ''' Ground or wall object '''
    def __init__(self, name, sprite):
        self.name = name
        self.sprite = sprite

    
dirt_block = Tile('dirt', '.')
stone_block = Tile('stone', '#')
empty_space = Tile('space', ' ')
