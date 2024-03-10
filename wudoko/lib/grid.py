"""
A character grid class
"""
import  numpy                   as np
from    argparse                import Namespace
from    wudoko.models.data      import Space, Dimensions, GridCoord, BreakOut
from    wudoko.lib.path         import Path
from    wudoko.lib.trajectory   import Trajectory
from    typing                  import Generator

class Grid:
    """ Keep in mind that the Grid is "internally" referenced by (row, col) in
        the numpy "grid" data structure, but GridCoords are indexed as (x, y),
        i.e. (col, row). For the most part, this internal "switch" is of no
        concern to a user/client. Simply use GridCoords to access grid locations
        and all will be fine.
    """

    def __init__(self, gridSize:Dimensions, fillChar:str = "*"):
        self.fillChar:str   = fillChar
        self.gridSize       = gridSize
        self.grid           = np.full((gridSize.y, gridSize.x), fillChar, dtype = 'U1')

    def rows(self) -> list[int]:
        return list(range(self.gridSize.y))

    def cols(self) -> list[int]:
        return list(range(self.gridSize.x))

    def get(self, coord:GridCoord) -> str:
        x, y            = coord.tuple()
        if not (0 <= x < self.grid.shape[1] and 0 <= y < self.grid.shape[0]):
            raise IndexError(f"Coordinate {coord} is out of bounds")
        return self.grid[y, x]

    def get_alongPath(self, trajectory:Path) -> str:
        lookup:str  = ""
        for cell in trajectory.path:
            lookup += self.get(cell)
        return lookup

    def cellIterate(self) -> Generator[GridCoord, None, None]:
        for y in self.rows():
            for x in self.cols():
                yield GridCoord(x=x, y=y)

    def copy(self) -> 'Grid':
        gridCopy:'Grid' = Grid(self.gridSize, self.fillChar)
        gridCopy.grid   = np.array(self.grid)
        return gridCopy

    def set(self, coord:GridCoord, value:str) -> str:
        x, y            = coord.tuple()
        if not (0 <= x < self.grid.shape[1] and 0 <= y < self.grid.shape[0]):
            raise IndexError(f"Coordinate {coord} is out of bounds")
        if len(value) != 1:
            raise ValueError(f"Character must be a single character string, got '{value}'")
        self.grid[y, x] = value
        return value

    def empty(self, coord:GridCoord) -> bool:
        return True if self.get(coord) == self.fillChar else False

    def word_canInsert(self, word:str, alonglocation:Path) -> bool:
        b_ret:bool      = True
        if len(word) != len(alonglocation.path):
            raise ValueError(
                f"length of word '{word}' and location path (len: {len(alonglocation.path)}) mismatch"
            )
        char:str        = ''
        gridPos         = GridCoord(x = 0, y = 0)
        for char,gridPos in zip(word, alonglocation.path):
            if char == self.get(gridPos) or self.empty(gridPos):
                continue
            else:
                b_ret   = False
                break
        return b_ret

    def word_insert(self, word:str, alonglocation:Path) -> str:
        inserted:str    = ""
        if len(word) != len(alonglocation.path):
            raise ValueError(
                f"length of word {word} and location path (len: {len(alonglocation.path)}) mismatch"
            )
        char:str        = ''
        gridPos         = GridCoord(x = 0, y = 0)
        for char,gridPos in zip(word, alonglocation.path):
            if char == self.get(gridPos) or self.empty(gridPos):
                self.set(gridPos, char)
                inserted += char
            else:
                break
        return inserted

    def has_word(self, word:str) -> bool:
        wordFound:bool  = False
        try:
            for cell in self.cellIterate():
                trajectory:Trajectory   = Trajectory(self.gridSize)
                trajectories:list[Path] = trajectory.paths_find(cell, len(word))
                for path in trajectories:
                    if self.get_alongPath(path) == word:
                        wordFound       = True
                        raise BreakOut
        except BreakOut:
            pass
        return wordFound

    def is_full(self) -> bool:
        # Find a mask of all cells that are empty
        nonEmptyMask:np.ndarray     = (self.grid != self.fillChar)
        # Check if any are empty and return accordingly...
        if not np.all(nonEmptyMask):
            return False
        # Now, get all the values in these nonempty cells
        nonEmptyCells:np.ndarray    = self.grid[nonEmptyMask]
        # ... and check that they only contain alphabetic characters
        is_alphabetic:np.ndarray    = ((nonEmptyCells >= 'a') & (nonEmptyCells <= 'z')) |\
                                      ((nonEmptyCells >= 'A') & (nonEmptyCells <= 'Z'))
        return bool(np.all(is_alphabetic))

    # These two methods are just to get the grid as a string, i.e. for printing
    def rows_get(self) -> Generator[str, None, None]:
        """ yield each row of the grid, row by row """
        for row in self.grid:
            yield ' '.join(row)

    def __str__(self) -> str:
        line:str        = ""
        wholeGrid:str   = ""
        for line in self.rows_get():
            wholeGrid += line + '\n'
        return wholeGrid
