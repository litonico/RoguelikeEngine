import unittest
from roguelike import *

# Graphics isn't tested, it's simple and if things go wrong it's obvious

# Game tests

# Fake input by messing with the builtin function. 
# This is kind of a terrible idea, but it's the only way I could hack it
real_input = __builtins__.input
def mock_input(char):
    __builtins__.input = lambda: char
    return None

class EntityTests(unittest.TestCase):
    def setUp(self):
        self.game = Game(16, 8, 16)
        dim_x, dim_y = self.game.dim_x, self.game.dim_y

        self.movegirl = Entity(self.game, 'Move Girl', '#', Pos(dim_x//2, dim_y//2, 0))
        def move_act():
            return Move(E)
        self.movegirl.get_action = move_act

        self.digboy = Entity(self.game, 'Dig Boy', '$', Pos(dim_x//2, dim_y//2, 0))
        self.digboy.get_action = lambda: Dig(E)

    def test_moving(self):
        self.game.entities.append(self.movegirl)
        # make sure she can move without digging
        self.game.world[0] = [
                empty_space for i in range(self.game.dim_x*self.game.dim_y)]
        original_pos = self.movegirl.pos
        self.game.step()
        self.assertEqual(self.movegirl.pos, (original_pos + E))
        #remove movegirl so she doesn't mess with the next test
        self.game.entites.pop()

    def test_digging(self):
        self.game.entities.append(self.digboy)
        original_pos = self.movegirl.pos
        self.game.step()
        self.assertEqual(self.digboy.pos, (original_pos + E))
        #remove digboy so he doesn't mess with the next test
        self.game.entites.pop()


    def test_attacking(self):
        pass

class HeroTests(unittest.TestCase):
    def setUp(self):
        self.game = Game(16, 8, 16)
        self.game.world[0] = [
                empty_space for i in range(self.game.dim_x*self.game.dim_y)]
        hero = self.game.hero

    def test_movement_off_grid(self):
        mock_input('w')
        for i in range(self.game.dim_y+5):
            self.game.step()
            # Hackishly prevent the hero from drifting endlessly
            self.game.hero.next_action = None

        mock_input('a')
        for i in range(self.game.dim_x+5):
            self.game.step()
            self.game.hero.next_action = None

    def test_movement_off_top(self):
        mock_input('\x1b[A')
        for i in range(self.game.dim_z+5):
            self.game.step()
            self.game.hero.next_action = None

    def test_movement_off_bot(self):
        mock_input('\x1b[B')
        for i in range(self.game.dim_z+5):
            self.game.step()
            self.game.hero.next_action = None

__builtins__.input = real_input


if __name__ == "__main__":
    unittest.main()
