import random
import curses

class Square(object):
    def __init__(self):
        self.sum = 0
        self.mine = 0
        self.marked = False
        self.revealed = False

class Grid(object):
    def __init__(self):
        self.mine_revealed = False
        self.grid = [[Square() for _ in range(12)] for _ in range(21)]
        self.populate_mines()
        self.compute_sums()
        self.unrevealed = 12 * 21
        self.win_condition_met = False

    def populate_mines(self):
        mines = 37
        while mines:
            self.grid[random.randrange(21)][random.randrange(12)].mine = 1
            mines -= 1

    def compute_sums(self):
        for i, row in enumerate(self.grid):
            for j, square in enumerate(row):
                square.sum = sum(self.grid[a][b].mine if 0 <= a < 21 and 0 <= b < 12 else 0 for (a, b) in self.neighbors(i, j))

    def reveal(self, x, y):
        if self.grid[x][y].marked:
            return

        self.grid[x][y].revealed = True
        self.unrevealed -= 1

        if self.unrevealed == 37:
            win_condition_met = True

        if self.grid[x][y].mine:
            self.mine_revealed = True
            return

        if self.grid[x][y].sum == 0:
            for (a, b) in self.neighbors(x, y):
                if 0 <= a < 21 and 0 <= b < 12 and not self.grid[a][b].revealed:
                    self.reveal(a, b)

    def mark(self, x, y):
        self.grid[x][y].marked = True

    def unmark(self, x, y):
        self.grid[x][y].marked = False

    def toggle_mark(self, x, y):
        if self.grid[x][y].marked:
            self.unmark(x, y)
        else:
            self.mark(x, y)

    def neighbors(self, x, y):
            return [(x - 1, y), (x - 1, y - 1), (x - 1, y + 1),
                    (x, y - 1), (x, y + 1),
                    (x + 1, y), (x + 1, y - 1), (x + 1, y + 1)]

    def draw(self, win):
        for i, row in enumerate(self.grid):
            for j, square in enumerate(row):
                x_pos = j + 2 * j
                if square.marked:
                    win.addstr(i, x_pos, '+')
                elif square.revealed:
                    win.addstr(i, x_pos, '{}'.format(square.sum if not square.mine else 'x'))
                else:
                    win.addstr(i, x_pos, '-')
            
def main():
    # curses setup
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    grid = Grid()
    grid.draw(stdscr)
    stdscr.move(0, 0)

    while True:
        cmd = stdscr.getkey()
        y, x = stdscr.getyx()

        if cmd == 'q':
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            break
        elif cmd == 'KEY_RIGHT':
            if x < 33:
                stdscr.move(y, x + 3)
        elif cmd == 'KEY_LEFT':
            if x > 0:
                stdscr.move(y, x - 3)
        elif cmd == 'KEY_UP':
            if y > 0:
                stdscr.move(y - 1, x)
        elif cmd == 'KEY_DOWN':
            if y < 20:
                stdscr.move(y + 1, x)
        elif cmd == 'z':
            grid.reveal(y, x // 3)
            stdscr.erase()
            grid.draw(stdscr)

            if grid.mine_revealed:
                stdscr.addstr(10, 12, 'YOU LOSE!', curses.A_REVERSE)
                curses.curs_set(0)
                stdscr.getch()
                stdscr.erase()
                grid = Grid()
                grid.draw(stdscr)
                curses.curs_set(1)

            if grid.win_condition_met:
                stdscr.addstr(10, 12, 'YOU WIN!', curses.A_REVERSE)
                curses.curse_set(0)
                stdscr.getch()
                stdscr.erase()
                grid = Grid()
                grid.draw(stdscr)
                curses.curs_set(1)

            stdscr.move(y, x)
        elif cmd == 'x':
            grid.toggle_mark(y, x // 3)
            stdscr.erase()
            grid.draw(stdscr)
            stdscr.move(y, x)

        stdscr.refresh()

if __name__ == '__main__':
    main()
