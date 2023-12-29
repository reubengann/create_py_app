import curses
from typing import Callable, Protocol


class CursesWrapper(Protocol):
    pass


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


def run_and_return_result(st: Callable[[Screen], list[str] | None]) -> list[str] | None:
    return curses.wrapper(st)  # type: ignore


def config_curses():
    try:
        # use the default colors of the terminal
        curses.use_default_colors()  # type: ignore
        # hide the cursor
        curses.curs_set(0)  # type: ignore
    except:
        # Curses failed to initialize color support, eg. when TERM=vt100
        curses.initscr()  # type: ignore
