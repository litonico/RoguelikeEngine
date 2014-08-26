from utility import Pos, N, S, E, W, UP, DN, NONE
from entities import Entity, Hero
from tiles import *
from asciirenderer import ASCIIRenderer

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
