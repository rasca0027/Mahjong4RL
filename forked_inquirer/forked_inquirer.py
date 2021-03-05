import inquirer
from inquirer.render.console._list import List as ListRenderer
from inquirer.render.console import ConsoleRender
from inquirer.themes import Theme
from readchar import key
from blessed import Terminal

term = Terminal()


class InquirerList(inquirer.List):
    def __init__(self,
                 name,
                 message='',
                 choices=None,
                 default=None,
                 ignore=False,
                 validate=True,
                 carousel=False,
                 vertical=True):

        super(inquirer.List, self).__init__(
            name, message, choices,
            default, ignore, validate
        )
        self.carousel = carousel
        self.vertical = vertical


def process_input(self, pressed):
    question = self.question
    if question.vertical:
        up = key.UP
        down = key.DOWN
    else:
        up = key.LEFT
        down = key.RIGHT
    if pressed == up:
        if question.carousel and self.current == 0:
            self.current = len(question.choices) - 1
        else:
            self.current = max(0, self.current - 1)
        return
    if pressed == down:
        if question.carousel and self.current == len(question.choices) - 1:
            self.current = 0
        else:
            self.current = min(
                len(self.question.choices) - 1,
                self.current + 1
            )
        return
    if pressed == key.ENTER:
        value = self.question.choices[self.current]
        raise inquirer.errors.EndOfInput(getattr(value, 'value', value))

    if pressed == key.CTRL_C:
        raise KeyboardInterrupt()


def _event_loop(self, render):
    try:
        while True:
            self._relocate()
            self._print_status_bar(render)
            if not render.question.vertical:
                self._print_header_h(render)
            else:
                self._print_header(render)
                self._print_options(render)

            self._process_input(render)
            self._force_initial_column()
    except inquirer.errors.EndOfInput as e:
        self._go_to_end(render)
        return e.selection


def _print_header(self, render):
    base = render.get_header()

    header = (base[:self.width - 9] + '...'
              if len(base) > self.width - 6
              else base)
    msg_template = "{t.move_up}{t.clear_eol}{t.normal}{msg}"

    # ensure any user input with { or } will not cause a formatting error
    escaped_current_value = (
        "{tq.mark_color}"
        + str(render.get_current_value())
        .replace('{', '{{')
        .replace('}', '}}')
        + "{t.normal}"
    )
    self.print_str(
        '\n%s: %s' % (msg_template, escaped_current_value),
        msg=header,
        lf=not render.title_inline,
        tq=self._theme.Question)


def _print_header_h(self, render):
    base = render.get_header()

    header = (base[:self.width - 9] + '...'
              if len(base) > self.width - 6
              else base)
    msg_template = "{t.move_up}{t.clear_eol}{t.normal}{msg}"

    # ensure any user input with { or } will not cause a formatting error
    escaped_current_value = (
        "{tq.mark_color}"
        + str(render.get_current_value())
        .replace('{', '{{')
        .replace('}', '}}')
        + "{t.normal}"
    )
    self.print_str(
        '%s:\n << %s >>' % (msg_template, escaped_current_value),
        msg=header,
        lf=not render.title_inline,
        tq=self._theme.Question)


class BlueTheme(Theme):

    def __init__(self):
        super(BlueTheme, self).__init__()
        self.Question.mark_color = term.blue


setattr(ListRenderer, 'process_input', process_input)
setattr(ConsoleRender, '_event_loop', _event_loop)
setattr(ConsoleRender, '_print_header', _print_header)
setattr(ConsoleRender, '_print_header_h', _print_header_h)
