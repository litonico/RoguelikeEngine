import sys
from utility import Pos, N, S, E, W, UP, DN, NONE
from entities import Entity, Hero
from tiles import *

class ASCIIRenderer(object):
    ''' Graphics engine - writes to console '''
    # Realllly primitive graphics

    def __init__(self, game):
        self.game = game

    '''
    # Not ready to include this
    def setcolor(color, char):
        styles = {
                'default': '\x1b[39;49m',
                'grey': '\x1b[30;0m',
                'red': '\x1b[31'
                }
        return lambda x: \
            sys.stdout.write(styles[c])
            sys.stdout.write(char)
            sys.stdout.write(styles['default'])
    '''

    def get_user_input(self):
        return input()

    def generate_buffer(self):
        '''Blit the sprites in @game (ASCII chars) onto a buffer'''
        # Write the 'world' to the buffer
        # Only the current z-index is drawn
        self.buf = [
                tile.sprite for tile in self.game.world[self.game.hero.pos.z]
                ]

        # On top of that, draw items (not implemented)

        # On top of that, draw the characters
        for entity in game.entities:
            if entity.pos.z == game.hero.pos.z:
                self.buf[game.flatten(entity.pos)] = entity.sprite

    def render(self):
        ''' Draw the buffer to STDOUT '''
        # Also surrounds the map with '#'
        
        #--Border
        for i in range(self.game.dim_x+1):
            sys.stdout.write('#')
        # Draw the actual game
        for index, char in enumerate(self.buf):
            # Write newline if neccesary
            if index % self.game.dim_x == 0: 
                sys.stdout.write('#') #--Border
                sys.stdout.write('\n')
                sys.stdout.write('#') #--Border
            sys.stdout.write(char)

        #--Border
        sys.stdout.write('#')
        sys.stdout.write('\n')
        for i in range(self.game.dim_x+1):
            sys.stdout.write('#')
        sys.stdout.write('\n')



class Game(object):
    '''Args: the dimensions (x, y, z) of the map'''
    def __init__(self, dim_x, dim_y, dim_z):
        self.dim_x, self.dim_y, self.dim_z = dim_x, dim_y, dim_z
        self.world = [
                [dirt_block for i in range(dim_x*dim_y)] for j in range(dim_z)]

        self.hero = Hero(self,
                        'hero',
                        '@',
                        # Starts at the middle of the top layer
                        Pos(dim_x//2, dim_y//2, 0))

        self.entities = [self.hero] #TODO: Un-hardcode
        self.active_entity = 0

        # Things that happened in a step before an update
        self.events = []
        self.ui = ASCIIRenderer(self)

    def flatten(self, pos):
        ''' Transforms 2D (x, y) coords to a 1D list '''
        # The modulus calculations check for wraparound: 
        # otherwise, there will be calls that raise an IndexError
        return (pos.x % self.dim_x) + (pos.y % self.dim_y)*self.dim_x

    def step(self):
        ''' Let each entity in the game take an action '''
        action = self.entities[self.active_entity].get_action()
        action.bind(self.entities[self.active_entity])
        # result stores SUCCESS or FAILURE
        result = action.execute()
        self.active_entity = (self.active_entity + 1) % len(self.entities)


def main_loop(game, renderer):
    ui = renderer(game)
    while True:
        game.step()
        ui.generate_buffer()
        ui.render()

if __name__ == "__main__":
    game = Game(16, 8, 16)
    main_loop(game, ASCIIRenderer)
