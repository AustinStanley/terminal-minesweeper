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

    def neighbors(self, x, y):
            return [(x - 1, y), (x - 1, y - 1), (x - 1, y + 1),
                    (x, y - 1), (x, y + 1),
                    (x + 1, y), (x + 1, y - 1), (x + 1, y + 1)]

    def draw(self):
        for i, row in enumerate(self.grid):
            print('{}\t'.format(i + 1), end='')
            for square in row:
                if square.marked:
                    print('+\t', end='')
                elif square.revealed:
                    print('{}\t'.format(square.sum if not square.mine else 'x'), end='')
                else:
                    print('-\t', end='')
            print('\n')
        print(' \tA\tB\tC\tD\tE\tF\tG\tH\tI\tJ\tK\tL')
            
def main():
    grid = Grid()
    cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

    while True:
        grid.draw()

        if grid.mine_revealed:
            print('You lose!')
            break

        cmd = input('>>> ')
        
        if cmd.lower() == 'q':
            break
        else:
            try:
                cmd = (cmd[0].lower(), cols.index(cmd[1].upper()), int(cmd[2:]) - 1)

                if cmd[0] == 'm':
                    grid.mark(cmd[2], cmd[1])
                elif cmd[0] == 'u':
                    grid.unmark(cmd[2], cmd[1])
                elif cmd[0] == 'r':
                    grid.reveal(cmd[2], cmd[1])
                else:
                    print('Invalid command')
            except IndexError:
                print('Invalid command')

if __name__ == '__main__':
    main()
