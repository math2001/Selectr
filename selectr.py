# -*- encoding: utf-8 -*-

from getch import getch
import sys
import click
import colorama

# colorama.init()

class _Select:

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    ARROW = b'\xe0'

    def render(self):
        for i, option in enumerate(self.options):
            if i == self.index:
                print('=> ', end='')
            else:
                print(' ' * 3, end='')
            print(option)

    def clear(self):
        for _ in range(len(self.options) + self._extra_rows):
            print(_Select.CURSOR_UP_ONE, _Select.ERASE_LINE, end='', sep='')
        self._extra_rows = 0

    def move(self, way):
        self.index += way
        if self.index < 0:
            self.index = 0
        elif self.index >= len(self.options):
            self.index = len(self.options) - 1
        self.clear()
        self.render()

    def select(self):
        char = getch()
        if char == _Select.ARROW:
            char = getch()
            if char == b'H':
                self.move(-1) # up
            elif char == b'P':
                self.move(1) # down
            return self.select()
        elif char == b'\r': # enter
            if self._want_index:
                return self.options[self.index], self.index
            return self.options[self.index]
        elif char == b'\x1b': # escape
            return
        else:
            print('Invalid key, please use only the UP/DOWN arrows, enter, and escape.')
            self._extra_rows += 1
            return self.select()

    def run(self, options, default_index, want_index):
        self.options = options
        self.index = default_index
        self._extra_rows = 0
        self._want_index = want_index
        self.render()
        return self.select()


def select(*options, **kwargs):
    return _Select().run(options, kwargs.get('default_index', 0), kwargs.get('want_index', False))

if __name__ == "__main__":
    print('You are:')
    type_ = select('A developer', 'A designer', 'A mutant', 'None of the above?')
    if not type_:
        print("Ho... you don't want to tell me?")
    else:
        print("You're {}?! That's awesome!".format(type_.lower()))
