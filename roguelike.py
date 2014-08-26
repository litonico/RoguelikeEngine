import sys
# TODO: Factor entities, tiles, and actions to different files
# from entites import Entity, Hero

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


class Tile(object):
    ''' Ground or wall object '''
    def __init__(self, name, sprite):
        self.name = name
        self.sprite = sprite


class Action(object):
    def bind(self, actor):
        self.actor = actor
        self.game = actor.game

    def execute(self):
        raise NotImplementedError

SUCCESS = True
FAILURE = False

class Move(Action):
    def __init__(self, direction):
        self.direction = direction

    def execute(self):
        flatten = self.game.flatten

        if not self.actor:
            raise NameError('No actor bound to action %s', str(self))

        # Get the place the entity is trying to move into
        final_pos = self.actor.pos + self.direction
        grid = self.game.world[final_pos.z % self.game.dim_z]
        tile = grid[flatten(final_pos)]

        # These can access out of bounds, so they're calculated modulo
        # the game's height– this makes them wrap around
        ceiling = self.game.world[(final_pos.z+1) % self.game.dim_z]
        floor = self.game.world[(final_pos.z-1) % self.game.dim_z]

        # If there are no walls around the player, keep drifting in direction
        if ((grid[flatten(final_pos + N)] is empty_space) and
            (grid[flatten(final_pos + S)] is empty_space) and
            (grid[flatten(final_pos + E)] is empty_space) and
            (grid[flatten(final_pos + W)] is empty_space) and
            (floor[flatten(final_pos)] is empty_space) and
            (ceiling[flatten(final_pos)] is empty_space)):

            # Set next action
            self.actor.next_action = Drift(self.direction)

        if tile is empty_space:
            self.actor.pos = final_pos % Pos(self.game.dim_x, 
                                             self.game.dim_y,
                                             self.game.dim_z)
            return SUCCESS

        elif tile is dirt_block:

            alternate_action = Dig(self.direction)
            alternate_action.bind(self.actor)
            return alternate_action.execute()


class Drift(Move):
    # Drift is the same as move, except drifting into something 
    # won't cause you to dig/attack it
    def __init__(self, direction):
        self.direction = direction
           

class Dig(Action):
    def __init__(self, direction):
        self.direction = direction

    def execute(self):
        flatten = self.game.flatten

        if not self.actor:
            raise NameError('No actor bound to action %s', str(self))

        # Get the place the entity is trying to move into
        final_pos = self.actor.pos + self.direction
        grid = self.game.world[final_pos.z]
        tile = grid[flatten(final_pos)]

        # These can access out of bounds, so they're calculated modulo
        # the game's height– this makes them wrap around
        ceiling = self.game.world[(final_pos.z+1)%self.game.dim_z]
        floor = self.game.world[(final_pos.z-1)%self.game.dim_z]

        if tile is dirt_block:
            self.actor.pos = final_pos
            grid[flatten(final_pos)] = empty_space
            return SUCCESS

        else: 
            # Dig should NEVER be tried on other things; 
            # Move should take care of all the alternates
            return FAILURE



class Attack(Action):
    def execute(self):
        return SUCCESS

    
dirt_block = Tile('dirt', '.')
stone_block = Tile('stone', '#')
empty_space = Tile('space', ' ')


class Entity(object):
    ''' A game actor, either hero, monster, or NPC '''

    def __init__(self, game, name, sprite, pos):
        self.name = name
        # In a sane implementation, Sprite would be a class. But not here!
        self.sprite = sprite
        self.pos = pos
        self.game = game # Binds the entity to a game instance
        # For knockback and forced actions
        self.next_action = None

    def get_action(self):
        # Defined by the subclass
        raise NotImplementedError

N = Pos(0, -1, 0)
S = Pos(0, 1, 0)
W = Pos(1, 0, 0)
E = Pos(-1, 0, 0)
UP = Pos(0, 0, 1)
DN = Pos(0, 0, -1)
NONE = Pos(0, 0, 0)

def handle_input():
    cmd = input()
    direction_lookup = {
        'w': Move(N),
        'a': Move(E),
        's': Move(S),
        'd': Move(W),
        '<': Move(UP),
        '>': Move(DN),
        # Alternatively, up/down arrows
        '\x1b[A': Move(UP),
        '\x1b[B': Move(DN)
        }
    return direction_lookup.get(cmd, Move(NONE))

class Hero(Entity):
    ''' A hero is an entity that gets user input '''
    def get_action(self):
        # Ask for input, no matter if there's a predetermined action
        # Otherwise, the game be refreshed as fast as the terminal can write.
        action = handle_input()

        # But, ignore the user's command if the hero's next move is set
        if self.next_action is not None:
            action = self.next_action
            self.next_action = None
            return action

        return action


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

        self.entities = [self.hero] # TODO: Un-hardcode
        self.active_entity = 0

        # Things that happened in a step before an update
        self.events = []
        self.graphics = ASCIIRenderer(self)

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
    graphics = renderer(game)
    while True:
        game.step()
        graphics.generate_buffer()
        graphics.render()

if __name__ == "__main__":
    game = Game(16, 8, 16)
    main_loop(game, ASCIIRenderer)
