import sys

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
        for entity in self.game.entities:
            if entity.pos.z == self.game.hero.pos.z:
                self.buf[self.game.flatten(entity.pos)] = entity.sprite

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




