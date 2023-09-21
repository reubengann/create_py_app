# Adapted from https://github.com/wong2/pick

import curses
import curses.ascii
from typing import Protocol


class Screen(Protocol):
    def getmaxyx(self) -> tuple[int, int]:
        ...

    def clear(self):
        ...

    def addnstr(self, y: int, x: int, s: str, n: int):
        ...

    def refresh(self):
        ...

    def getch(self) -> int:
        ...


INDICATOR = "*"
SYMBOL_FILLED_CIRCLE = "(x)"
SYMBOL_EMPTY_CIRCLE = "( )"
VS_CODE_KEY_UP = 450
VS_CODE_KEY_DOWN = 456

KEYS_ENTER = (curses.KEY_ENTER, ord("\n"), ord("\r"))
KEYS_UP = (curses.KEY_UP, ord("k"), VS_CODE_KEY_UP)
KEYS_DOWN = (curses.KEY_DOWN, ord("j"), VS_CODE_KEY_DOWN)
QUIT_KEYS = (curses.ascii.ESC, ord("q"))
KEYS_SELECT = (curses.KEY_RIGHT, ord(" "))


class Picker:
    def __init__(
        self, options: list[str], title: str, default_to_enabled=False
    ) -> None:
        self.index = 0
        self.selected_indexes: list[int] = []
        self.title = title
        self.options = options
        if default_to_enabled:
            self.selected_indexes = list(range(len(options)))

    def run_loop(self, screen: Screen) -> list[str] | None:
        while True:
            self.draw(screen)
            c = screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                if len(self.selected_indexes) < 1:
                    continue
                return [self.options[i] for i in self.selected_indexes]
            elif c in QUIT_KEYS:
                return None
            elif c in KEYS_SELECT:
                self.mark_index()

    def mark_index(self) -> None:
        if self.index in self.selected_indexes:
            self.selected_indexes.remove(self.index)
        else:
            self.selected_indexes.append(self.index)

    def move_up(self) -> None:
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self) -> None:
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def draw(self, screen: Screen):
        screen.clear()
        x, y = 1, 1
        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y
        lines, current_line = self.get_lines()
        scroll_top = 0
        if current_line > max_rows:
            scroll_top = current_line - max_rows

        lines_to_draw = lines[scroll_top : scroll_top + max_rows]

        for line in lines_to_draw:
            screen.addnstr(y, x, line, max_x - 2)
            y += 1

        screen.refresh()

    def get_title_lines(self) -> list[str]:
        if self.title:
            return self.title.split("\n") + [""]
        return []

    def get_option_lines(self) -> list[str]:
        lines: list[str] = []
        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = INDICATOR
            else:
                prefix = len(INDICATOR) * " "

            symbol = (
                SYMBOL_FILLED_CIRCLE
                if index in self.selected_indexes
                else SYMBOL_EMPTY_CIRCLE
            )
            prefix = f"{prefix} {symbol}"
            lines.append(f"{prefix} {option}")

        return lines

    def get_lines(self) -> tuple[list[str], int]:
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def start(self):
        return curses.wrapper(self._start)

    def _start(self, screen: Screen):
        self.config_curses()
        return self.run_loop(screen)

    def config_curses(self) -> None:
        try:
            # use the default colors of the terminal
            curses.use_default_colors()
            # hide the cursor
            curses.curs_set(0)
        except:
            # Curses failed to initialize color support, eg. when TERM=vt100
            curses.initscr()


def pick(options: list[str], title: str):
    picker = Picker(options, title, False)
    return picker.start()
