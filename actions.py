from utility import Pos, N, S, E, W, UP, DN, NONE
from tiles import *
SUCCESS = True
FAILURE = False


class Action(object):
    def bind(self, actor):
        self.actor = actor
        self.game = actor.game

    def execute(self):
        raise NotImplementedError


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
