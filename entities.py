from utility import Pos, N, S, E, W, UP, DN, NONE
from actions import Move, Dig, Attack

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


class Hero(Entity):
    ''' A hero is an entity that gets user input '''
    def handle_input(self, cmd):
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
 
    def get_action(self):
        # Ask for input, no matter if there's a predetermined action
        # Otherwise, the game be refreshed as fast as the terminal can write.
        action = self.handle_input(self.game.ui.get_user_input())

        # But, ignore the user's command if the hero's next move is set
        if self.next_action is not None:
            action = self.next_action
            self.next_action = None
            return action

        return action


