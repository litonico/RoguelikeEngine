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
        world = self.game.world
        if not self.actor:
            raise NameError('No actor bound to action %s', str(self))

        # Get the place the entity is trying to move into
        final_pos = self.actor.pos + self.direction
        tile = world.get(final_pos)

        # If there are no walls around the player, keep drifting in direction
        if ((world.get(final_pos + N) is empty_space) and
            (world.get(final_pos + S) is empty_space) and
            (world.get(final_pos + E) is empty_space) and
            (world.get(final_pos + W) is empty_space) and
            (world.get(final_pos + UP) is empty_space) and
            (world.get(final_pos + DN) is empty_space)):

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
        world = self.game.world

        if not self.actor:
            raise NameError('No actor bound to action %s', str(self))

        # Get the place the entity is trying to move into
        final_pos = self.actor.pos + self.direction
        tile = world.get(final_pos)

        if tile is dirt_block:
            self.game.world.set(final_pos, empty_space)
            self.actor.pos = final_pos
            return SUCCESS

        else: 
            # Dig should NEVER be tried on other things; 
            # Move should take care of all the alternates
            return FAILURE



class Attack(Action):
    def execute(self):
        return SUCCESS
