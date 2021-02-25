# -*- coding: utf-8 -*-

from readchar import key
from .base import BaseConsoleRender
from inquirer import errors


class Text(BaseConsoleRender):
    title_inline = True

    def __init__(self, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self.current = self.question.default or ''
        self.cursor_offset = 0

    def get_current_value(self):
        return self.current + (self.terminal.move_left * self.cursor_offset)

    def process_input(self, pressed):
        if pressed == key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed in (key.CR, key.LF, key.ENTER):
            raise errors.EndOfInput(self.current)

        if pressed == key.BACKSPACE:
            if self.current and self.cursor_offset != len(self.current):
                if self.cursor_offset > 0:
                    self.current = (self.current[:-self.cursor_offset - 1] +
                                    self.current[-self.cursor_offset:])
                else:
                    self.current = self.current[:-1]
        elif pressed == key.LEFT:
            if self.cursor_offset < len(self.current):
                self.cursor_offset += 1
        elif pressed == key.RIGHT:
            self.cursor_offset = max(self.cursor_offset - 1, 0)
        elif len(pressed) != 1:
            return
        else:
            if self.cursor_offset == 0:
                self.current += pressed
            else:
                self.current = ''.join((
                    self.current[:-self.cursor_offset],
                    pressed,
                    self.current[-self.cursor_offset:]
                ))
