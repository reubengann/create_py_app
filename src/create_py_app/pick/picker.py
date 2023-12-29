# Adapted from https://github.com/wong2/pick

from abc import ABC, abstractmethod
from create_py_app.pick.curses_wrap import (
    Screen,
    config_curses,
    run_and_return_result,
)

import create_py_app.pick.keycodes as kc


INDICATOR = "*"
SYMBOL_FILLED_CIRCLE = "(x)"
SYMBOL_EMPTY_CIRCLE = "( )"
VS_CODE_KEY_UP = 450
VS_CODE_KEY_DOWN = 456

KEYS_ENTER = (kc.KEY_ENTER, ord("\n"), ord("\r"))
KEYS_UP = (kc.KEY_UP, ord("k"), VS_CODE_KEY_UP)
KEYS_DOWN = (kc.KEY_DOWN, ord("j"), VS_CODE_KEY_DOWN)
QUIT_KEYS = (kc.ESC, ord("q"))
KEYS_SELECT = (kc.KEY_RIGHT, ord(" "))


class Picker(ABC):
    options: list[str]
    title: str

    @abstractmethod
    def get_option_lines(self) -> list[str]:
        pass

    @abstractmethod
    def run_loop(self, screen: Screen) -> list[str] | None:
        pass

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

    def get_lines(self) -> tuple[list[str], int]:
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def start(self) -> list[str] | None:
        return run_and_return_result(self._start)

    def _start(self, screen: Screen):
        config_curses()
        return self.run_loop(screen)


class MultiOptionsPicker(Picker):
    def __init__(self, options: list[tuple[str, bool]], title: str) -> None:
        self.index = 0
        self.selected_indexes: list[int] = []
        self.title = title
        self.options = [o[0] for o in options]
        self.selected_indexes = []
        for i, opt in enumerate(options):
            if opt[1]:
                self.selected_indexes.append(i)

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


class SingleItemPicker(Picker):
    def __init__(self, options: list[str], title: str) -> None:
        self.index = 0
        self.title = title
        self.options = options

    def run_loop(self, screen: Screen) -> list[str] | None:
        while True:
            self.draw(screen)
            c = screen.getch()
            if c in KEYS_UP:
                self.move_up()
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in QUIT_KEYS:
                return None
            elif c in KEYS_SELECT + KEYS_ENTER:
                return [self.options[self.index]]

    def get_option_lines(self) -> list[str]:
        lines: list[str] = []
        for index, option in enumerate(self.options):
            if index == self.index:
                prefix = "==>"
            else:
                prefix = len("==>") * " "
            lines.append(f"{prefix} {option}")
        return lines
